import boto3
from FileEncryptor import *


def download_file_from_s3(bucket_name, file_name,s3_key):
    s3_client = boto3.client('s3')
    # Uploading file to S3
    try:
        res = s3_client.download_file(bucket_name, file_name,s3_key)
        print(res)
        print(f"Success: {file_name} downloaded from {bucket_name}")
        return file_name
    except Exception as e:
        print(f"Error: Failed to download {file_name} from {bucket_name}. Because: {str(e)}")
        return None





