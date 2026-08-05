import os
import json
import boto3
from datetime import datetime, timezone, timedelta

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYINWI54QUF",
    aws_secret_access_key="vzoDaHLWP97VayPQRZpwLhu9+wucg+FdyJbsgKBQ",
    aws_session_token="IQoJb3JpZ2luX2VjELX//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCICgyqloerkVTXTE5628Kp386BsQLYbXsQC4+rOu6I0INAiALeJaaL7isClSF+8qxnBZHA9Hk+WTg7zcTBxBBIzGtyiq1AggiEAAaDDEyMTc3NDA1Mjg4MCIM+Rpw/jafiBZf85MDKpICyLS9DUhUvWvbZ96LLt/M2kRPwKA2Cz68ISWVyBt/A7mKpJ0/E0HNdzCBZod2V2B2A+e2pm7A0yd/0pcb4t7MErEMgPBMoIzOywtMhleclfugWQqI52Do/aUoiR3cPNfBXutl/fYMykNSRZIkU+r1RywE1Yy3nbDy9zGpa2tfXU5plezMGPO15sxKYFz6PClI98LayWhEiEl89hTv5oAdzK+O3ONrp2TM8IyZf7G3eA3t9BP1Kl19E/NtsNZkQCYQwIbOMgRbAkQMvZCBKXilYo1GUVQvrGmeoyZq3LGOgj9o9bxa5jV+Kg4TSRTdL5R0yqeQrhiq3uJBh3ybX+8lnKs+auiOvaava6lGaGyL5KdwXzCu58vTBjqeARTzARMyhUPkGpGGVOScggiv11wG1cCI039vSFoWRPBrCt2Kt1K6+sJqTm4Jxbkg0A0ca6yLHbGxCkq6f3nrdRfuDiBVACtArW8jBjgxp+saXsdfHpS6xTaGTGk8kSE7PBtzeSYzug2gmQdMjL1+LlotY2UVvcIft1FSc8YxPWu62NeRcPyGJMkbHLS/6VJcRAhPg/Vnbx9m/gkhpvl7",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"

prefix = "userd8a2f72fe43094e8/GetObject/"
today = datetime.now(timezone.utc)
last_hours = today - timedelta(hours=2)
start_after = f"{prefix}{last_hours.strftime('%Y-%m-%d-%H')}"
print(f"Checking {prefix} logs starting after: {start_after}")

found_data = {}

response = s3.list_objects_v2(Bucket=log_bucket, Prefix=prefix, StartAfter=start_after)
if 'Contents' in response:
    sorted_objs = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    for obj in sorted_objs[:200]: 
        log_obj = s3.get_object(Bucket=log_bucket, Key=obj['Key'])
        log_content = log_obj['Body'].read().decode('utf-8')
        try:
            log_data = json.loads(log_content)
            # Both forms
            ua = log_data.get('userAgent')
            if not ua:
                detail = log_data.get('detail', {})
                ua = detail.get('userAgent')
            
            if ua and "TASK" in ua and "-" in ua:
                # expecting TASK<id>-<chunk_idx>-<chunk_data>
                parts = ua.split('-')
                if len(parts) >= 3:
                    marker_type = parts[0]
                    try:
                        idx = int(parts[1])
                        chunk = parts[2]
                        if marker_type not in found_data:
                            found_data[marker_type] = {}
                        found_data[marker_type][idx] = chunk
                        print(f"Got {marker_type} chunk {idx}: {chunk}")
                    except ValueError:
                        pass
        except json.JSONDecodeError:
            pass
            
for marker_type, chunks in found_data.items():
    import base64
    sorted_chunks = [chunks[k] for k in sorted(chunks.keys())]
    full_b32 = "".join(sorted_chunks)
    print(f"\n{marker_type} Full base32:", full_b32[:50], "...")
    try:
        padding = len(full_b32) % 8
        if padding:
            full_b32 += "=" * (8 - padding)
        decoded = base64.b32decode(full_b32).decode()
        print(f"\nDecoded {marker_type}:")
        print(decoded)
    except Exception as e:
        print("Decode error:", e)

if not found_data:
    print("No markers found in latest logs.")
