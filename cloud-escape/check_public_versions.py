import boto3

s3 = boto3.client('s3')
public_bucket = "publicd8a2f72fe43094e8"

try:
    # Use unauthenticated request
    from botocore import UNSIGNED
    from botocore.config import Config
    s3_unauth = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    response = s3_unauth.list_object_versions(Bucket=public_bucket)
    print("SUCCESS")
    versions = response.get('Versions', [])
    for v in versions:
        print(f"{v['Key']} ({v['VersionId']})")
    
except Exception as e:
    print("FAILED:", e)
