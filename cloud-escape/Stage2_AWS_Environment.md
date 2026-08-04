<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=34&duration=2500&pause=900&color=00C7B7&center=true&vCenter=true&width=860&height=85&lines=AWS+Environment+Map;ctf_participant_role+Surface;Allow+%C2%B7+Deny+%C2%B7+Foothold" alt="Typing SVG" />

  <p>
    <img src="https://img.shields.io/badge/ALLOW-5+probes-2EA44F?style=for-the-badge" alt="allow" />
    <img src="https://img.shields.io/badge/DENY-130%2B+probes-red?style=for-the-badge" alt="deny" />
    <img src="https://img.shields.io/badge/Principal-ctf_participant_role-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="role" />
  </p>
</div>

---

> [!IMPORTANT]
> This principal is **intentionally minimal**. Real foothold = **log bucket object read** + **SigV4 code_exec**.  
> Everything else in this account (IAM, EC2, Lambda list, CF control plane, Stage1 buckets) is **denied**.

# AWS environment enumeration
Generated (UTC): 2026-08-04T08:13:12.155897+00:00

## 1. Identity (STS)
```json
{
  "UserId": "AROARYWSMSYIPWMOE25U2:d6d7ee068aa0",
  "Account": "121774052880",
  "Arn": "arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0",
  "ResponseMetadata": {
    "RequestId": "befeeea3-1e4d-47c7-be97-091a558cbe8f",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "x-amzn-requestid": "befeeea3-1e4d-47c7-be97-091a558cbe8f",
      "x-amz-sts-extended-request-id": "MTp1cy1lYXN0LTE6UzoxNzg1ODMxMTkzMDU4OlI6SmZ2eHdKNlk=",
      "content-type": "text/xml",
      "content-length": "451",
      "date": "Tue, 04 Aug 2026 08:13:13 GMT"
    },
    "RetryAttempts": 0
  }
}
```

- **sts.get_caller_identity**: ALLOW
- **sts.get_session_token**: DENY `AccessDenied` — Cannot call GetSessionToken with session credentials
- **sts.assume_role(cicdRole)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: sts:AssumeRole on resource: arn:aws:iam::009661764077:role/cicdRole
- **sts.assume_role(lambdaRole)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: sts:AssumeRole on resource: arn:aws:iam::121774052880:role/lambdaRole

## 2. IAM
- **list_roles**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:ListRoles on resource: arn:aws:iam::121774052880:role/ because no i
- **list_users**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:ListUsers on resource: arn:aws:iam::121774052880:user/ because no i
- **list_policies**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:ListPolicies on resource: policy path / because no identity-based p
- **get_user**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:GetUser on resource: user d6d7ee068aa0 because no identity-based po
- **list_attached_role_policies(ctf_participant_role)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:ListAttachedRolePolicies on resource: role ctf_participant_role bec
- **list_role_policies(ctf_participant_role)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:ListRolePolicies on resource: role ctf_participant_role because no 
- **get_role(ctf_participant_role)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:GetRole on resource: role ctf_participant_role because no identity-
- **simulate principal GetObject**: DENY `InvalidInput` — Invalid ARN provided in the request: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0
- **simulate_principal_policy s3:GetObject user/flag**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: iam:SimulatePrincipalPolicy on resource: arn:aws:iam::121774052880:role

## 3. S3
- **list_buckets**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListAllMyBuckets because no identity-based policy allows the s3:List
### Bucket `userd8a2f72fe43094e8`
- **list_objects_v2**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::userd8a2f72fe43094e8" because 
- **head_bucket**: DENY `403` — Forbidden
- **get_bucket_location**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::userd8a2f72fe43094e8" b
- **get_bucket_policy**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPolicy on resource: "arn:aws:s3:::userd8a2f72fe43094e8" bec
- **get_bucket_acl**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketAcl on resource: "arn:aws:s3:::userd8a2f72fe43094e8" becaus
- **get_bucket_versioning**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketVersioning on resource: "arn:aws:s3:::userd8a2f72fe43094e8"
- **list_object_versions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucketVersions on resource: "arn:aws:s3:::userd8a2f72fe43094e8" 
- **get_public_access_block**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPublicAccessBlock on resource: "arn:aws:s3:::userd8a2f72fe4
- **get_bucket_cors**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketCORS on resource: "arn:aws:s3:::userd8a2f72fe43094e8" becau
- **get_bucket_website**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketWebsite on resource: "arn:aws:s3:::userd8a2f72fe43094e8" be
- **get_bucket_logging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLogging on resource: "arn:aws:s3:::userd8a2f72fe43094e8" be
- **get_bucket_tagging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketTagging on resource: "arn:aws:s3:::userd8a2f72fe43094e8" be
- **get_bucket_encryption**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::userd8a2f72fe4
- **get_bucket_ownership_controls**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketOwnershipControls on resource: "arn:aws:s3:::userd8a2f72fe4
- **get_bucket_notification_configuration**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketNotification on resource: "arn:aws:s3:::userd8a2f72fe43094e
- **get_object(flag.txt)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::userd8a2f72fe43094e8" because 
- **get_object(index.html)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::userd8a2f72fe43094e8" because 
- **head_object(flag.txt)**: DENY `403` — Forbidden

