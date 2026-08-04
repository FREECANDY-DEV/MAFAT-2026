# Stage 2 â€” Deep enumeration (secrets, hints, intel)

**Generated (UTC):** 2026-08-04T08:17:47.536757+00:00
**Principal:** `arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0`
**Account:** `121774052880`

> Scope: challenge assets + everything this principal can reach. No speculative flags.

## 1. Public CloudFront / origin surface

| Path | Status | Bytes | Notable headers |
|---|---|---|---|
| `/` | **200** | 1972 | ETag="f1cbe3fb27f4b8e693efec34c74ccbdf"; Last-Modified=Wed, 29 Jul 2026 16:40:54 |
| `/index.html` | **200** | 1972 | ETag="f1cbe3fb27f4b8e693efec34c74ccbdf"; Last-Modified=Wed, 29 Jul 2026 16:40:54 |
| `/docs.html` | **200** | 3099 | ETag="ea5850c0e504e2e3dadbd78af26e34ee"; Last-Modified=Wed, 29 Jul 2026 16:40:54 |
| `/junior_developer.png` | **200** | 3052187 | ETag="8b02f593ff3ab4ebde264b01e0ecfd2d"; Last-Modified=Wed, 29 Jul 2026 16:40:54 |
| `/flag.txt` | **403** | 263 | Content-Type=application/xml; Server=AmazonS3 |
| `/flag` | **404** | 275 | Content-Type=application/xml; Server=AmazonS3 |
| `/secret.txt` | **404** | 301 | Content-Type=application/xml; Server=AmazonS3 |
| `/secret` | **404** | 277 | Content-Type=application/xml; Server=AmazonS3 |
| `/robots.txt` | **404** | 281 | Content-Type=application/xml; Server=AmazonS3 |
| `/.well-known/security.txt` | **404** | 295 | Content-Type=application/xml; Server=AmazonS3 |
| `/favicon.ico` | **404** | 282 | Content-Type=application/xml; Server=AmazonS3 |
| `/sitemap.xml` | **404** | 282 | Content-Type=application/xml; Server=AmazonS3 |
| `/bucket_policy.json` | **404** | 309 | Content-Type=application/xml; Server=AmazonS3 |
| `/policy.json` | **404** | 282 | Content-Type=application/xml; Server=AmazonS3 |
| `/.git/HEAD` | **404** | 280 | Content-Type=application/xml; Server=AmazonS3 |
| `/.env` | **404** | 275 | Content-Type=application/xml; Server=AmazonS3 |
| `/backup` | **404** | 277 | Content-Type=application/xml; Server=AmazonS3 |
| `/admin` | **404** | 296 | Content-Type=application/xml; Server=AmazonS3 |

### 1.1 `index.html` narrative (hints)
```html
???
Test Site
I worked hard on this site, but I had a lot of fun doing it!
I made sure not to include any secret information hereâ€”pretty sure I deleted it all.
Hereâ€™s a picture of me having so much fun:
>
```

**Extracted strings of interest:**
- ` but I had a lot of fun doing it`
- `I made sure not to include any secret information here`
- `I worked hard on this site`
- `Test Site`
- `pretty sure I deleted it all.`
- `s a picture of me having so much fun:`

