import boto3
import json
import concurrent.futures

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYIOLOPQDID",
    aws_secret_access_key="fzVE7H2+LqCvSNDLNzb1qS7oNEgVmwUm6T4ykuhq",
    aws_session_token="IQoJb3JpZ2luX2VjELf//////////wEaDGlsLWNlbnRyYWwtMSJIMEYCIQDbv8K6aDIK9hgYAX96Cy3KWnf1nV6CK4zSOHtFYxRSzwIhAO6mXPFjyZd+6TRZsMIwtXohzOCURYNPdJqLl/uzdiyQKrUCCCQQABoMMTIxNzc0MDUyODgwIgwgxonHTHHAlDodO9wqkgJx7w+jK4uqQZAWDUqG7wlZ0IGc+cypxmsZ2PuPd1TWtwFF4Vv0MaCadKDdi49HdvpTY7KA+FQDtpJWBk2gmHkf9xpvMK4F5py+qG0lY7UalW/0OBGBfU2xb7YGzxmZF9w2TpqAj7HBEP07bhqST0ViU2ODIvf+5NMbDHYnhoOsYk2E1OPadWGQrakz6poU2+kTlvpA0bNCpR8sVZ6nz7FddcgJJmREMSdYMr+WJ3L3GNbiXihQT6Bzf1+IyItX7pgfhD2xpRSTFuePD9PeWMr3ASGt8ZSaOQDNBORnDUytLPGAYwBFdQZpl30pBnHA8vUZFFiRDdNNMs/HmHBH1dpN+yVtCNn/QnibHS2z6kA+n2OsMIOjzNMGOpwBypSEq9f7dXcHc58gHPJwbsnXkYmhe3joODue97MM0EHT9q1Ts6mkhrhJkvcIFPIlIwa6dYuWLiKxkbh80fSCOYuEHmzqkrynYFofo/BOxZ93fx1HlLeZji+uXDVLq8Z4kVuUu5DMkOKqvoFFPtZmFneh8sbN3NBvBPxgFD+KoLEuLJJzmYmg0zLO/cCE8VaNNVrVtIGQGJw6FVw1",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"
prefix = "userd8a2f72fe43094e8/GetObject/"

def check_log(key):
    try:
        log_obj = s3.get_object(Bucket=log_bucket, Key=key)
        log_content = log_obj['Body'].read().decode('utf-8')
        log_data = json.loads(log_content)
        detail = log_data.get('detail', {})
        req_key = detail.get('requestParameters', {}).get('key', '')
        error_code = detail.get('errorCode', '')
        user_agent = detail.get('userAgent', '')
        
        # If it's a success, or if it's NOT index.html (maybe flag.txt?)
        if error_code == '' or error_code is None or req_key == 'flag.txt':
            print(f"FOUND! [{error_code}] Key: {req_key} -> UserAgent: {user_agent}", flush=True)
            return True
    except Exception as e:
        pass
    return False

print("Fetching list of all logs...", flush=True)
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=log_bucket, Prefix=prefix)

keys = []
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            keys.append(obj['Key'])

print(f"Total keys: {len(keys)}. Starting parallel processing...", flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Submit all keys
    futures = {executor.submit(check_log, key): key for key in keys}
    
    count = 0
    for future in concurrent.futures.as_completed(futures):
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count}/{len(keys)}", flush=True)
        if future.result():
            print("Found a match! Continuing to search though...", flush=True)

print("Done checking all logs.", flush=True)
