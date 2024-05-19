import os
from dotenv import load_dotenv
import boto3

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


def get_username():
    # print account id and username
    client = boto3.client(
        "sts",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = client.get_caller_identity()
    return response["Arn"].split("/")[-1]

def get_account_id():
    # print account id and username
    client = boto3.client(
        "sts",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = client.get_caller_identity()
    return response["Account"]


def download_all_files_from_s3_bucket(bucket_name):
    """Download all files from bucket and maintain nested folder structure"""

    s3 = boto3.client(
        "s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    paginator = s3.get_paginator("list_objects_v2")
    for result in paginator.paginate(Bucket=bucket_name):
        if result.get("Contents") is not None:
            for file in result.get("Contents"):
                if not file.get("Key").endswith('/'):  # Check if the file is not a directory
                    if not os.path.exists(os.path.dirname(file.get("Key"))):
                        os.makedirs(os.path.dirname(file.get("Key")))
                    s3.download_file(bucket_name, file.get("Key"), file.get("Key"))
                else:
                    if not os.path.exists(file.get("Key")):
                        os.makedirs(file.get("Key"))


""" Based on IAM account info, obtain information about the root account """
# Path: sketchyactivitybackend/download_s3_files.py
def get_root_info():
    # Create an Organizations client
    organizations_client = boto3.client(
        'organizations',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Get the root account ID
    root_id = organizations_client.list_roots()['Roots'][0]['Id']

    # Get the root account details
    root_details = organizations_client.describe_account(AccountId=root_id)
    return root_details

if __name__ == "__main__":
    # # download_all_files_from_s3_bucket(bucket_name=AWS_STORAGE_BUCKET_NAME)
    # # Create an Organizations client
    # organizations_client = boto3.client(
    #     'organizations',
    #     aws_access_key_id=AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    # )

    # # Get the account ID using STS
    # sts_client = boto3.client(
    #     'sts',
    #     aws_access_key_id=AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    # )

    # response = sts_client.get_caller_identity()
    # account_id = response['Account']

    # # Get the account details using Organizations
    # try:
    #     account_details = organizations_client.describe_account(AccountId=account_id)
    #     print("Account ID: ", account_details['Account']['Id'])
    #     print("Email: ", account_details['Account']['Email'])
    #     print("Name: ", account_details['Account']['Name'])
    # except organizations_client.exceptions.AWSOrganizationsNotInUseException:
    #     print("Organizations is not in use or you do not have the necessary permissions.")
    # except organizations_client.exceptions.AccessDeniedException:
    #     print("You do not have the necessary permissions to access this information.")

    print(get_root_info())
