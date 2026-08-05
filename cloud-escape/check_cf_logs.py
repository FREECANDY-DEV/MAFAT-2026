import os
import json
import boto3

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYIMLIFTXQE",
    aws_secret_access_key="2pFYytUGEJ61BMm0LEWESi0d71uWsf2TjoGpwObR",
    aws_session_token="IQoJb3JpZ2luX2VjELb//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDpaG+c2mutY4AeFGfNj7oLjQMeRIsmd0NuI37jMbzhrAiA0PNs5JJEosI8VsHZvtRtKgyq1OZfrfHIoOzZBoAugeyq1AggjEAAaDDEyMTc3NDA1Mjg4MCIMUFWh9GRVwObVUas1KpICQXRQ0m3on3qF93Q0rOaryZIVQNYEgWm6UKvUzYd+i/s6gHXodfCt1JKYpsPNqQ4gwrxvCKiP8Tr2f3tZ7Wox+TH2TTxNjYyzsDw3iedbCJp+5NXZ8xEerIpmIeyMKFM4s//Cn4k3i70ysMD3cgFkYX3A4EvOeP1bE0JukWRwJEGftHlKpmtYjijVGtGCu2bc58w9LTIRSsAztboEt4muWQ2xlNa5IYEXaciHoU3VnpkU537ZlGqpnO3MVyXukDhmj6wVhS231TXp1LS9FW9YirdqA1LU6JwCgGERQiC6FZte6VqeQW7/UvbgcIkTvUiYqHL/vzY6+TsoTNuYiqjJ0wrL4mp3FmMT5VSV6vyKEtD4FDDkhszTBjqeAd5NRHgUIjh1w6DyNpim5EeZx7ULUCpbxkUEwpyZRXQHtukm7sOeGsP4HSgp3/DvLu2pS+YhLlWx8ag+KoLE1WVynoEpjvNbG6NXlUK0eCsS81BdGTy0kHRdJCV36nZQLEdoDCPxjAZn4Nd0kihI9HU0k7EFKvtuQCtTf7B8hIydoVFQu/WMw3AAQRjYQyHDy58kBUo9u65TTgHWqZSg",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"
prefix = "userd8a2f72fe43094e8/GetObject/2026-08-05"

print("Scanning for CloudFront failed requests...")

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=log_bucket, Prefix=prefix)

found_uas = set()
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            try:
                log_obj = s3.get_object(Bucket=log_bucket, Key=obj['Key'])
                log_content = log_obj['Body'].read().decode('utf-8')
                log_data = json.loads(log_content)
                detail = log_data.get('detail', {})
                key = detail.get('requestParameters', {}).get('key', '')
                error_code = detail.get('errorCode', '')
                user_agent = detail.get('userAgent', '')
                
                # CloudFront typically has "Amazon CloudFront" in its standard UA, but we want the CUSTOM one!
                # If they set a custom header like "User-Agent: Secret", we will see "Secret"
                # So let's just look at the UserAgent for requests to nonexistent.html or flag.txt
                if key in ['nonexistent.html', 'flag.txt', 'bucket_policy.json', 'docs.html']:
                    if user_agent and not user_agent.startswith('Boto3') and not user_agent.startswith('CODE-'):
                        if user_agent not in found_uas:
                            print(f"[{error_code}] Key: {key} -> UserAgent: {user_agent}")
                            found_uas.add(user_agent)
            except Exception:
                pass
print("Done.")
