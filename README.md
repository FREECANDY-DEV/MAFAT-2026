<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=42&pause=1000&color=F79211&center=true&vCenter=true&width=800&height=85&lines=AWS+Cloud+Escape+CTF+2026;Master+Security+Writeup;Operation+%22Miss+Me+Yet%3F%22" alt="Typing SVG" />

  <p align="center">
    <img src="https://img.shields.io/badge/AWS-us--east--1-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Region" />
    <img src="https://img.shields.io/badge/Service-IAM%20%7C%20Lambda%20%7C%20S3%20%7C%20API%20Gateway-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS Services" />
    <img src="https://img.shields.io/badge/Category-Cloud%20Security%20%7C%20OIDC%20%26%20IAM-F79211?style=for-the-badge" alt="Category" />
    <img src="https://img.shields.io/badge/Total%20Points-300%20PTS-00C7B7?style=for-the-badge" alt="Points" />
    <img src="https://img.shields.io/badge/Status-Methodology%20Verified-2EA44F?style=for-the-badge" alt="Status" />
  </p>
</div>

---

## 🎯 Executive Summary & Official Submission

> [!IMPORTANT]  
> **Campaign Overview:** This repository serves as the official security submission for the **Cloud Escape CTF 2026**. It documents the complete exploitation lifecycle, architectural mapping, and step-by-step methodologies used to penetrate a hardened AWS serverless environment across two challenge stages.

<table>
  <thead>
    <tr>
      <th width="120">Stage</th>
      <th width="200">Challenge Name</th>
      <th width="120">Points</th>
      <th width="240">Core Technique</th>
      <th width="320">Detailed Writeup Documentation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Stage 1</code></td>
      <td><strong>"Have Some Faith"</strong></td>
      <td><strong>100 PTS</strong></td>
      <td>OIDC Wildcard & DNS Tunneling</td>
      <td>📄 <a href="cloud-escape/Stage_1_Have_Some_Faith.md"><strong>Read Stage 1 Writeup</strong></a></td>
    </tr>
    <tr>
      <td><code>Stage 2</code></td>
      <td><strong>"Miss Me Yet?"</strong></td>
      <td><strong>200 PTS</strong></td>
      <td>Header Injection & S3 Versioning</td>
      <td>📄 <a href="cloud-escape/Stage_2_Miss_Me_Yet.md"><strong>Read Stage 2 Writeup</strong></a></td>
    </tr>
  </tbody>
</table>

---

## 🗺️ Master Architectural Threat Model

The following Mermaid diagram illustrates the AWS infrastructure across both challenge stages:

```mermaid
graph TD
    A["GitHub Actions: corgi branch"]
    B["AWS IAM OIDC Provider"]
    C["cicdRole Account: 009661764077"]
    D["API Gateway: /dev/nslookupv2 Stage 1"]
    E["API Gateway: /dev/code_exec Stage 2"]

    subgraph VPC_Stage1 ["VPC Stage 1: Route 53 DNS Resolver Enabled"]
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

## 📂 Documentation Directory & Writeups

- 🛡️ **[Writeups index](cloud-escape/README.md)** · **[Combined summary](cloud-escape/WRITEUP.md)**
- 🟢 **[Stage 1: "Have Some Faith" (100 Points)](cloud-escape/Stage_1_Have_Some_Faith.md)**: Single detailed writeup — Git forensics, OIDC wildcard, `nslookupv2` injection, Route 53 DNS exfil (`1a1jelrlfg2yi2s0`).
- 🔍 **[Stage 2: "Miss Me Yet?" (200 Points)](cloud-escape/Stage_2_Miss_Me_Yet.md)**: Single detailed writeup — CloudFront `/docs.html` policy, code_exec sandbox, UA/VPC conditions, log forensics, versioning, oracles.

---

<div align="center">
  <sub>🛡️ Documented by <b>Agent freecandy</b> • Cloud Escape CTF 2026 • Advanced Cloud Infrastructure Security</sub>
</div>