### 1.2 `docs.html` â€” leaked policy (full structure)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
			],
            "Resource": [
                "arn:aws:s3:::REDACTED/index.html",
                "arn:aws:s3:::REDACTED/docs.html",
                "arn:aws:s3:::REDACTED/junior_developer.png",
                "arn:aws:s3:::REDACTED"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:UserAgent": REDACTED
                }
            }
        },
        {
            "Sid": "Statement2",
            "Principal": "*",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
			],
            "Resource": [
                "arn:aws:s3:::REDACTED/*",
                "arn:aws:s3:::REDACTED"
			],
            "Condition": {
                "StringEquals": {
                    "aws:SourceVpc": REDACTED,
                    "aws:UserAgent": REDACTED
                }
            }
        }
    ]
}
```

**Policy intelligence:**
| Item | Observation |
|---|---|
| Statement1 Principal | `*` |
| Statement1 Actions | `s3:GetObject`, `s3:ListBucket` |
| Statement1 Resources | public keys: index/docs/png + bucket ARN (REDACTED name) |
| Statement1 Condition | `StringEquals` â†’ `aws:UserAgent` = **REDACTED** |
| Statement2 Principal | `*` |
| Statement2 Actions | `s3:GetObject`, `s3:ListBucket` |
| Statement2 Resources | `bucket/*` + bucket (includes `flag.txt`) |
| Statement2 Conditions | `StringEquals` â†’ `aws:SourceVpc` **AND** `aws:UserAgent` both REDACTED |
| StringLike / StringNotEquals | **not present** in leaked HTML |
| SourceVpce | **not present** in leaked HTML |

### 1.3 `junior_developer.png`
- Size: **3052187** bytes
- PNG signature OK: `True` (standard IHDR+IDAT…+IEND; 0 bytes after IEND)
- Bytes after IEND: **0**
- Chunk summary: [('IHDR', 13), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096), ('IDAT', 4096)]...
- Printable strings with keywords: [':]7S3""', "s3G4;3'", 'mo!gMS3', '4jXS3e=', '^s332A$']

## 2. Log bucket deep forensics (`logd8a2f72fe43094e8`)

### 2.1 Layout
```
logd8a2f72fe43094e8/
  userd8a2f72fe43094e8/<ApiName>/<timestamp>.json
```

- Objects scanned (sampled): **140**
- Success-like events (no errorCode): **0**

### 2.2 API volume (sample)
| API | Count in sample |
|---|---|
| `GetObject` | 80 |
| `ListObjects` | 13 |
| `ListObjectVersions` | 13 |
| `GetObjectAcl` | 7 |
| `GetObjectTagging` | 7 |
| `SelectObjectContent` | 6 |
| `PutObject` | 5 |
| `HeadObject` | 4 |
| `CopyObject` | 2 |
| `HeadBucket` | 1 |
| `RestoreObject` | 1 |
| `GetObjectAttributes` | 1 |

### 2.3 User-Agents seen (top 40) â€” **intel for Stmt1/2**
| Count | User-Agent |
|---|---|
| 27 | `Amazon CloudFront` |
| 13 | `Boto3/1.43.62 md/Botocore#1.43.62 md/awscrt#0.36.1 ua/2.1 os/windows#11 md/arch#amd64 lang/python#3.14.6 md/pyimpl#CPyth` |
| 6 | `aws-internal/3` |
| 6 | `AWS Internal` |
| 6 | `Python-urllib/3.13` |
| 6 | `Python-urllib/3.14` |
| 6 | `` |
| 6 | `Boto3` |
| 6 | `secret` |
| 6 | `deleted` |
| 6 | `Miss Me Yet?` |
| 6 | `junior_developer` |
| 6 | `d4ysu55xg7wfi` |
| 5 | `Boto3/1.43.63 md/Botocore#1.43.63 md/awscrt#1.0.0.dev0 ua/2.1 os/linux#6.18.33.2-microsoft-standard-WSL2 md/arch#x86_64 ` |
| 4 | `Boto3/1.43.63 md/Botocore#1.43.63 md/awscrt#1.0.0.dev0 ua/2.1 os/linux#6.18.33.2-microsoft-standard-WSL2 md/arch#x86_64 ` |
| 3 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 3 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 3 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 3 | `Boto3/1.43.62 md/Botocore#1.43.62 md/awscrt#0.36.1 ua/2.1 os/windows#11 md/arch#amd64 lang/python#3.14.6 md/pyimpl#CPyth` |
| 2 | `userd8a2f72fe43094e8` |
| 2 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 2 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 1 | `Boto3/1.43.62 md/Botocore#1.43.62 md/awscrt#0.36.1 ua/2.1 os/windows#11 md/arch#amd64 lang/python#3.14.6 md/pyimpl#CPyth` |
| 1 | `aws-cli/2.31.35 md/awscrt#1.0.0.dev0 ua/2.1 os/linux#6.18.33.2-microsoft-standard-WSL2 md/arch#x86_64 lang/python#3.13.1` |
| 1 | `aws-cli/2.36.2 md/awscrt#0.36.0 ua/2.1 os/linux#6.17.0-1020-azure md/arch#x86_64 lang/python#3.14.6 md/pyimpl#CPython m/` |
| 1 | `Boto3/1.42.97 md/Botocore#1.42.97 ua/2.1 os/linux#5.10.255-260-300.1053.amzn2.x86_64 md/arch#x86_64 lang/python#3.13.14 ` |
| 1 | `Boto3/1.43.63 md/Botocore#1.43.63 md/awscrt#1.0.0.dev0 ua/2.1 os/linux#6.18.33.2-microsoft-standard-WSL2 md/arch#x86_64 ` |
| 1 | `Boto3/1.43.63 md/Botocore#1.43.63 md/awscrt#1.0.0.dev0 ua/2.1 os/linux#6.18.33.2-microsoft-standard-WSL2 md/arch#x86_64 ` |
| 1 | `Boto3/1.43.62 md/Botocore#1.43.62 md/awscrt#0.36.1 ua/2.1 os/windows#11 md/arch#amd64 lang/python#3.14.6 md/pyimpl#CPyth` |

### 2.4 Principals
| Count | Principal |
|---|---|
| 85 | `AWSAccount:anonymous` |
| 50 | `AWSAccount:AROARYWSMSYIPWMOE25U2:d6d7ee068aa0` |
| 3 | `AWSAccount:AROARYWSMSYIHGV6HRCCY:user_function` |
| 1 | `AWSAccount:AROAU2VYTBGYCEB4JME2S:CognitoIdentityCredentials` |
| 1 | `AWSAccount:AROAQEP7C2HWZYKJGPIHM:GitHubActions` |

### 2.5 Object keys requested
| Count | Key |
|---|---|
| 53 | `flag.txt` |
| 45 | `index.html` |
| 3 | `from_lambda_probe.txt` |
| 2 | `participant_probe.txt` |
| 2 | `docs.html` |
| 2 | `junior_developer.png` |
| 2 | `secret` |
| 2 | `secret.txt` |
| 1 | `copy_test_alt.txt` |
| 1 | `alt_copy_test.txt` |

### 2.6 Network
- **VPC endpoints:** {'vpce-04104ef3d57a26557': 109}
- **Source IPs (top):** [('10.0.0.29', 109), ('147.234.73.200', 30), ('172.184.211.113', 1)]

### 2.7 Sample deny messages (secrets/hints in wording)
**Sample 1** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 2** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 3** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 4** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 5** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 6** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 7** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 8** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 9** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 10** (`GetObject` key=`index.html`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 11** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

**Sample 12** (`GetObject` key=`flag.txt`)
- error: `AccessDenied`
- msg: `Access Denied`
- ua: `[Amazon CloudFront]` vpce=`vpce-04104ef3d57a26557` ip=`10.0.0.29`

### 2.8 SUCCESS events
- **None** in sampled windows â€” no historical successful GetObject of flag/public keys in this sample.

## 3. code_exec runtime deep map

Oracle: exact success/error JSON only (stdout suppressed).

### 3.1 Boolean probes
| Probe | Result |
|---|---|
| `pass` | `True` |
| `fail` | `False` |
| `handler_exists` | `True` |
| `handler_len_571` | `True` |
| `only_one_task_file` | `True` |
| `opt_empty` | `True` |
| `tmp_exists` | `True` |
| `has_boto3` | `True` |
| `has_botocore` | `None` |
| `no_FLAG_env` | `True` |
| `no_SECRET_env` | `True` |
| `has_AWS_ACCESS_KEY` | `True` |
| `function_name_user_function` | `True` |
| `region_us_east_1` | `True` |
| `s3_regional_dns` | `True` |
| `bucket_vhost_dns_fails` | `True` |
| `path_unsigned_flag_403` | `True` |
| `path_unsigned_index_403` | `True` |
| `lambda_signed_identity_deny` | `True` |
| `cannot_list_log_as_lambda` | `True` |
| `imds_blocked` | `True` |
| `no_dns_external` | `True` |

### 3.2 Handler source (previously recovered, re-verified length 571)
```python
import base64

def lambda_handler(event, context):
    try:
        encoded_code = event.get("code")
        if not encoded_code:
            return {"error": "Missing 'code' parameter in event"}
        decoded_code = base64.b64decode(encoded_code).decode("utf-8")
        exec(decoded_code)
        return {"result": "Code executed successfully"}
    except Exception as e:
        return {"error": "Something went wrong!"}

```
- **No embedded secrets** (no UA, no flag, no bucket name).

## 4. Secrets / hints board

| # | Finding | Type | Exploit relevance |
|---|---|---|---|
| 1 | Dual redacted bucket policy on `/docs.html` | **Hint** | Defines Stmt1 UA-only and Stmt2 VPC+UA gate |
| 2 | Site narrative: secrets â€œdeletedâ€ | **Hint** | Suggests versioning / non-current objects |
| 3 | Page title `???` | **Hint** | Possible literal UA or joke |
| 4 | `flag.txt` CF 403 not 404 | **Intel** | Object exists / is gated |
| 5 | Participant: only log bucket List/Get | **Access** | Side-channel intelligence + UA-exfil sink |
| 6 | code_exec SigV4 + blind OK/FAIL | **Access** | RCE in VPC; boolean oracle |
| 7 | Path-style S3 works; virtual-hosted DNS fails in Lambda | **Intel** | Must use `s3.us-east-1.amazonaws.com/bucket/key` |
| 8 | lambdaRole signed S3 = identity deny | **Intel** | Prefer UNSIGNED Principal `*` for Stmt2 |
| 9 | Participant-in-Lambda GetObject = resource deny even with CF UA | **Intel** | `Amazon CloudFront` is **not** Stmt2 UA (or not alone) |
| 10 | VPCe `vpce-04104ef3d57a26557` / ENI `10.0.0.29` in logs | **Intel** | Confirms S3 gateway path |
| 11 | cicdRole cannot invoke Stage2 code_exec (GHA proven) | **Intel** | Stage2 â‰  Stage1 OIDC path |
| 12 | 0 successful S3 data events in deep sample | **Intel** | No free UA leak from successes yet |
| 13 | PutObject by cicdRole = explicit identity deny | **Intel** | Writes blocked hard |
| 14 | PNG: no trailing payload / no useful text chunks | **Negative** | Stego dead under basic checks |
| 15 | Handler pure base64+exec, 571 bytes | **Intel** | No secrets in source |

## 5. Cross-account / multi-role map

```text
Account 121774052880
  ctf_participant_role  â†’ logd* (read) + execute-api code_exec
  lambdaRole/user_function â†’ code_exec runtime (no S3 identity allow)

Account 009661764077 (Stage 1)
  cicdRole (GHA OIDC corgi) â†’ Stage1 account enum; NOT Stage2 code_exec

Account 186769093912 (bucket owner from trails)
  userd8a2f72fe43094e8 resource policies (Stmt1/2)
```

## 6. Attack surface residual (what is left)

1. **Unknown `aws:UserAgent`** for Statement2 (and possibly Statement1).
2. Confirm **`aws:SourceVpc`** value equals Lambda VPC (cannot DescribeVpcs as participant).
3. Optional: non-current object versions if ListBucketVersions ever unlocks (currently identity-deny).
4. Monitor logs for first non-AccessDenied GetObject to steal working UA.

## 7. Recommended next exploit steps (ordered)

1. Keep using **participant STS** for code_exec (not cicdRole).
2. From Lambda: path-style **UNSIGNED** `GetObject` `flag.txt` with UA candidates derived from:
   - log-mined unique UAs
   - site narrative exact strings
   - OCR of laptop screen in PNG (if readable)
3. On first HTTP 200: boolean char oracle â†’ flag.
4. Document real flag only after verification; never submit `000000â€¦`.

---
*Deep enum for Cloud Escape CTF 2026 Stage 2 â€” Agent freecandy*

