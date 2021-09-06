from .models import *
def s3context(request):
    if 'page_load_count' not in request.session:
        request.session['page_load_count'] = 1
    else:
        request.session['page_load_count'] += 1
    main_preview_image = list(PortfolioItem.objects.all())[-1].s3_drawing_private_url
    return {
        'base_media_url':'',
        'preview_image': main_preview_image,
        'page_load_count': request.session.get('page_load_count')
        }