from django.core.cache import cache
from django.conf import settings
from django.db import models
import boto3
import uuid
import os

''' Image field utilizing presigned temporary URL's '''
class PresignedURLImageField(models.ImageField):
    '''
        Initialize the field
        --------------------
        folder_name: folder where the image will be stored (e.g., 'orders', 'purchases')
    '''
    def __init__(self, folder_name = None, *args, **kwargs):
        self.folder_name = folder_name
        kwargs['upload_to'] = self.generate_upload_path
        super().__init__(*args, **kwargs)

    '''
        Generate a unique file path for the uploaded file
        -------------------------------------------------
        instance: model instance
        filename: original filename
    '''
    def generate_upload_path(self, instance, filename):
        if not self.folder_name:
            raise ValueError("The 'folder_name' argument is required.")
        base_name, ext = os.path.splitext(filename)
        unique_id = uuid.uuid4().hex[:8]
        return f'{self.folder_name}/{base_name}-{unique_id}{ext}'

    ''' Generate a pre-signed URL for accessing an object in R2 '''
    def generate_presigned_url(self, object_key):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        url = s3_client.generate_presigned_url(
            'get_object',
            Params = {
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': object_key,
            },
            ExpiresIn = 3600,
        )
        return url

    ''' Override the 'url' to return a pre-signed URL '''
    @property
    def url(self):
        # If no file is associated or debug is set to true, return None
        if settings.DEBUG or not self.name:
            return None
        # Check if the URL is already cached
        cache_key = f'presigned_url_{self.name}'
        presigned_url = cache.get(cache_key)
        if not presigned_url:
            # Generate and cache the URL
            presigned_url = self.generate_presigned_url(self.name)
            cache.set(cache_key, presigned_url, timeout=300)
        return presigned_url
