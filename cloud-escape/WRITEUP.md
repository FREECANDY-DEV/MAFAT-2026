<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&duration=2600&pause=900&color=FF9900&center=true&vCenter=true&width=820&height=75&lines=Cloud+Escape+CTF+2026;Combined+Campaign+Report" alt="Combined report" />

<p>
  <img src="https://img.shields.io/badge/Team-Agent+freecandy-F79211?style=for-the-badge" alt="team" />
  <img src="https://img.shields.io/badge/Stage1-1a1jelrlfg2yi2s0-2EA44F?style=for-the-badge" alt="f1" />
  <img src="https://img.shields.io/badge/Stage2-Pending-yellow?style=for-the-badge" alt="f2" />
</p>

</div>

---

## 1. Purpose of this document

This is the **combined executive campaign report** for Cloud Escape CTF 2026. It is suitable for:

- Official writeup submission / peer review  
- Handoff to another operator  
- Audit of what was proven vs what remains  

Detailed step-by-step content lives in the per-stage files linked below.

---

## 2. Campaign outcome

| Stage | Challenge | Pts | Flag | Outcome |
|:---:|:---|:---:|:---|:---|
| 1 | Have Some Faith | 100 | `1a1jelrlfg2yi2s0` | **Captured** |
| 2 | Miss Me Yet? | 200 | — | **Mapped · not captured** |
| **Total** | | **100 / 300** | | In progress |

**Hard negatives (never submit)**

| Value | Reason |
|:---|:---|
| `00000000000000000000` | Decoy / false-positive timing oracle |
| Stage 1 flag as Stage 2 answer | Wrong challenge plane |

---

## 3. Stage 1 — Have Some Faith (solved)

| | |
|:---|:---|
| **Flag** | `1a1jelrlfg2yi2s0` |
| **Points** | 100 |
| **Doc** | [Stage_1_Have_Some_Faith.md](Stage_1_Have_Some_Faith.md) |
| **Account** | `009661764077` |

### Chain

1. Forensic review of `dotgit.zip` / Terraform history  
2. Discovery of OIDC trust: `repo:*/*:ref:refs/heads/corgi`  
3. GitHub Actions on branch `corgi` → assume `cicdRole`  
4. Command injection on `/dev/nslookupv2` (`shell=True`)  
5. Flag read inside VPC; exfil via Route 53 Resolver (`169.254.169.253`) → external DNS hex decode  

### Why it worked

The CI/CD trust boundary was wider than intended (wildcard repository subject). Combined with a classic shell-injection RCE and a DNS side-channel that bypassed “no outbound data” isolation, the Stage 1 flag left the VPC.

---

## 4. Stage 2 — Miss Me Yet? (mapped)

| | |
|:---|:---|
| **Flag** | `[NOT CAPTURED]` |
| **Points** | 200 |
| **Docs** | [Writeup](Stage_2_Miss_Me_Yet.md) · [Technical report](Stage2_Technical_Report.md) · [Deep enum](Stage2_Deep_Enumeration.md) · [AWS map](Stage2_AWS_Environment.md) |

### Assets

| Asset | Value |
|:---|:---|
| CloudFront | `https://d4ysu55xg7wfi.cloudfront.net/` |
| code_exec API | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| User bucket | `userd8a2f72fe43094e8` (owner **186769093912**) |
| Log bucket | `logd8a2f72fe43094e8` |
| Player account | `121774052880` |
| Participant role | `ctf_participant_role` |
| Lambda role | `lambdaRole/user_function` |
| S3 VPCe | `vpce-04104ef3d57a26557` · ENI `10.0.0.29` |

### Designed / intended chain

```text
1. Platform STS → ctf_participant_role
2. Log-bucket forensics (CloudTrail-style data events)
3. SigV4 invoke /dev/code_exec (base64 Python)
4. From Lambda: path-style S3 over gateway VPCe
5. Satisfy resource policy Statement2:
     Principal * + StringEquals aws:SourceVpc + aws:UserAgent
6. GetObject flag.txt → recover body via boolean oracle or UA-exfil to logs
```

### What was proven (high confidence)

