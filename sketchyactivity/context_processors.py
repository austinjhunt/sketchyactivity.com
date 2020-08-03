from .models import *
from myproject.settings import MEDIA_URL
def s3context(request): 
    return {'base_media_url': MEDIA_URL}