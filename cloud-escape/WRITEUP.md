# ☁️ Cloud Escape CTF 2026 — Combined Summary

**Team:** Agent freecandy

---

## 🚩 Stage 1: Have Some Faith

**Flag:** `1a1jelrlfg2yi2s0`

Stage 1 focused on gaining an initial foothold into the target AWS environment and pivoting to extract data from an isolated VPC.

- **Initial foothold:** Misconfigured GitHub OIDC trust policy (`repo:*/*` on branch `corgi`) → assume `cicdRole` in account `009661764077`.
- **Enumeration:** S3 buckets, Lambdas (`nslookupv2`, `code_exec`), CloudFront, API Gateway.
- **Exploitation & exfiltration:** Command injection in `/dev/nslookupv2` (`shell=True` + unsanitized `domain`). No VPC internet egress — flag hex-exfiltrated via Route 53 VPC DNS resolver (`169.254.169.253`) to an external DNS log.

**Full writeup:** [Stage_1_Have_Some_Faith.md](Stage_1_Have_Some_Faith.md)

---

## 🚩 Stage 2: Miss Me Yet?

Stage 2 elevates difficulty with strict egress filtering and a blind code-exec context.

- **Discovery:** CloudFront site + `/docs.html` bucket policy (Statement1: UA; Statement2: SourceVpc + UA). Participant can read `logd8a2f72fe43094e8` audit trail.
- **Execution:** `/dev/code_exec` runs base64 Python with stdout suppressed; S3 path via VPC endpoint; Boto3/`urllib` User-Agent injection.
- **Forensics:** CloudTrail principals, deny taxonomy, versioning hypothesis, boolean/timing oracles, UA→log exfil channel.

**Full writeup:** [Stage_2_Miss_Me_Yet.md](Stage_2_Miss_Me_Yet.md)

---

*Write-up by Agent freecandy — Cloud Escape CTF 2026*
