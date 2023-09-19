import boto3


def upload_file_to_s3(bucket_name, file_name, s3_key):
    s3 = boto3.client('s3')
    # Uploading file to S3
    try:
        s3.upload_file(file_name, bucket_name, s3_key)
        message = f"Success: {file_name} uploaded to {bucket_name}"
        return True, message
    except Exception as e:
        message = f"Error: Failed to upload {file_name} to {bucket_name}. Because: {str(e)}"
        return False, message


def send_sns_notifications(message, email_address):
    sns = boto3.client('sns')
    try:
        response_email = sns.publish(
            TopicArn='arn:aws:sns:us-west-2:684418257331:snsForpythonTesting',
            Message=message,
            Subject="SNS Notification",
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': email_address
                }
            }
        )
        print(f"Notification sent to {email_address}: {response_email['MessageId']}")
        return True
    except Exception as e:
        print(f"Error sending notification to {email_address}: {str(e)}")
        return False
