import os
import json
import boto3

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYINWI54QUF",
    aws_secret_access_key="vzoDaHLWP97VayPQRZpwLhu9+wucg+FdyJbsgKBQ",
    aws_session_token="IQoJb3JpZ2luX2VjELX//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCICgyqloerkVTXTE5628Kp386BsQLYbXsQC4+rOu6I0INAiALeJaaL7isClSF+8qxnBZHA9Hk+WTg7zcTBxBBIzGtyiq1AggiEAAaDDEyMTc3NDA1Mjg4MCIM+Rpw/jafiBZf85MDKpICyLS9DUhUvWvbZ96LLt/M2kRPwKA2Cz68ISWVyBt/A7mKpJ0/E0HNdzCBZod2V2B2A+e2pm7A0yd/0pcb4t7MErEMgPBMoIzOywtMhleclfugWQqI52Do/aUoiR3cPNfBXutl/fYMykNSRZIkU+r1RywE1Yy3nbDy9zGpa2tfXU5plezMGPO15sxKYFz6PClI98LayWhEiEl89hTv5oAdzK+O3ONrp2TM8IyZf7G3eA3t9BP1Kl19E/NtsNZkQCYQwIbOMgRbAkQMvZCBKXilYo1GUVQvrGmeoyZq3LGOgj9o9bxa5jV+Kg4TSRTdL5R0yqeQrhiq3uJBh3ybX+8lnKs+auiOvaava6lGaGyL5KdwXzCu58vTBjqeARTzARMyhUPkGpGGVOScggiv11wG1cCI039vSFoWRPBrCt2Kt1K6+sJqTm4Jxbkg0A0ca6yLHbGxCkq6f3nrdRfuDiBVACtArW8jBjgxp+saXsdfHpS6xTaGTGk8kSE7PBtzeSYzug2gmQdMjL1+LlotY2UVvcIft1FSc8YxPWu62NeRcPyGJMkbHLS/6VJcRAhPg/Vnbx9m/gkhpvl7",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"

prefix = "userd8a2f72fe43094e8/PutObject/"
print(f"Checking {prefix} logs...")

response = s3.list_objects_v2(Bucket=log_bucket, Prefix=prefix)
if 'Contents' in response:
    for obj in response['Contents']:
        log_obj = s3.get_object(Bucket=log_bucket, Key=obj['Key'])
        log_content = log_obj['Body'].read().decode('utf-8')
        try:
            log_data = json.loads(log_content)
            detail = log_data.get('detail', {})
            error_code = detail.get('errorCode')
            if not error_code:
                print(f"Success PutObject found! File: {obj['Key']}")
                print(f"UserAgent: {detail.get('userAgent')}")
                print(f"RequestParameters: {detail.get('requestParameters')}")
                print("---")
        except json.JSONDecodeError:
            pass
else:
    print("No PutObject logs found.")
