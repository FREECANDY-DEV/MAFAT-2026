<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=40&pause=1000&color=F71111&center=true&vCenter=true&width=800&height=80&lines=%E2%98%81%EF%B8%8F+Cloud+Escape+CTF+2026;Operation+%22Miss+Me+Yet%3F%22;Full+Writeup+by+Agent+freecandy" alt="Typing SVG" />
</div>

<div align="center">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />
  <img src="https://img.shields.io/badge/CTF-Hacking-FF0000?style=for-the-badge&logo=hackthebox&logoColor=white" />
</div>

<br/>

<details open>
<summary><h2> 📖 Executive Summary </h2></summary>

Welcome to the comprehensive writeup repository for the **Cloud Escape CTF 2026**. This repository contains the complete exploitation lifecycle, methodologies, and scripts used to compromise a heavily restricted AWS infrastructure across two complex stages.

Our objective was to navigate through a deeply isolated Virtual Private Cloud (VPC), bypass strict Identity and Access Management (IAM) controls, and exfiltrate highly sensitive data without standard internet egress.
</details>

---

## 🏆 Captured Flags

| Stage | Challenge Name | Difficulty | Status | Flag |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Have Some Faith | <img src="https://img.shields.io/badge/High-FF0000?style=flat-square" /> | 🟢 **COMPLETED** | `1a1jelrlfg2yi2s0` |
| **2** | Miss Me Yet? | <img src="https://img.shields.io/badge/Critical-8B0000?style=flat-square" /> | 🟡 **IN PROGRESS** | *[ANALYZING ORACLE DATA]* |

---

## 🏗️ Attack Architecture & Methodologies

The CTF environment was designed to prevent standard data exfiltration. The target Lambda functions were placed inside a VPC with **no NAT Gateway** (no outbound internet) and highly restrictive IAM policies. 

To succeed, we engineered advanced side-channel attacks.

### <img src="https://img.shields.io/badge/Stage_1-DNS_Exfiltration-blue?style=for-the-badge" />

By exploiting a GitHub OIDC trust misconfiguration and a Lambda command injection vulnerability, we gained Remote Code Execution (RCE). We bypassed the internet blockade by forcing the Lambda to resolve a custom DNS subdomain containing the hex-encoded flag via the AWS Route 53 VPC Resolver.

```mermaid
graph LR
    A[GitHub Actions] -->|AssumeRole| B(cicdRole)
    B -->|POST Inject| C[API Gateway]
    C --> D[Lambda]
    D -->|Read| E[(S3 Bucket)]
    D -->|DNS Query| F[VPC Resolver]
    F -->|Extract| G[Attacker DNS]
    style A fill:#24292e,color:#fff
    style D fill:#f90,color:#fff
    style E fill:#3b82f6,color:#fff
```

### <img src="https://img.shields.io/badge/Stage_2-Timing_Oracle-orange?style=for-the-badge" />

Facing an arbitrary code execution endpoint (`exec()`) that swallowed all `stdout` and exceptions, we bypassed an S3 Bucket Policy by spoofing the `aws:UserAgent` using `boto3` event hooks. We are currently developing a multi-threaded blind timing oracle (`time.sleep()`) to exfiltrate the flag character-by-character based on API response latency. So far, we have mapped out the capability to inject headers and verified the timing discrepancies.

```mermaid
graph LR
    A[Attacker] -->|Base64 Payload| B[API Gateway]
    B -->|exec()| C[Lambda]
    C -.->|Spoof User-Agent| D[boto3]
    D -->|Read Flag| E[(Test Site S3)]
    C -->|time.sleep()| C
    C -->|Latency Output| A
    style A fill:#ef4444,color:#fff
    style C fill:#f90,color:#fff
    style E fill:#3b82f6,color:#fff
```

---

## 📂 Documentation Directory

Dive into the highly detailed, step-by-step methodologies for each stage:

* 🛡️ **[Combined Technical Overview](cloud-escape/WRITEUP.md)**: A master document detailing the full attack narrative.
* 🚀 **[Stage 1 Deep Dive](cloud-escape/WRITEUP_STAGE1.md)**: OIDC exploitation, recon, and DNS side-channel payloads.
* ⏱️ **[Stage 2 Deep Dive](cloud-escape/WRITEUP_STAGE2.md)**: CloudFront policy analysis, header injection, and the timing oracle (WIP).

---
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=400&size=20&pause=2000&color=888888&center=true&vCenter=true&width=600&height=50&lines=%22In+the+cloud,+there+is+no+such+thing+as+perfect+isolation.%22" alt="Quote" />
</div>
