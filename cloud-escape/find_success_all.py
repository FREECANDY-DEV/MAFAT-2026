import boto3
import json
import concurrent.futures

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYIIWK4BEMG",
    aws_secret_access_key="yQXeKSwcKm2sMkj34DVhMhzMAQ/U+U1en5S4xmsd",
    aws_session_token="IQoJb3JpZ2luX2VjELj//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDF7JGpYPE2Awtt7TrTdowno6OzcS1UBLm1VG22edZvjAiAv6CKYlLqEA5XGHTjHC7Zd31GU07fTZIRT5h7wSS8G/Cq1AgglEAAaDDEyMTc3NDA1Mjg4MCIM8Ws5xRwIAZJyZCjjKpICTQVLdf5ZWWgYfpiwvtdLAL0/+M0Ni6LskzqCorBijcWaC1N3cRkuqy3kc12VA7NtjK/D7SCZmtYRDNt5pbZnvg48BZqtjY8gr0EMWKU0Y3ihq4VRkG9Ey73csFLx+gsgxkvyK6Bv9O4tVKZbTVrQ305DcAKTL2zpTB86uM9TGG/Y7D72CqrKLYPlYl2n2QK1Wyc46WaM/CakboW6J9IxNlIVGymn6hm1gdxC/nk7YShxnCg9Kh3rPwquB0axT85cSeVOVX3a6quCb1+fVY5PT4flf4y216WIRqyPDFywpQVxEC769cf/4zu6LOKWbTPaK18wFRu+XXVw/XbkPE+dBb9MqbtaP4tKSD6rmD5fqCrlwDCCw8zTBjqeAcYMGqS2qPpmzSR6yQkw5yPW14q0kin4++AZfBFJS0gZta7D90stYQPFM0+OsMz1yqfueBMihYUxZblCv2kj5nQLpPMPSMSx9gL/PKZtTO5+fRdOMtkjPWsdF3Z6O+Y37DDagfhoUmrMUoBTWBZLdenZp00N2Wb9oGwCMq1oRYjVnqoQjNABxqiaRSP/m1T1LN5hFw7DBYkgkvIQ1DVT",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"
prefix = "userd8a2f72fe43094e8/GetObject/"

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=log_bucket, Prefix=prefix)

keys = []
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            keys.append(obj['Key'])

print(f"Total logs: {len(keys)}. Scanning for SUCCESS...")

def process_key(key):
    try:
        log_obj = s3.get_object(Bucket=log_bucket, Key=key)
        log_content = log_obj['Body'].read().decode('utf-8')
        log_data = json.loads(log_content)
        detail = log_data.get('detail', {})
        req_key = detail.get('requestParameters', {}).get('key', '')
        if req_key == 'flag.txt':
            err = detail.get('errorCode', '')
            if not err:
                return log_content
    except Exception as e:
        pass
    return None

found_success = []
processed = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(process_key, key): key for key in keys}
    for future in concurrent.futures.as_completed(futures):
        processed += 1
        if processed % 5000 == 0:
            print(f"Processed {processed}/{len(keys)}")
        res = future.result()
        if res:
            found_success.append(res)
            print(f"\n[!!!] FOUND SUCCESS: {res}\n")

print(f"Done. Found {len(found_success)} successes.")
