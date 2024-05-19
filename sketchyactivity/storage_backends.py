from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class PrivateMediaStorageOriginal(S3Boto3Storage):
    location = 'media/drawings'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
class PrivateMediaStorageThumbnail(S3Boto3Storage):
    location = 'media/copied_smaller_drawings'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False