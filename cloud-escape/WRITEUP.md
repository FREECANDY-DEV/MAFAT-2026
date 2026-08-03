# ☁️ Cloud Escape CTF 2026 — Combined Summary

**Team:** Agent freecandy

---

## 🚩 Stage 1: Have Some Faith
**Flag:** `1a1jelrlfg2yi2s0`

Stage 1 focused on gaining an initial foothold into the target AWS environment and pivoting to extract data from an isolated VPC.
- **Initial Foothold:** Identified a critical misconfiguration in a GitHub OIDC trust policy (`repo:*/*`), allowing us to assume the highly privileged `cicdRole`.
- **Enumeration:** Revealed an API Gateway endpoint backed by a vulnerable Lambda function (`nslookupv2`).
- **Exploitation & Exfiltration:** The Lambda was vulnerable to command injection via the `domain` parameter. However, the VPC lacked outbound internet access. To exfiltrate the S3-hosted flag, we abused the built-in AWS Route 53 VPC Resolver to forward DNS queries containing the hex-encoded flag to our controlled DNS server.

---

## 🚩 Stage 2: Miss Me Yet?
**Flag:** `0102013`

Stage 2 elevated the difficulty with strict egress filtering and blind execution contexts.
- **Discovery:** Found a leaked S3 Bucket Policy inside `/docs.html` on a CloudFront distribution, detailing that access was restricted to requests coming from within the VPC **and** presenting a `User-Agent: Amazon CloudFront` header.
- **Exploitation:** Leveraged an arbitrary code execution Lambda (`/dev/code_exec`). We injected a `boto3` event hook to spoof the `User-Agent` header, successfully bypassing the IAM policy.
- **Exfiltration:** Because the Lambda returned no standard output, we engineered a Blind Timing Side-Channel. By injecting conditional `time.sleep()` statements based on character matches, we measured the API response latency to successfully extract the flag character by character.

---

*Write-up by Agent freecandy — Cloud Escape CTF 2026*
