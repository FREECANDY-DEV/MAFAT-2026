import boto3
import gzip
import json
import os

s3 = boto3.client('s3')
bucket = 'logd8a2f72fe43094e8'

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='userd8a2f72fe43094e8/GetObject/')

uas = set()

for page in pages:
    if 'Contents' not in page:
        continue
    for obj in page['Contents']:
        key = obj['Key']
        resp = s3.get_object(Bucket=bucket, Key=key)
        body = resp['Body'].read()
        
        # Some trails are gzipped, some are plain JSON. Let's try parsing.
        try:
            if key.endswith('.gz'):
                data = gzip.decompress(body)
            else:
                data = body
            
            # S3 server access logs or CloudTrail data events? 
            # From earlier we saw CloudTrail data events (JSON)
            lines = data.decode('utf-8').strip().split('\n')
            for line in lines:
                if not line.strip(): continue
                record = json.loads(line)
                
                # S3 data event or single record
                if 'Records' in record:
                    recs = record['Records']
                else:
                    recs = [record]
                
                for r in recs:
                    if 'userAgent' in r:
                        ua = r['userAgent']
                        req_params = r.get('requestParameters', {})
                        s3_key = req_params.get('key', '')
                        if s3_key in ['index.html', 'docs.html', 'junior_developer.png']:
                            uas.add(ua)
                            print(f"Found UA for {s3_key}: {ua}")
        except Exception as e:
            print(f"Error parsing {key}: {e}")

print("Unique UAs found:")
for ua in uas:
    print(ua)
