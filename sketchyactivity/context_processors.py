from .models import *
def s3context(request):
    main_preview_image = PortfolioItem.objects.get(filename="jennalynn.JPG").s3_drawing_private_url
    return {'base_media_url':'','preview_image': main_preview_image}