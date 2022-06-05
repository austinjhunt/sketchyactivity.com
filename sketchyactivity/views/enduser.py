# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.core.cache import cache
from ..models import PortfolioItem
from .util import *
from .s3 import s3_client


class HomeView(View):
    @csrf_exempt
    def get(self, request):
        portfolio = PortfolioItem.objects.all().order_by('-date')
        # update private urls if they need to be updated
        if not cache.get('updated_private_video_url'):
            private_video_url = update_private_video_url(s3_client)
            cache.set('updated_private_video_url', private_video_url, timeout=302400)# half the max expiration time of the private urls for the media files in s3.
        if not cache.get('updated_private_urls'):
            print("Updating private urls for portfolio...")
            update_private_urls_full_portfolio(portfolio,s3_client)
            print("Setting cache.updated_private_urls ")
            cache.set('updated_private_urls', 'is_updated',timeout=302400) # half the max expiration time of the private urls for the media files in s3.
        else:
            print("Cache updated_private_urls is set already")
        return render(
            request=request,
            template_name='index.html',
            context={
                'featured': portfolio[0],
                'title': 'Austin Hunt Portraiture',
                'portfolio1': portfolio[:4],
                'portfolio2': portfolio[4:8],
                'portfolio3': portfolio[8:],
                'private_video_url': cache.get('updated_private_video_url')
                }
        )

class CommissionsView(View):
    def get(self, request):
        print('GET')
        traditional_prices = Price.objects.filter(style='TR')
        traditional_unique_sizes = traditional_prices.order_by('size').distinct().values_list('size', flat=True)
        traditional_unique_sizes = sorted(traditional_unique_sizes, key=lambda el: float(el.split('x')[0]))
        traditional_unique_num_subjects = traditional_prices.order_by('num_subjects').distinct().values_list('num_subjects', flat=True)

        digital_prices = Price.objects.filter(style='DI')
        digital_unique_num_subjects = digital_prices.order_by('num_subjects').distinct().values_list('num_subjects', flat=True)
        return render(
            request,
            'commissions.html',
            context={
                'title': 'Austin Hunt Portraiture Commissions',
                'traditional_prices': traditional_prices,
                'traditional_unique_sizes':  traditional_unique_sizes,
                'traditional_unique_num_subjects':  traditional_unique_num_subjects ,
                'sale':  MetaStuff.objects.all()[0].sale,
                'digital_prices': traditional_prices,
                'digital_unique_num_subjects':  digital_unique_num_subjects ,
                'sale':  MetaStuff.objects.all()[0].sale,
                'sale_amount':  MetaStuff.objects.all()[0].sale_amount
            }
        )

class PortfolioItemEdit(UpdateView):
    model = PortfolioItem
    template_name = 'super/portfolio_item_edit.html'
    fields = ['tag', 'portrait_name', 'date']
    success_url = '/'

class PortfolioItemDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    template_name = 'super/portfolio_item_delete.html'
    success_url = '/'
    def test_func(self):
        return self.request.user.is_superuser

class PortfolioManage(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'super/manage_portfolio.html'
    def get(self,request):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'portfolio': PortfolioItem.objects.all().order_by('-date')
            }
        )
    def test_func(self):
        return self.request.user.is_superuser

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['bio'] = get_bio()
        data['profile_image'] = MetaStuff.objects.first().profile_image_private_url
        return data
