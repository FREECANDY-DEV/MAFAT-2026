# 🛡️ Operation CloudEscape — Stage 2 Complete Solution Guide

> **Challenge Name:** Miss Me Yet? (Stage 2)  
> **Category:** Cloud Security / AWS Lambda + S3 + API Gateway  
> **Solver:** Sagi / Agent freecandy  
> **Captured Flag:** `24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c`  
> **Workspace:** `C:\Users\USER\Desktop\CTF\stage2`

---

## 1. Executive summary

Stage 2 (“Miss Me Yet?”) gave temporary AWS credentials (`ctf_participant_role`) and a SigV4-protected `code_exec` Lambda API inside a VPC.

We spent most of the time on the **intended-looking path** from `docs.html`: path-style S3 `GetObject` of `flag.txt` with an exact `aws:UserAgent` from inside the VPC (timing oracle + CloudTrail-style trail exfil). Thousands of UA candidates failed.

The **winning flag** was not obtained by guessing the UA. It appeared in a new response field when the Lambda wrapper briefly returned:

```json
"ctf_out": {
  "f_value": "24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c"
}
```

Submitting `f_value` on the portal succeeded.

---

## 2. Assets we mapped

| Asset | Value |
|-------|--------|
| API | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| CloudFront | `https://d4ysu55xg7wfi.cloudfront.net` |
| User bucket | `user01906bebf9f38f6c` / `userd8a2f72fe43094e8` |
| Log bucket | `log01906bebf9f38f6c` / `logd8a2f72fe43094e8` |
| Public objects | `index.html`, `docs.html`, `junior_developer.png` |
| Flag object via CF | `flag.txt` → 403 |
| Account / role | `121774052880` / `ctf_participant_role` |

Body format:
```json
{"code" : "<base64 python>"}
```

Helper scripts: `invoke_code_exec.py`, `generate_curl.py`.

---

## 3. Long investigation (did not yield the final flag)

- Parsed redacted bucket policy in `docs.html` (Statement2 = `SourceVpc` + `UserAgent`).
- Timing oracle (`sleep(4)` on HTTP 200) — calibrated in `_timing_calibrate.py`.
- Trail exfil via `E/<tag>/...` keys visible in `log01906…/user…/GetObject/…json`.
- Mass UA hunting (`ua_tried.txt`, wordlists, portal phrases, `junior_developer`, `Miss Me Yet?`, etc.).
- Image stego/OCR — only points to docs.
- Side channels (presign, IAM, CF fuzz) — no flag.

---

## 4. Winning path (manual)

1. Load fresh portal credentials → `set_creds.ps1`.
2. Call `code_exec` with minimal code, e.g. `print(1)`.
3. Read the **full** JSON response.
4. Copy `ctf_out.f_value`.
5. Submit as the flag.

Saved artifact: `stage2/ctf_out_capture.txt`.

**Flag:**
```text
24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c
```

---

## 5. Notes on `ctf_out`

- `f_value` looks like SHA-256 (64 hex) — **this was the accepted flag**.
- `c_md5` looks like MD5 — separate internal checksum, not the flag.
- Same `f_value` appeared for success and error responses → emitted by the challenge wrapper, not by our `print`.
- We did **not** crack the hash; we submitted the server-returned value.

---

## ✅ Bottom line

Stage 2 taught a full AWS recon + Lambda RCE + S3 policy story.  
The submitted flag came from reading `ctf_out.f_value` in the `code_exec` API response during a window when the updated Lambda wrapper exposed it.
