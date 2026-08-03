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

---

## 🔍 The Reconnaissance Process

### 1. Fuzzing the CloudFront Test Site
The challenge intelligence provided a CloudFront distribution URL. Manual inspection showed a basic webpage. We utilized directory busting tools to fuzz the endpoints and discovered a hidden `/docs.html` file.

### 2. The Policy Leak
The `/docs.html` file inadvertently leaked the raw S3 Bucket Policy. 
The policy stated that `s3:GetObject` was allowed ONLY IF:
1. The request came from the specific VPC.
2. The request contained the `User-Agent: Amazon CloudFront` header.

<details>
<summary><b>View docs.html (Bucket Policy Leak)</b></summary>

```json
System Documentation
This is the bucket_policy.json I applied to this site.
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
                "arn:aws:s3:::REDACTED/index.html",
                "arn:aws:s3:::REDACTED/docs.html",
                "arn:aws:s3:::REDACTED/junior_developer.png",
                "arn:aws:s3:::REDACTED"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:UserAgent": REDACTED
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
                "arn:aws:s3:::REDACTED/*",
                "arn:aws:s3:::REDACTED"
			],
            "Condition": {
                "StringEquals": {
                    "aws:SourceVpc": REDACTED,
                    "aws:UserAgent": REDACTED
                }
            }
        }
    ]
}
End of file.
```
</details>

---

## ⚙️ Running the Exploit via GitHub Actions

We integrated our Stage 2 payloads into the GitHub Actions CI/CD pipeline located at `.github/workflows/stage2.yml`.

**How to run this yourself:**
1. Navigate to the **Actions** tab in this repository.
2. Select the **Cloud Escape - Stage 2 (Miss Me Yet?)** workflow.
3. Click **Run workflow**. 
4. The runner will invoke the `/dev/code_exec` endpoint with our Base64-encoded Python payloads, testing the timing boundaries against the buckets.

---

## ⏱️ The Timing Oracle & Header Injection

We interacted with the `/dev/code_exec` API which executed code via `exec()`. To bypass the S3 policy and access the internal buckets, we injected the required header into the internal `boto3` client:

```python
s3.meta.events.register('before-send.s3.*', lambda request, **kwargs: request.headers.update({'User-Agent': 'Amazon CloudFront'}))
```

Because the API swallowed all output, we created a **Timing Oracle**. By measuring the HTTP response time of the API Gateway, we could infer if a character guess was correct on the `logd8a2f72fe43094e8` bucket:

```python
if flag[pos] == guess:
    time.sleep(2.0)
```

We iterated through the flag locally using a multi-threaded Python script.

> **Stage 2 Flag Captured:** 🟢 *00000000000000000000*
