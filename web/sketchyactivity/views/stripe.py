from datetime import date
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import MetaStuff, Price, Purchase, UserProfile, Product
from django.shortcuts import redirect, render
from .util import get_total_price_from_cart
import stripe
import json
import logging
import datetime
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .s3 import s3_client
from .util import resize_image, rp, update_private_url_product_reference_image
import pytz
import os
logger = logging.getLogger('stripe-integration')

class AddToCartView(View, LoginRequiredMixin):

    def save_new_product(self, request): 
        size_style_price_choice = request.POST.get('size-style-price-choice')
        commission_name = request.POST.get('commission-name')
        _split = size_style_price_choice.split('-')
        style = _split[0]
        if style == 'tr': # traditional. format: tr-WxHin-numSubjects
            size = _split[1]
            num_subjects = _split[2] 
            description = f'Traditional Drawing, {size}, {num_subjects} subjects'
        elif style == 'di': # digital. no size. di-numSubjects
            num_subjects = _split[1]
            size = 'n/a'
            description = f'Digital Drawing, {num_subjects} subjects'
        reference_image_filename = request.FILES.get('referenceImage').name 
        s3_reference_image_url = ""  
        # get current price based on selection
        # prevents front end user from manipulating the price directly.
        price = Price.objects.get(
            style=style.upper(),
            size=size,
            num_subjects=num_subjects
        ).amount
        ms = MetaStuff.objects.first()
        if ms.sale_still_active():
            price = ms.get_sale_price(original_price=price)  
        new_product = Product(
            name=commission_name,
            description=description,
            type=style,
            price=price,
            reference_image_filename=reference_image_filename,
            s3_reference_image_url=s3_reference_image_url
        )
        new_product.save()
        return new_product

    def save_reference_image(self, request): 
        ## save the reference image file
        reference_image_file = request.FILES.get('referenceImage')
        fs = FileSystemStorage(location='', file_permissions_mode=0o655)
        filename = fs.save(reference_image_file.name, reference_image_file)
        response = s3_client.upload_file(
            filename,
            'sketchyactivitys3',
            f'media/commission-reference-images/{reference_image_file.name}',
            ExtraArgs={
                'ACL': 'private'
            }
        ) 
        try:
            os.remove(filename)
        except Exception as e:
            logger.error(e) 
        return response 

    def post(self, request): 
        profile = UserProfile.objects.get(user=request.user)
        if request.FILES.get('referenceImage', None) \
            and request.POST.get('size-style-price-choice', None) \
            and request.POST.get('size-style-price-choice') != 'null' \
            and request.POST.get('commission-name', None): 
            self.save_reference_image(request=request)
            new_product = self.save_new_product(request=request)
            update_private_url_product_reference_image(new_product, s3_client)
            cart = profile.cart
            cart.add(new_product)
            profile.save()
            return redirect('checkout')
        else:
            return redirect('commissions')
 

class RemoveFromCartView(View, LoginRequiredMixin):
    def get(self, request, product_id): 
        profile = UserProfile.objects.get(user=request.user)
        try: 
            cart = profile.cart
            productToRemove = Product.objects.get(id=product_id)
            description, price = productToRemove.description, productToRemove.price
            cart.remove(Product.objects.get(id=product_id))
            productToRemove.delete()
            profile.save() 
        except Exception as e:
            logger.error(e) 
        return redirect('commissions')

class ClearCartView(View, LoginRequiredMixin):
    def post(self, request):
        data = json.loads(request.body.decode())
        profile = UserProfile.objects.get(user=request.user)
        try:
            # Note this doesn’t delete the related objects – it just disassociates them.
            # Dont want to delete because product object needs to exist in order for Order
            # to persist. Don't want to lose order history.
            profile.cart.clear()
            profile.save()
            response = {
                'result': f'cart cleared',
                'totalCartItems': 0,
                'cartTotalPrice': 0
                }
        except Exception as e:
            logger.error(e)
            response = {'result': f'Error: {e}' }
        return JsonResponse(response)

class CheckoutView(View, LoginRequiredMixin):
    def get(self, request):
        cart = UserProfile.objects.get(user=request.user).cart
        for order_item in cart.all():
            update_private_url_product_reference_image(order_item, s3_client)
        total = get_total_price_from_cart(cart)
        return render(
            request=request,
            template_name='stripe/checkout.html',
            context={'cart': cart, 'total': total}
        )

class CreatePaymentIntentView(View, LoginRequiredMixin):
    def post(self, request):
        cart  = UserProfile.objects.get(user=request.user).cart
        total = get_total_price_from_cart(cart)
        stripe.api_key = settings.STRIPE_API_KEY
        data = json.loads(request.body)
        # Create a PaymentIntent with the order amount and currency
        if total >= 1:
            intent = stripe.PaymentIntent.create(
                amount=total,
                currency=data['currency'],
                metadata={'integration_check': 'accept_a_payment'},
                )
            try:
                return JsonResponse({
                    'publishableKey': settings.STRIPE_PUBLISHABLE_KEY,
                    'clientSecret': intent.client_secret
                    })
            except Exception as e:
                return JsonResponse({'error':str(e)}, status=403)
        else:
            return JsonResponse(
                {'error': 'cart is empty; not creating a payment intent'}
            )

class OrdersView(View, LoginRequiredMixin):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        orders = Purchase.objects.filter(user_profile=profile)
        for order in orders:
            update_private_url_product_reference_image(order.product, s3_client)
        return render(
            request=request,
            template_name='stripe/orders.html',
            context={'orders': orders}
        )

class PaymentCompleteView(View, LoginRequiredMixin):
    def post(self, request):
        data = json.loads(request.POST.get('payload'))
        try:
            if data['status'] == 'succeeded':
                # save purchase here for each item in user's cart before cart is cleared
                profile = UserProfile.objects.get(user=request.user)
                user_items_already_paid_for = profile.cart.all()
                for product in user_items_already_paid_for:
                    Purchase(
                        product=product,
                        user_profile=profile,
                        timestamp=timezone.now()
                    ).save()
                # clear the user's cart ; they've already paid for the items
                profile.cart.clear()
                profile.save()
            else:
                logger.error('payment not successful')
        except Exception as e:
            logger.error(e)
        return redirect('orders')

