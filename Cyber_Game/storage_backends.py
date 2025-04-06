# from storages.backends.s3boto3 import S3Boto3Storage

# class MediaStorage(S3Boto3Storage):
#     location = 'media'
#     file_overwrite = False

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION
    file_overwrite = False