### Bucket `logd8a2f72fe43094e8`
- **list_objects_v2**: ALLOW
- **head_bucket**: ALLOW
- **get_bucket_location**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::logd8a2f72fe43094e8" be
- **get_bucket_policy**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPolicy on resource: "arn:aws:s3:::logd8a2f72fe43094e8" beca
- **get_bucket_acl**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketAcl on resource: "arn:aws:s3:::logd8a2f72fe43094e8" because
- **get_bucket_versioning**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketVersioning on resource: "arn:aws:s3:::logd8a2f72fe43094e8" 
- **list_object_versions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucketVersions on resource: "arn:aws:s3:::logd8a2f72fe43094e8" b
- **get_public_access_block**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPublicAccessBlock on resource: "arn:aws:s3:::logd8a2f72fe43
- **get_bucket_cors**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketCORS on resource: "arn:aws:s3:::logd8a2f72fe43094e8" becaus
- **get_bucket_website**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketWebsite on resource: "arn:aws:s3:::logd8a2f72fe43094e8" bec
- **get_bucket_logging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLogging on resource: "arn:aws:s3:::logd8a2f72fe43094e8" bec
- **get_bucket_tagging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketTagging on resource: "arn:aws:s3:::logd8a2f72fe43094e8" bec
- **get_bucket_encryption**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::logd8a2f72fe43
- **get_bucket_ownership_controls**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketOwnershipControls on resource: "arn:aws:s3:::logd8a2f72fe43
- **get_bucket_notification_configuration**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketNotification on resource: "arn:aws:s3:::logd8a2f72fe43094e8
- **get_object(flag.txt)**: DENY `NoSuchKey` — The specified key does not exist.
- **get_object(index.html)**: DENY `NoSuchKey` — The specified key does not exist.
- **head_object(flag.txt)**: DENY `404` — Not Found

### Bucket `codec4f26c862a321ef5`
- **list_objects_v2**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::codec4f26c862a321ef5" because 
- **head_bucket**: DENY `403` — Forbidden
- **get_bucket_location**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::codec4f26c862a321ef5" b
- **get_bucket_policy**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPolicy on resource: "arn:aws:s3:::codec4f26c862a321ef5" bec
- **get_bucket_acl**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketAcl on resource: "arn:aws:s3:::codec4f26c862a321ef5" becaus
- **get_bucket_versioning**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketVersioning on resource: "arn:aws:s3:::codec4f26c862a321ef5"
- **list_object_versions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucketVersions on resource: "arn:aws:s3:::codec4f26c862a321ef5" 
- **get_public_access_block**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPublicAccessBlock on resource: "arn:aws:s3:::codec4f26c862a
- **get_bucket_cors**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketCORS on resource: "arn:aws:s3:::codec4f26c862a321ef5" becau
- **get_bucket_website**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketWebsite on resource: "arn:aws:s3:::codec4f26c862a321ef5" be
- **get_bucket_logging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLogging on resource: "arn:aws:s3:::codec4f26c862a321ef5" be
- **get_bucket_tagging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketTagging on resource: "arn:aws:s3:::codec4f26c862a321ef5" be
- **get_bucket_encryption**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::codec4f26c862a
- **get_bucket_ownership_controls**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketOwnershipControls on resource: "arn:aws:s3:::codec4f26c862a
- **get_bucket_notification_configuration**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketNotification on resource: "arn:aws:s3:::codec4f26c862a321ef
- **get_object(flag.txt)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetObject on resource: "arn:aws:s3:::codec4f26c862a321ef5/flag.txt" 
- **get_object(index.html)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::codec4f26c862a321ef5" because 
- **head_object(flag.txt)**: DENY `403` — Forbidden

