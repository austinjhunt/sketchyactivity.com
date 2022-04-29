from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from ..models import PortfolioItem, MetaStuff
from django.shortcuts import render, redirect
from .s3 import s3_client
from .util import resize_image, rp, update_private_url_single
import datetime
import os

# Super mods.
@csrf_exempt
def upload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST' and request.FILES['newfile']:
            """ Have inmemoryuploadedfile. That's what uploadprivate expects as file arg. need to
            1. save original with upload private in the 'drawings' """
            # Save the regular image, but also save a 30% version to show in preview (smaller size = faster load)
            # Regular image
            myfile = request.FILES['newfile']
            fs = FileSystemStorage(location='', file_permissions_mode=0o655)
            filename = fs.save(myfile.name, myfile)
            response1 = s3_client.upload_file(
                filename,
                'sketchyactivitys3',
                f'media/drawings/{myfile.name}',
                ExtraArgs={
                    'ACL':'private'
                }
            )
            resize_path = f'/tmp/{filename}'
            resize_image(filename,  resize_path)
            response2 = s3_client.upload_file(
                resize_path,
                'sketchyactivitys3',
                f'media/copied_smaller_drawings/{myfile.name}',
                ExtraArgs={'ACL':'private'}
                )
            os.remove(filename)
            # Initialize private urls to empty strings
            s3_drawing_private_url = ""
            s3_copied_smaller_drawing_private_url = ""

            tag = rp(request, 'tag')
            if not tag:
                tag = 'Portrait'

            date = rp(request,'date')
            # create a new object in DB for naming
            new_item = PortfolioItem(
                tag=tag,
                portrait_name=rp(request,"portraitname"),
                filename=myfile.name,
                date=date,
                s3_drawing_private_url=s3_drawing_private_url,
                s3_copied_smaller_drawing_private_url=s3_copied_smaller_drawing_private_url)
            new_item.save()

            update_private_url_single(new_item, s3_client)

            return redirect('/')
        return render(request=request, template_name='super/upload.html', context={'title': 'Add Content'})
    else:
        return redirect('/')




def update_profile(request):
    """ View for updating profile, starting for now just with bio """
    if request.method == "POST":
        bio = request.POST.get('bio','')
        website_title = request.POST.get('website_title','')
        website_description = request.POST.get('website_description','')
        website_keywords = request.POST.get('website_keywords','')
        sale = True if request.POST.get('commission_sale', None) else False
        sale_amount = request.POST.get('commission_sale_amount', 0)
        sale_end = request.POST.get('commission_sale_end','')
        ms = MetaStuff.objects.all()[0]
        ms.website_title = website_title
        ms.website_description = website_description
        ms.website_keywords = website_keywords
        ms.sale = sale
        ms.sale_amount = sale_amount
        ms.sale_end = datetime.datetime.strptime(sale_end, '%Y-%m-%d').date()
        ms.bio = bio
        ms.save()
        return redirect("/")
    else:
        bio = MetaStuff.objects.all()[0].bio
        return render(
            request=request,
            template_name='super/update_profile.html',
            context={'bio':bio, 'title': 'Update Website'})