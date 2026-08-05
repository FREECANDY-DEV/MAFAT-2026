import boto3

session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYIOLOPQDID",
    aws_secret_access_key="fzVE7H2+LqCvSNDLNzb1qS7oNEgVmwUm6T4ykuhq",
    aws_session_token="IQoJb3JpZ2luX2VjELf//////////wEaDGlsLWNlbnRyYWwtMSJIMEYCIQDbv8K6aDIK9hgYAX96Cy3KWnf1nV6CK4zSOHtFYxRSzwIhAO6mXPFjyZd+6TRZsMIwtXohzOCURYNPdJqLl/uzdiyQKrUCCCQQABoMMTIxNzc0MDUyODgwIgwgxonHTHHAlDodO9wqkgJx7w+jK4uqQZAWDUqG7wlZ0IGc+cypxmsZ2PuPd1TWtwFF4Vv0MaCadKDdi49HdvpTY7KA+FQDtpJWBk2gmHkf9xpvMK4F5py+qG0lY7UalW/0OBGBfU2xb7YGzxmZF9w2TpqAj7HBEP07bhqST0ViU2ODIvf+5NMbDHYnhoOsYk2E1OPadWGQrakz6poU2+kTlvpA0bNCpR8sVZ6nz7FddcgJJmREMSdYMr+WJ3L3GNbiXihQT6Bzf1+IyItX7pgfhD2xpRSTFuePD9PeWMr3ASGt8ZSaOQDNBORnDUytLPGAYwBFdQZpl30pBnHA8vUZFFiRDdNNMs/HmHBH1dpN+yVtCNn/QnibHS2z6kA+n2OsMIOjzNMGOpwBypSEq9f7dXcHc58gHPJwbsnXkYmhe3joODue97MM0EHT9q1Ts6mkhrhJkvcIFPIlIwa6dYuWLiKxkbh80fSCOYuEHmzqkrynYFofo/BOxZ93fx1HlLeZji+uXDVLq8Z4kVuUu5DMkOKqvoFFPtZmFneh8sbN3NBvBPxgFD+KoLEuLJJzmYmg0zLO/cCE8VaNNVrVtIGQGJw6FVw1",
    region_name="us-east-1"
)
s3 = session.client('s3')
log_bucket = "logd8a2f72fe43094e8"

response = s3.list_objects_v2(Bucket=log_bucket, Prefix="userd8a2f72fe43094e8/", Delimiter="/")
print("Prefixes under userd8a2f72fe43094e8/:")
for prefix in response.get('CommonPrefixes', []):
    print(prefix.get('Prefix'))
