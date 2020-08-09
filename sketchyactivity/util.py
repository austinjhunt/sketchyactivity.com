import json
from django.http import HttpResponse
# DRY Utility Functions
def rp(request, data):
    return request.POST.get(data)
def isauth(request):
    return request.user.is_authenticated
def fget(form,string):
    return form.cleaned_data[string]
def ajax(request):
    return request.is_ajax()

# for ajax requests, returning JSON to JS
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

MAX_EXPIRATION_ONE_WEEK_SECS = 604800

def update_private_url_single(item,s3_client):
    item.s3_drawing_private_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/drawings/{item.filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)

    item.s3_copied_smaller_drawing_private_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/copied_smaller_drawings/{item.filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)
    item.save()

def update_private_urls_full_portfolio(portfolio=None,s3_client=None):
    if portfolio:
        for p in portfolio:
            update_private_url_single(p, s3_client)