from django.core.management.base import BaseCommand
from order.models import OrderPicture
from django.conf import settings
import boto3

class Command(BaseCommand):
    help = 'Deletes orphaned images for the Order Picture model (files in storage with no database reference).'

    def handle(self, *args, **kwargs):
        # Fetch all image names stored in the database
        stored_images = set(OrderPicture.objects.values_list('image', flat=True))

        # Fetch all objects from the bucket
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        objects = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket is empty
        if 'Contents' not in objects:
            self.stdout.write(self.style.WARNING('Bucket is empty. No files to clean.'))
            return

        # Iterate through bucket objects
        for obj in objects['Contents']:
            # Full path of the object in the bucket
            file_key = obj['Key']

            # Ensure file key matches the format stored in the database
            relative_path = file_key.lstrip('/')

            # Check if the file is missing in the database
            if relative_path not in stored_images:
                # Delete the orphaned file from the bucket
                s3_client.delete_object(Bucket=bucket_name, Key=file_key)
                # Log deleted file to console
                self.stdout.write(self.style.SUCCESS(f'Deleted: {file_key}'))

        # Indicate cleanup is complete
        self.stdout.write(self.style.SUCCESS(f'Bucket cleanup completed for order pictures!'))
