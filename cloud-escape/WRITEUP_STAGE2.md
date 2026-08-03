<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=40&pause=1000&color=F79211&center=true&vCenter=true&width=800&height=80&lines=Stage+2+Deep+Dive;%22Miss+Me+Yet%3F%22" alt="Typing SVG" />
</div>

## 📋 Challenge Intelligence & Overview

| Field | Value |
|---|---|
| **Challenge** | Miss Me Yet? — Stage 2 |
| **Points** | 150 |
| **Test Site** | `https://d4ysu55xg7wfi.cloudfront.net/` |
| **Execution API** | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| **Target Buckets** | `userd8a2f72fe43094e8` and `logd8a2f72fe43094e8` |
| **Current Status** | Architecture & Versioning Enumeration (In Progress) |

---

## 🔍 Detailed Investigation Steps & Methodology

### Step 1: Reconnaissance & Fuzzing the CloudFront Distribution
Initial exploration of the provided CloudFront distribution (`https://d4ysu55xg7wfi.cloudfront.net/`) revealed the main landing page (`index.html`) featuring an image (`junior_developer.png`) and text claiming that all secret information had been removed.

By fuzzing the endpoint paths, we discovered a hidden documentation page at `/docs.html` which leaked the bucket's IAM Bucket Policy JSON.

<details>
<summary><b>View docs.html (Leaked S3 Bucket Policy)</b></summary>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::userd8a2f72fe43094e8/index.html",
                "arn:aws:s3:::userd8a2f72fe43094e8/docs.html",
                "arn:aws:s3:::userd8a2f72fe43094e8/junior_developer.png",
                "arn:aws:s3:::userd8a2f72fe43094e8"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:UserAgent": "Amazon CloudFront"
                }
            }
        },
        {
            "Sid": "Statement2",
            "Principal": "*",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::userd8a2f72fe43094e8/*",
                "arn:aws:s3:::userd8a2f72fe43094e8"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:SourceVpc": "REDACTED",
                    "aws:UserAgent": "REDACTED"
                }
            }
        }
    ]
}
```
</details>

---

### Step 2: Analyzing `/dev/code_exec` & VPC Security Constraints

We investigated the Python code execution endpoint at `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec`. By submitting base64-encoded Python scripts, we mapped out the runtime constraints:

1. **IAM Identity & Execution Context**:
   - The code runs inside an AWS Lambda function under Account ID `186769093912`.
   - The execution role is an internal Lambda IAM role inside the designated VPC (`aws:SourceVpc` condition in Statement 2 is satisfied when running from within this Lambda).

2. **Outbound Network Isolation (VPC Egress Blocked)**:
   - External HTTP/HTTPS web requests fail because the VPC lacks an attached Internet Gateway or NAT Gateway.
   - Outbound DNS resolution queries (port 53) are blocked.

3. **API Response Masking**:
   - The endpoint suppresses standard stdout/stderr output.
   - Successful execution returns a static response: `{"result": "Code executed successfully"}`.
   - Any raised exception returns a static error: `{"error": "Something went wrong!"}`.

---

### Step 3: Header Injection & Bypassing Statement 1

To interact with `userd8a2f72fe43094e8` using the AWS SDK (`boto3`) inside `/dev/code_exec`, we injected the required `User-Agent: Amazon CloudFront` header using Boto3 event hooks:

```python
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
s3.meta.events.register(
    'before-send.s3.*', 
    lambda request, **kwargs: request.headers.update({'User-Agent': 'Amazon CloudFront'})
)
```

With this header injection in place, standard enumeration (`s3.list_objects_v2`) successfully listed the public assets defined in `Statement1` (`index.html`, `docs.html`, and `junior_developer.png`).

---

### Step 4: Discovery of S3 Server Access Logs (`logd8a2f72fe43094e8`)

Further enumeration revealed a secondary bucket: `logd8a2f72fe43094e8`.
- This bucket is configured as the destination for **S3 Server Access Logs** (and CloudTrail Data Events) for `userd8a2f72fe43094e8`.
- Because our local challenge credentials (`ctf_participant_role`) have read access to this log bucket, we were able to inspect historical access logs in JSON format.
- Parsing these logs allowed us to inspect historical API calls (`GetObject`, `ListObjects`), identity principals (`userIdentity`), and `userAgent` strings used by automated workflows and deployment pipelines.

---

### Step 5: Direct S3 Object Versioning & Delete Marker Discovery

Rather than relying on indirect timing oracles, we tested advanced S3 API calls directly against `userd8a2f72fe43094e8` from within the VPC Lambda execution environment.

We discovered that **S3 Object Versioning** is enabled on `userd8a2f72fe43094e8` and that `s3:ListBucketVersions` is permitted when using valid User-Agent headers:

```python
res = s3.list_object_versions(Bucket='userd8a2f72fe43094e8')
```

#### Key Findings from Versioning Analysis:
1. **Multiple Object Versions**: `userd8a2f72fe43094e8` contains multiple historical versions of `docs.html` and `index.html`.
2. **Delete Markers & Non-Current Keys**: The bucket history contains more than the three current live objects, indicating that previous versions or deleted objects exist in the bucket hierarchy.
3. **Ruling Out False Positives**: Previous assumptions based on indirect timing measurements (such as `022050290014`) were ruled out as false positives.

---

## 🚀 Next Steps & Active Investigation Paths

1. **Enumerate All Version IDs**:
   - Extract and inspect the full list of `Key` names and `VersionId` values returned by `list_object_versions` on `userd8a2f72fe43094e8`.
   - Retrieve historical versions of `docs.html`, `index.html`, and any deleted/non-current keys using `s3.get_object(Bucket=..., Key=..., VersionId=...)`.

2. **Correlate Access Logs with Statement 2**:
   - Cross-reference the historical `userAgent` values discovered in `logd8a2f72fe43094e8` to determine the exact string required by `Statement2` to unlock unrestricted access across all objects in `userd8a2f72fe43094e8/*`.
