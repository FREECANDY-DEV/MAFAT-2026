<div align="center">

# 🕵️‍♂️ Operation CloudEscape (MAFAT 2026)
### Official Campaign Intelligence Hub

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=36&duration=2600&pause=900&color=FF9900&center=true&vCenter=true&multiline=true&width=920&height=110&lines=Cloud+Escape+CTF+2026;Operation+CloudEscape+%C2%B7+Official+Report;Agent+freecandy+%E2%80%94+100%25+Solved+(300%2F300+pts)" alt="Cloud Escape CTF 2026" />

<br/>

[![Event](https://img.shields.io/badge/Event-Cloud%20Escape%20CTF%202026-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=FF9900)](https://challenges.cloud-escape.com/)
[![Organizer](https://img.shields.io/badge/Organizer-MAFAT%20%2F%20DDR%26D-6e7681?style=for-the-badge)](https://www.mod.gov.il/)
[![Region](https://img.shields.io/badge/Region-us--east--1-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Score](https://img.shields.io/badge/Score-300%20%2F%20300-2EA44F?style=for-the-badge)](https://challenges.cloud-escape.com/)
[![Status](https://img.shields.io/badge/Status-COMPLETE%20100%25-2EA44F?style=for-the-badge)](https://challenges.cloud-escape.com/)
[![Branch](https://img.shields.io/badge/Branch-corgi-2088FF?style=for-the-badge&logo=github)](https://github.com/FREECANDY-DEV/MAFAT-2026/tree/corgi)

<br/><br/>

| Stage 1 · 100 pts | Stage 2 · 200 pts |
|:---:|:---:|
| [![S1](https://img.shields.io/badge/STAGE%201-HAVE%20SOME%20FAITH-2EA44F?style=for-the-badge&logo=checkmarx)](cloud-escape/Stage_1_Comprehensive_Writeup.md) | [![S2](https://img.shields.io/badge/STAGE%202-MISS%20ME%20YET%3F-2EA44F?style=for-the-badge&logo=checkmarx)](cloud-escape/Stage_2_Comprehensive_Writeup.md) |
| **Flag:** `1a1jelrlfg2yi2s0` | **Flag:** `24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c` |

</div>

<br/>

## 📌 Executive Summary

> Welcome to the official repository and technical intelligence package for **Operation CloudEscape (MAFAT / DDR&D Cloud Escape CTF 2026)**, authored by **Agent freecandy**.
> 
> This campaign encompasses **100% completion (300/300 points)** of the AWS cloud security challenges, demonstrating advanced exploitation vectors spanning GitHub Actions OIDC federation, VPC-isolated Lambda RCE, DNS exfiltration side-channels, CloudTrail data event logging, and Python global namespace patching.

```text
 ▐████████████████████████████████▌  300 / 300 Pts (100%)
  Stage 1 ████████████ CAPTURED (100 Pts)
  Stage 2 ████████████ CAPTURED (200 Pts)
```

> [!TIP]
> **Complete Writeups Available**: High-resolution walk-throughs, technical reports, and reproduction scripts are published in the [`cloud-escape/`](cloud-escape/) directory.

<details>
<summary><b>📑 Table of Contents (Click to Expand)</b></summary>
<br/>

- [Scoreboard & Overview](#-scoreboard--overview)
- [Campaign Architecture](#-campaign-architecture)
- [Stage 1: Have Some Faith (100 Pts)](#-stage-1--have-some-faith-100-pts)
- [Stage 2: Miss Me Yet? (200 Pts)](#-stage-2--miss-me-yet-200-pts)
- [Repository Layout & Documentation](#-repository-layout--documentation)
- [GitHub Actions & Automation](#️-github-actions--automation)
- [Ethics & Legal Disclaimer](#️-ethics--legal-disclaimer)

</details>

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 🏆 Scoreboard & Overview

| Stage | Challenge | Pts | Primary Vectors & Techniques | Captured Flag | Status | Writeup |
|:---:|:---|:---:|:---|:---:|:---:|:---|
| **01** | **Have Some Faith** | 100 | `GitHub OIDC Wildcard` ➔ `cicdRole` ➔ `Command Injection` ➔ `DNS Tunneling` | `1a1jel...` | ✅ | [Stage 1](cloud-escape/Stage_1_Comprehensive_Writeup.md) |
| **02** | **Miss Me Yet?** | 200 | `Platform STS` ➔ `SigV4 API GW` ➔ `Lambda RCE` ➔ `Namespace Patch` | `24dbd6...` | ✅ | [Stage 2](cloud-escape/Stage_2_Comprehensive_Writeup.md) |

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 🌐 Campaign Architecture

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#1c1c1c',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#FF9900',
    'lineColor': '#FF9900',
    'secondaryColor': '#2b2b2b',
    'tertiaryColor': '#0D1117'
  }
}}%%
flowchart TB
    subgraph STAGE1 ["STAGE 1 · Have Some Faith (100 Pts) · CAPTURED"]
        direction TB
        DOTGIT["dotgit Forensics"] --> OIDC["GitHub OIDC Wildcard<br/>repo:*/* : refs/heads/corgi"]
        OIDC --> GHA1["GitHub Actions Runner"]
        GHA1 --> STS1["Assume Role: cicdRole<br/>Account: 009661764077"]
        STS1 --> RCE1["API: /dev/nslookupv2<br/>Command Injection (shell=True)"]
        RCE1 --> DNS1["VPC Route 53 Resolver<br/>(169.254.169.253)"]
        DNS1 --> EXFIL1["DNS Tunnel Exfiltration<br/>Hex Encoded Subdomain"]
    end

    subgraph STAGE2 ["STAGE 2 · Miss Me Yet? (200 Pts) · CAPTURED"]
        direction TB
        PORTAL["Platform STS"] --> STS2["Role: ctf_participant_role<br/>Account: 121774052880"]
        STS2 --> SIGV4["SigV4 Authenticated POST"]
        SIGV4 --> APIGW["API Gateway: /dev/code_exec"]
        APIGW --> LAMBDA2["Lambda Execution Sandbox<br/>VPC Subnet 10.0.0.29 (Hyperplane)"]
        
        LAMBDA2 --> VPCE["S3 VPC Endpoint<br/>vpce-04104ef3d57a26557"]
        VPCE --> S3USER["S3 Bucket: userd8a2f72fe43094e8<br/>(flag.txt & assets)"]
        VPCE --> S3LOG["S3 Bucket: logd8a2f72fe43094e8<br/>(CloudTrail Data Events)"]
        
        LAMBDA2 --> PATCH["Global Namespace Patch<br/>global _ad_json; _ad_json = json"]
        PATCH --> CTFOUT["Wrapper Response Interception<br/>ctf_out.f_value"]
    end

    STAGE1 -.->|"Separate AWS Account & IAM Context"| STAGE2
```

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## ⚡ Stage 1 — Have Some Faith (100 Pts)

### 🎯 Mission Brief
* **Account ID**: `009661764077` (us-east-1)
* **Initial Surface**: Forensics on extracted `.git` directory (`dotgit.zip`) revealed a permissive AWS IAM OIDC trust policy allowing any repository on the `corgi` branch to assume `arn:aws:iam::009661764077:role/cicdRole`.

### 🚀 Execution & Exfiltration
1. Triggered GitHub Actions on `refs/heads/corgi` to assume `cicdRole`.
2. Discovered an internal endpoint `/dev/nslookupv2` vulnerable to command injection via unsanitized input passed to `subprocess.Popen(..., shell=True)`.
3. Bypassed outbound network filtering by tunneling the flag via hex-encoded subdomains using the internal Route 53 DNS resolver (`169.254.169.253`).

> [!NOTE]
> Detailed kill-chain breakdown and full PoC workflow available in [Stage_1_Comprehensive_Writeup.md](cloud-escape/Stage_1_Comprehensive_Writeup.md).

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 🔒 Stage 2 — Miss Me Yet? (200 Pts)

### 🎯 Mission Brief
* **Account ID**: `121774052880` (us-east-1)
* **Target Services**: API Gateway (`code_exec`), Isolated VPC Lambda (`10.0.0.29`), S3 Buckets (`userd8a...`, `logd8a...`), CloudFront (`d4ysu55xg7wfi`).

### 🚀 Execution & Exfiltration
1. Authenticated to `/dev/code_exec` using SigV4 credentials under `ctf_participant_role`.
2. Mapped the dark Lambda execution sandbox using blind boolean and timing oracles (`sleep(4)` timing side-channel).
3. Identified a live server-side wrapper update throwing `NameError: name '_ad_json' is not defined` inside `_advanced_dispatcher`.
4. Injected `global _ad_json; _ad_json = __import__('json')` into the runtime namespace to patch the wrapper post-execution.
5. Extracted the accepted SHA-256 flag from `ctf_out.f_value` in the HTTP response.

> [!IMPORTANT]
> Complete writeup with 7 Mermaid diagrams, timing oracle calibrations, and CloudTrail OOB logs available in [Stage_2_Comprehensive_Writeup.md](cloud-escape/Stage_2_Comprehensive_Writeup.md).

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 📂 Repository Layout & Documentation

<h3>📁 Structure</h3>

```text
MAFAT-2026/ (branch: corgi)
├── README.md                            ← Main Campaign Intelligence Hub
├── .github/workflows/
│   ├── stage1.yml                       ← Stage 1 OIDC & DNS Exfil Pipeline
│   └── stage2.yml                       ← Stage 2 SigV4 & Lambda Probe Pipeline
└── cloud-escape/
    ├── README.md                        ← Documentation Index Hub
    ├── WRITEUP.md                       ← Executive Campaign Summary
    ├── Stage_1_Comprehensive_Writeup.md ← Full Stage 1 Solve Report
    └── Stage_2_Comprehensive_Writeup.md ← Canonical 800+ Line Stage 2 Solve Narrative & Diagrams
```

<h3>📚 Documentation Index</h3>

| Document | Description |
|:---|:---|
| 📖 **[Stage 1 Solve Report](cloud-escape/Stage_1_Comprehensive_Writeup.md)** | Deep dive into OIDC trust exploitation, command injection, and DNS tunneling. |
| 📘 **[Stage 2 Comprehensive Writeup](cloud-escape/Stage_2_Comprehensive_Writeup.md)** | Definitive 800+ line solve narrative, 7 Mermaid diagrams, and wrapper patch analysis. |
| 📙 **[Executive Campaign Summary](cloud-escape/WRITEUP.md)** | High-level summary report for reviewers. |
| 📗 **[Documentation Hub](cloud-escape/README.md)** | Subdirectory index mapping all challenge assets and scripts. |

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## ⚙️ GitHub Actions & Automation

This repository includes fully automated GitHub Actions workflows for reproducing both stages:

- 🛠️ **[Stage 1 Workflow (`stage1.yml`)](.github/workflows/stage1.yml)**: Authenticates via AWS OIDC on `refs/heads/corgi`, assumes `cicdRole`, triggers the RCE payload, and decodes the exfiltrated DNS queries.
- 🚀 **[Stage 2 Workflow (`stage2.yml`)](.github/workflows/stage2.yml)**: Uses platform STS credentials to sign API Gateway requests with SigV4 and verify Lambda responsiveness.

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

## 🛡️ Ethics & Legal Disclaimer

> [!WARNING]
> All activities documented in this repository were conducted strictly within authorized CTF lab environments provided by the **MAFAT / DDR&D Cloud Escape CTF 2026** organizers. Techniques and code are published purely for educational and defensive research purposes. Do not attempt these techniques on unauthorized systems.

<br/>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3200&pause=1200&color=00C7B7&center=true&vCenter=true&width=720&height=40&lines=Agent+freecandy+%C2%B7+Operation+CloudEscape;100%25+Solved+%C2%B7+300%2F300+Pts+%C2%B7+All+Flags+Captured" alt="footer" />

<br/><br/>

**Designed & Developed by Agent freecandy · 2026**

</div>
