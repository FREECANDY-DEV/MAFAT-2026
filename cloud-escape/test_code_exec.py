import urllib.request, urllib.error, json, os, base64, time
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

API = 'https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec'
creds = Credentials(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], os.environ['AWS_SESSION_TOKEN'])

def exec_code(code):
    b64 = base64.b64encode(code.encode()).decode()
    payload = json.dumps({'code': b64})
    r0 = AWSRequest(method='POST', url=API, data=payload, headers={'Content-Type': 'application/json'})
    SigV4Auth(creds, 'execute-api', 'us-east-1').add_auth(r0)
    req = urllib.request.Request(API, data=payload.encode(), headers=dict(r0.headers), method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as r: return r.read().decode().strip()
    except Exception as e:
        return str(e)

code = '''
import urllib.request
import urllib.error
USER = "userd8a2f72fe43094e8"
FLAG_KEY = "flag.txt"
PATH_URL = f"https://s3.us-east-1.amazonaws.com/{USER}/{FLAG_KEY}"
ua = "squished_bug_exfil"
req = urllib.request.Request(PATH_URL, headers={"User-Agent": ua})
try:
    urllib.request.urlopen(req, timeout=5)
    assert False
except Exception as e:
    assert True
'''
print(exec_code(code))
