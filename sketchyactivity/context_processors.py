from .models import *
def s3context(request):
    main_preview_image = list(PortfolioItem.objects.all())[-1].s3_drawing_private_url
    return {'base_media_url':'','preview_image': main_preview_image}