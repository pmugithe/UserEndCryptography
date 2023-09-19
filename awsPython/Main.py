import base64
import os
from FileEncryptor import Encryptor
from DownloadFile import download_file_from_s3
from awsPython.UploadFile import upload_file_to_s3, send_sns_notifications

if __name__ == '__main__':
    encryptor = Encryptor()

    # Encrypt plain text file
    key = encryptor.key_create()
    encryptor.key_write(key, 'pradykey.txt')
    print(key)
    encryptor.file_encrypt(key, 'TestFile.txt', 'TestEncrypted.txt')
    encryptor.file_decrypt(key, 'TestEncrypted.txt', 'decrypted.txt')

    # Encrypt Excel file
    key = encryptor.key_create()
    print(key)
    encryptor.key_write(key, 'pradykey.txt')
    encryptor.excel_encrypt(key, 'grades.xlsx', 'gradesEncrypted.xlsx')
    encryptor.excel_decrypt(key, 'gradesEncrypted.xlsx', 'gradesDecrypted.xlsx')

    # uploading files to s3

    file_name = input("Enter the file name: ")
    bucket_name = input("Enter the bucket name: ")
    s3_key = bucket_name + "/" + file_name
    email_address = input("Enter your email address: ")

    upload_success, upload_result = upload_file_to_s3(bucket_name, file_name, s3_key)
    print(upload_result)

    # Calling send_sns_notifications
    if upload_success:
        message = f"File {file_name} successfully uploaded to {bucket_name}"
        notification_success = send_sns_notifications(message, email_address)
        if notification_success:
            print(f"Notification sent to {email_address}")
        else:
            print(f"Failed to send notification to {email_address}")
    else:
        error_message = f"Failed to upload file {file_name} to bucket {bucket_name}: {upload_result}"
        notification_success = send_sns_notifications(error_message, email_address)
        if notification_success:
            print(f"Error notification sent to {email_address}")
        else:
            print(f"Failed to send error notification to {email_address}")

    dow_file = download_file_from_s3(file_name, bucket_name, s3_key)
    # dow_file = 'TestEncrypted.txt'

    key = input("Enter the encryption key: ").encode('utf-8')
    url_safe_key = base64.urlsafe_b64encode(key)
    print(url_safe_key)
    decrypt_file = encryptor.file_decrypt(key=key, encrypted_file=dow_file, decrypted_file='decrypted.txt')

    print(dow_file)

    # Cleaning up Keys if we want, but it's for org so a BIG NO
    # os.remove('key.txt')
