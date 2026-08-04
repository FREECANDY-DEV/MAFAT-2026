<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=34&duration=2600&pause=900&color=FF9900&center=true&vCenter=true&width=820&height=75&lines=Cloud+Escape+CTF+2026;Combined+Campaign+Summary" alt="Typing SVG" />

  <p>
    <img src="https://img.shields.io/badge/Team-Agent+freecandy-F79211?style=for-the-badge" alt="team" />
    <img src="https://img.shields.io/badge/Stage1-1a1jelrlfg2yi2s0-2EA44F?style=for-the-badge" alt="f1" />
    <img src="https://img.shields.io/badge/Stage2-Pending-yellow?style=for-the-badge" alt="f2" />
  </p>
</div>

---

## Stage 1 — Have Some Faith

| | |
|:---|:---|
| **Flag** | `1a1jelrlfg2yi2s0` |
| **Points** | 100 |
| **Doc** | [Stage_1_Have_Some_Faith.md](Stage_1_Have_Some_Faith.md) |

**Chain**

1. Forensics on `dotgit.zip` → OIDC trust `repo:*/*:ref:refs/heads/corgi`
2. GitHub Actions on branch `corgi` → assume `cicdRole` (`009661764077`)
3. Command injection in `/dev/nslookupv2` (`shell=True`)
4. Read S3 flag inside VPC; exfil via Route 53 DNS (`169.254.169.253`) → external DNS hex decode

---

## Stage 2 — Miss Me Yet?

| | |
|:---|:---|
| **Flag** | `[NOT CAPTURED]` |
| **Points** | 200 |
| **Docs** | [Writeup](Stage_2_Miss_Me_Yet.md) · [Deep enum](Stage2_Deep_Enumeration.md) · [AWS map](Stage2_AWS_Environment.md) |

**Chain (designed)**

1. Platform STS → `ctf_participant_role` (not cicdRole)
2. Log bucket forensics (`logd8a2f72fe43094e8`)
3. SigV4 `code_exec` → blind Python in VPC (S3 VPCe only)
4. Path-style UNSIGNED S3 + match Statement2 `SourceVpc` **and** `User-Agent`
5. Boolean oracle / UA→CloudTrail exfil → flag

**Hard constraints**

- `cicdRole` **cannot** invoke Stage 2 `code_exec` (GHA-proven)
- Virtual-hosted S3 DNS fails inside Lambda; **path-style required**
- `lambdaRole` signed S3 → identity deny; prefer Principal `*`
- Never submit `00000000000000000000`

---

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3200&pause=1000&color=00C7B7&center=true&vCenter=true&width=620&height=35&lines=Agent+freecandy+%E2%80%A2+Cloud+Escape+CTF+2026" alt="footer" />
</div>