### Bucket `platform-bucket-009661764077-us-east-1`
- **list_objects_v2**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::platform-bucket-009661764077-u
- **head_bucket**: DENY `403` — Forbidden
- **get_bucket_location**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::platform-bucket-0096617
- **get_bucket_policy**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPolicy on resource: "arn:aws:s3:::platform-bucket-009661764
- **get_bucket_acl**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketAcl on resource: "arn:aws:s3:::platform-bucket-009661764077
- **get_bucket_versioning**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketVersioning on resource: "arn:aws:s3:::platform-bucket-00966
- **list_object_versions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucketVersions on resource: "arn:aws:s3:::platform-bucket-009661
- **get_public_access_block**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPublicAccessBlock on resource: "arn:aws:s3:::platform-bucke
- **get_bucket_cors**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketCORS on resource: "arn:aws:s3:::platform-bucket-00966176407
- **get_bucket_website**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketWebsite on resource: "arn:aws:s3:::platform-bucket-00966176
- **get_bucket_logging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLogging on resource: "arn:aws:s3:::platform-bucket-00966176
- **get_bucket_tagging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketTagging on resource: "arn:aws:s3:::platform-bucket-00966176
- **get_bucket_encryption**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::platform-bucke
- **get_bucket_ownership_controls**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketOwnershipControls on resource: "arn:aws:s3:::platform-bucke
- **get_bucket_notification_configuration**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketNotification on resource: "arn:aws:s3:::platform-bucket-009
- **get_object(flag.txt)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::platform-bucket-009661764077-u
- **get_object(index.html)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::platform-bucket-009661764077-u
- **head_object(flag.txt)**: DENY `403` — Forbidden

### Bucket `site781fe43f26b9eba3`
- **list_objects_v2**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::site781fe43f26b9eba3" because 
- **head_bucket**: DENY `403` — Forbidden
- **get_bucket_location**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::site781fe43f26b9eba3" b
- **get_bucket_policy**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPolicy on resource: "arn:aws:s3:::site781fe43f26b9eba3" bec
- **get_bucket_acl**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketAcl on resource: "arn:aws:s3:::site781fe43f26b9eba3" becaus
- **get_bucket_versioning**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketVersioning on resource: "arn:aws:s3:::site781fe43f26b9eba3"
- **list_object_versions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucketVersions on resource: "arn:aws:s3:::site781fe43f26b9eba3" 
- **get_public_access_block**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketPublicAccessBlock on resource: "arn:aws:s3:::site781fe43f26
- **get_bucket_cors**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketCORS on resource: "arn:aws:s3:::site781fe43f26b9eba3" becau
- **get_bucket_website**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketWebsite on resource: "arn:aws:s3:::site781fe43f26b9eba3" be
- **get_bucket_logging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketLogging on resource: "arn:aws:s3:::site781fe43f26b9eba3" be
- **get_bucket_tagging**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketTagging on resource: "arn:aws:s3:::site781fe43f26b9eba3" be
- **get_bucket_encryption**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::site781fe43f26
- **get_bucket_ownership_controls**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketOwnershipControls on resource: "arn:aws:s3:::site781fe43f26
- **get_bucket_notification_configuration**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetBucketNotification on resource: "arn:aws:s3:::site781fe43f26b9eba
- **get_object(flag.txt)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::site781fe43f26b9eba3" because 
- **get_object(index.html)**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: s3:GetObject on resource: "arn:aws:s3:::site781fe43f26b9eba3/index.html
- **head_object(flag.txt)**: DENY `403` — Forbidden

