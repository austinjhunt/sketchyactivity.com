from django.db import models

from sketchyactivity.storage_backends import PrivateMediaStorageThumbnail,PrivateMediaStorageOriginal



class UploadPrivateOriginal(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=PrivateMediaStorageOriginal())
class UploadPrivateThumbnail(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=PrivateMediaStorageThumbnail())