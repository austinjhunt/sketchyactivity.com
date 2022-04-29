import boto3
from botocore.client import Config
from django.conf import settings
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2',
    config=Config(signature_version='s3v4'))
# Have to use long polling for pushing API responses from Slack to front end without front end triggering updates.
# use responses dictionary with key,val = client, last response from me
# whenever new response for given client pushed to front end (check every 10 secs), make value for key null
responses = {}
