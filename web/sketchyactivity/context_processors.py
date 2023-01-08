from .models import *


def s3context(request):
    # new session, prompt with art shop
    show_redbubble_prompt = 'existing_session' not in request.session
    request.session['existing_session'] = True

    if 'page_load_count' not in request.session:
        request.session['page_load_count'] = 1
    else:
        request.session['page_load_count'] += 1
    main_preview_image = list(
        PortfolioItem.objects.all())[-1].s3_drawing_private_url
    if request.user.is_authenticated:
        cart_items = UserProfile.objects.get(user=request.user).cart.all()
    else:
        cart_items = []
    return {
        'base_media_url': '',
        'preview_image': main_preview_image,
        'page_load_count': request.session.get('page_load_count'),
        'meta': MetaStuff.objects.first(),
        'cart_items': cart_items,
        'show_redubble_prompt': show_redbubble_prompt
    }
