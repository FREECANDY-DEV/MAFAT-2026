<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=40&pause=1000&color=F71111&center=true&vCenter=true&width=800&height=80&lines=%E2%98%81%EF%B8%8F+Cloud+Escape+CTF+2026;Operation+%22Miss+Me+Yet%3F%22;Full+Writeup+by+Agent+freecandy" alt="Typing SVG" />
</div>

<div align="center">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" />
  <img src="https://img.shields.io/badge/CTF-Hacking-FF0000?style=for-the-badge&logo=hackthebox&logoColor=white" />
</div>

<br/>

<details open>
<summary><h2> 📖 Executive Summary & Official Submission </h2></summary>

Welcome to the comprehensive writeup repository for the **Cloud Escape CTF 2026**, organized by MAFAT (DDR&D) at the Israel Ministry of Defense and the C4I Cyber Defense Directorate.

This repository serves as our **Official Mandatory Write-Up**. It contains the complete exploitation lifecycle, methodologies, automated Proof of Concepts (PoCs), and scripts used to compromise a heavily restricted AWS infrastructure across two complex stages.
</details>

---

## ✉️ The Adventure Begins

Our journey began with a high-stakes transmission:
> *"Your mission: penetrate a highly secure, custom-built cloud environment, navigate complex architectures, and extract the hidden data flags before time runs out."*

With a massive $15,000 grand prize and a specific $3,000 bounty for **"out-of-the-box" creativity** on the line, standard tools were obsolete. We were facing a target hardened against traditional exfiltration, demanding deep mastery over IAM permission management and complex VPC networking. 

We engineered two sophisticated side-channel attacks to bypass modern defense concepts and exfiltrate flags from completely blind environments.

---

## 🔍 How We Found It: The Reconnaissance

To crack an enterprise-grade cloud environment, meticulous reconnaissance is vital. Here is how we uncovered the critical vulnerabilities:

1. **Git Forensics (`Stage 1`)**: We started with a provided `dotgit.zip` file. By extracting it and running `git log -p`, we scoured the commit history of the Terraform infrastructure files. Deep within an old commit (`17e4932`), we discovered a critical OIDC trust policy template utilizing a wildcard (`repo:*/*`). This was our skeleton key.
2. **Identity Enumeration (`Stage 1`)**: After assuming the `cicdRole` via GitHub Actions, we used the `aws-cli` to aggressively list S3 buckets, Lambda functions, and API Gateways, mapping the internal attack surface.
3. **Directory Busting & CloudFront (`Stage 2`)**: Moving to the second stage, we encountered a hardened CloudFront distribution. Standard interaction yielded nothing. However, by fuzzing the endpoints (directory busting), we uncovered an exposed `/docs.html` file. This file accidentally leaked the raw JSON of an S3 Bucket Policy, revealing the exact `aws:UserAgent` and `aws:SourceVpc` conditions required for access.

---

## 🏆 Captured Flags

| Stage | Challenge Name | Difficulty | Status | Flag / Methodology |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Have Some Faith | <img src="https://img.shields.io/badge/High-FF0000?style=flat-square" /> | 🟢 **COMPLETED (100 PTS)** | `1a1jelrlfg2yi2s0` |
| **2** | Miss Me Yet? | <img src="https://img.shields.io/badge/Critical-8B0000?style=flat-square" /> | 🟢 **VERIFIED (200 PTS)** | *[S3 Versioning & Audit Logs]* |

---

## ⚙️ How to Use This Guide & Run the Exploits on GitHub

For judges and researchers, we have built **fully automated, one-click exploit chains** using GitHub Actions. You do not need any local AWS credentials to test this.

### Running the Proof of Concepts (PoCs)
Our exploits are packaged as GitHub Action Workflows in the `.github/workflows/` directory.

1. **Fork this Repository**: Clone this repository to your own GitHub account.
2. **Navigate to the Actions Tab**: In your forked repository, click on the "Actions" tab at the top.
3. **Enable Workflows**: If prompted, click "I understand my workflows, go ahead and enable them."
4. **Trigger the Exploit**: 
   - Select either **"Cloud Escape - Stage 1 Recon"** or **"Cloud Escape - Flag Exfiltration"** from the left sidebar.
   - Click the **"Run workflow"** button.
   - Alternatively, you can simply push a commit to the `corgi` branch, and the pipelines will trigger automatically.
5. **View the Loot**: Click into the running job to watch the live logs as the runner assumes the AWS IAM role, executes the command injection, and triggers the exfiltration side-channels!

---

## 📂 Documentation Directory

* 🛡️ **[Master Challenge Overview](cloud-escape/README.md)**: A master document detailing the full attack narrative.
* 🚀 **[Stage 1: "Have Some Faith" (100 PTS)](cloud-escape/Stage_1_Have_Some_Faith.md)**: OIDC exploitation, recon, and DNS side-channel payloads.
* ⏱️ **[Stage 2: "Miss Me Yet?" (200 PTS)](cloud-escape/Stage_2_Miss_Me_Yet.md)**: CloudFront policy analysis, header injection, S3 versioning, and access log forensics.

---
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=400&size=20&pause=2000&color=888888&center=true&vCenter=true&width=600&height=50&lines=%22In+the+cloud,+there+is+no+such+thing+as+perfect+isolation.%22" alt="Quote" />
</div>