### Log bucket deep list (prefixes)
- **list delimiter /**: ALLOW
  - prefix `userd8a2f72fe43094e8/`
- **  list userd8a2f72fe43094e8/ delimiter**: ALLOW
    - `userd8a2f72fe43094e8/CopyObject/`
    - `userd8a2f72fe43094e8/GetObject/`
    - `userd8a2f72fe43094e8/GetObjectAcl/`
    - `userd8a2f72fe43094e8/GetObjectAttributes/`
    - `userd8a2f72fe43094e8/GetObjectTagging/`
    - `userd8a2f72fe43094e8/HeadBucket/`
    - `userd8a2f72fe43094e8/HeadObject/`
    - `userd8a2f72fe43094e8/ListObjectVersions/`
    - `userd8a2f72fe43094e8/ListObjects/`
    - `userd8a2f72fe43094e8/PutObject/`
    - `userd8a2f72fe43094e8/RestoreObject/`
    - `userd8a2f72fe43094e8/SelectObjectContent/`

## 4. Lambda
- **list_functions**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: lambda:ListFunctions on resource: * because no identity-based policy al

## 5. API Gateway
- **apigateway.get_rest_apis**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: apigateway:GET on resource: arn:aws:apigateway:us-east-1::/restapis bec
- **apigatewayv2.get_apis**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: apigateway:GET on resource: arn:aws:apigateway:us-east-1::/apis because

## 6. EC2 / VPC / networking
- **describe_vpcs**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeVpcs beca
- **describe_subnets**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeSubnets b
- **describe_security_groups**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeSecurityG
- **describe_instances**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeInstances
- **describe_vpc_endpoints**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeVpcEndpoi
- **describe_route_tables**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeRouteTabl
- **describe_nat_gateways**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeNatGatewa
- **describe_internet_gateways**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeInternetG
- **describe_network_interfaces**: DENY `UnauthorizedOperation` — You are not authorized to perform this operation. User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ec2:DescribeNetworkIn

## 7. CloudFront
- **list_distributions**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: cloudfront:ListDistributions because no identity-based policy allows th

## 8. Other services (smoke)
- **ssm.describe_parameters**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ssm:DescribeParameters on resource: arn:aws:ssm:us-east-1:121774052880:
- **ssm.describe_instance_information**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ssm:DescribeInstanceInformation on resource: arn:aws:ssm:us-east-1:1217
- **secretsmanager.list_secrets**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: secretsmanager:ListSecrets because no identity-based policy allows the 
- **kms.list_keys**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: kms:ListKeys on resource: * because no identity-based policy allows the
- **dynamodb.list_tables**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: dynamodb:ListTables on resource: arn:aws:dynamodb:us-east-1:12177405288
- **rds.describe_db_instances**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: rds:DescribeDBInstances on resource: arn:aws:rds:us-east-1:121774052880
- **ecs.list_clusters**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ecs:ListClusters on resource: * because no identity-based policy allows
- **eks.list_clusters**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: eks:ListClusters on resource: arn:aws:eks:us-east-1:121774052880:cluste
- **ecr.describe_repositories**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: ecr:DescribeRepositories on resource: arn:aws:ecr:us-east-1:12177405288
- **sns.list_topics**: DENY `AuthorizationError` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: SNS:ListTopics on resource: arn:aws:sns:us-east-1:121774052880:* becaus
- **sqs.list_queues**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: sqs:listqueues on resource: arn:aws:sqs:us-east-1:121774052880: because
- **events.list_event_buses**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: events:ListEventBuses on resource: arn:aws:events:us-east-1:12177405288
- **logs.describe_log_groups**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: logs:DescribeLogGroups on resource: arn:aws:logs:us-east-1:121774052880
- **cloudtrail.describe_trails**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: cloudtrail:DescribeTrails because no identity-based policy allows the c
- **cloudformation.list_stacks**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: cloudformation:ListStacks on resource: arn:aws:cloudformation:us-east-1
- **codebuild.list_projects**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: codebuild:ListProjects because no identity-based policy allows the code
- **codepipeline.list_pipelines**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: codepipeline:ListPipelines on resource: arn:aws:codepipeline:us-east-1:
- **cognito-idp.list_user_pools**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: cognito-idp:ListUserPools on resource: * because no identity-based poli
- **cognito-identity.list_identity_pools**: DENY `AccessDeniedException` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: cognito-identity:ListIdentityPools on resource: arn:aws:cognito-identit
- **sts.get_access_key_info**: DENY `AccessDenied` — User: arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0 is not authorized to perform: sts:GetAccessKeyInfo because no identity-based policy allows the sts:Ge

## 9. Known Stage assets (challenge briefing)
| Asset | Value |
|---|---|
| code_exec API | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| test site (CF) | `https://d4ysu55xg7wfi.cloudfront.net/` |
| user bucket | `userd8a2f72fe43094e8` |
| log bucket | `logd8a2f72fe43094e8` |
| Stage1 API (historical) | `https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookupv2` |
| Stage1 cicdRole | `arn:aws:iam::009661764077:role/cicdRole` |

## 10. Summary — what this principal can do
- ALLOW count (probe lines): **5**
- DENY count (probe lines): **134**

### High-value ALLOWs
- **sts.get_caller_identity**: ALLOW
- **list_objects_v2**: ALLOW
- **head_bucket**: ALLOW
- **list delimiter /**: ALLOW
- **  list userd8a2f72fe43094e8/ delimiter**: ALLOW

### Notes
- Participant is designed for Stage 2 foothold: log-bucket read + execute-api to code_exec (invoke tested separately with SigV4).
- cicdRole (Stage 1 GHA) cannot invoke Stage 2 code_exec API (confirmed in GHA run).
- Full exploit still centers on code_exec in VPC + path-style S3 + bucket policy conditions.
