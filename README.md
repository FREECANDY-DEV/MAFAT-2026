# ☁️ Cloud Escape CTF 2026 — Full Writeup (Stage 1 & 2)

**Team:** Agent freecandy

Welcome to the comprehensive writeup repository for the **Cloud Escape CTF 2026**. This repository details the methodologies, vulnerabilities, and exploitation techniques used to completely compromise the target AWS infrastructure across both stages of the competition.

---

## 🏆 Summary of Compromise

| Stage | Challenge | Key Vulnerabilities Exploited | Flag |
|---|---|---|---|
| **Stage 1** | Have Some Faith | Misconfigured OIDC Wildcard Trust Policy, Lambda Command Injection, DNS Side-Channel Exfiltration | `1a1jelrlfg2yi2s0` |
| **Stage 2** | Miss Me Yet? | Unsafe Python Code Execution (`exec()`), `aws:UserAgent` Identity Bypass, High-Precision Timing Side-Channel | `0102013` |

---

## 📖 Detailed Writeups

Each stage required unique lateral movement and bypassing of severe network isolation constraints within an AWS VPC environment. 

🔗 **[Stage 1: Have Some Faith — Deep Dive Writeup](cloud-escape/WRITEUP_STAGE1.md)**
- Detailed breakdown of exploiting a wildcard GitHub OIDC trust policy.
- Automated API Gateway command injection.
- Bypassing strict VPC network isolation by leveraging the default AWS Route 53 VPC Resolver (`169.254.169.253`) for DNS exfiltration.

🔗 **[Stage 2: Miss Me Yet? — Deep Dive Writeup](cloud-escape/WRITEUP_STAGE2.md)**
- Analysis of a leaked S3 bucket policy via a CloudFront website.
- Overriding signed HTTP headers inside `boto3` to spoof `User-Agent: Amazon CloudFront` and satisfy IAM policy conditions.
- Developing a 100% accurate, multi-threaded Blind Timing Side-Channel Oracle to leak data from an isolated Lambda environment.

🔗 **[Combined Stage Overview](cloud-escape/WRITEUP.md)**

---

*Write-up by Agent freecandy — Cloud Escape CTF 2026*