1. **code_exec** is a pure `base64` → `exec` sandbox (~571 bytes). No embedded flag or UA secret.  
2. **Participant IAM surface is minimal**: log List/Get + `code_exec` invoke; almost all control plane denied.  
3. **Cross-account** user bucket (owner ≠ player).  
4. **lambdaRole** signed S3 → **identity-based** AccessDenied.  
5. **participant** signed S3 → **resource-based** AccessDenied until Stmt2 conditions match.  
6. **Virtual-hosted S3 DNS fails** in Lambda; **path-style** is required.  
7. **UNSIGNED path-style** from Lambda reaches S3 via VPCe (HTTP 403 with wrong UA).  
8. Lambda is **S3-only**: IMDS connection refused; STS unreachable; Hyperplane networking (`169.254.100.5/6`).  
9. CloudFront public site uses **OAC/OAI** (not Statement1 UA spoof). `docs.html` leaks policy **structure** with **REDACTED** values.  
10. Log corpus (tens of thousands of events) shows **0 successful** S3 data-plane reads of the flag.  
11. Literal `Amazon CloudFront` and large deliberate/wordlist UA sets are **falsified**.  
12. **cicdRole** (Stage 1 GHA OIDC) **cannot** invoke Stage 2 `code_exec`.  
13. **UA → CloudTrail exfil** is a reliable blind channel (handler/env/deny-message recovery).  

### Identity matrix

| Capability | Participant | cicdRole (GHA) | lambdaRole (runtime) |
|:---|:---:|:---:|:---:|
| Invoke Stage 2 `code_exec` | ✅ | ❌ | n/a |
| Read log bucket | ✅ | ❌ | side-channel only |
| Direct user-bucket GetObject | ❌ | ❌ | needs policy + no identity deny |
| Path-style S3 from VPC | n/a | n/a | ✅ required |
| Virtual-hosted S3 from VPC | n/a | n/a | ❌ |

### Residual problem statement

```text
UNKNOWN: exact StringEquals value of Statement2 aws:UserAgent
UNKNOWN (unverified): aws:SourceVpc equals Lambda VPC
(vpc-xxxx cannot be read from IMDS inside the sandbox)

ONCE KNOWN:
  UNSIGNED + path-style + correct UA
  → HTTP 200 on flag.txt
  → boolean / UA-exfil → flag string
```

### Explicitly abandoned (without new evidence)

- Blind multi-thousand UA dictionary / ffuf spray  
- Treating Stage 1 `cicdRole` as Stage 2 RCE path  
- Expecting CF public GETs to reveal Stmt1 UA  
- Expecting unredacted policy on current `docs.html` ETag  

---

## 5. Tooling & evidence practices

| Practice | Implementation |
|:---|:---|
| Blind code_exec oracle | Exact body match: success vs `Something went wrong!` + majority vote |
| Deny-message recovery | Force ClientError → chunk into `User-Agent` → read log bucket |
| Network classification | Exception type + HTTP status from path vs virtual hosts |
| Log forensics | Minute-prefix `StartAfter` (list is lexical; MaxKeys alone is oldest-biased) |
| Automation | GHA `stage1.yml` (OIDC) · `stage2.yml` (participant STS inputs) |

---

## 6. References inside this repo

| Document | Role |
|:---|:---|
| [Stage_1_Have_Some_Faith.md](Stage_1_Have_Some_Faith.md) | Stage 1 full solve |
| [Stage_2_Miss_Me_Yet.md](Stage_2_Miss_Me_Yet.md) | Stage 2 methodology |
| [Stage2_Technical_Report.md](Stage2_Technical_Report.md) | Full technical consolidation |
| [Stage2_Deep_Enumeration.md](Stage2_Deep_Enumeration.md) | Enumeration detail |
| [Stage2_AWS_Environment.md](Stage2_AWS_Environment.md) | IAM/S3 probe matrix |
| [../README.md](../README.md) | Mission control hub |

---

## 7. Ethics

Authorized CTF only. Do not apply these techniques to systems outside the challenge scope.

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&duration=3000&pause=1000&color=00C7B7&center=true&vCenter=true&width=640&height=35&lines=Agent+freecandy+%C2%B7+Cloud+Escape+CTF+2026" alt="footer" />
</div>

### 8. Latest Reconnaissance Additions

- The execution environment is an S3-only prison: IMDS, X-Ray (169.254.100.1:2000), and STS endpoints are entirely inaccessible.
- Using boto3 *inside* the Lambda payload with ctf_participant_role credentials still yields an AccessDenied on S3 resources, because the boto3 User-Agent does not match the StringEquals requirement in Statement 2 of the bucket policy.
- Without the exact undocumented ws:UserAgent string for Statement 2, all known exfiltration paths remain blocked.
