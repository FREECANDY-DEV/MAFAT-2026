# Stage 2 Writeup: Miss Me Yet?

## Challenge Overview
- **Challenge:** "Miss Me Yet?" - Stage 2
- **New Components:**
  - CloudFront Distribution: `https://d4ysu55xg7wfi.cloudfront.net/`
  - Code Execution API: `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec`
  - Target Buckets: `userd8a2f72fe43094e8`, `logd8a2f72fe43094e8`
  - Test Site Bucket: `site781fe43f26b9eba3`

## Phase 1: Test Site Investigation
We investigated the test site exposed via CloudFront and discovered a `/docs.html` endpoint that leaked a bucket policy.
The policy required specific `aws:UserAgent` and `aws:SourceVpc` conditions:
- **Statement 1:** Allowed `GetObject` and `ListBucket` for specific files (`index.html`, `docs.html`, `junior_developer.png`) conditionally based on a specific `UserAgent`.
- **Statement 2:** Allowed `GetObject` and `ListBucket` for all objects, but required both `SourceVpc` AND `UserAgent` conditions to be met.

## Phase 2: Code Execution Lambda Analysis
The API provided a `/dev/code_exec` endpoint that accepted base64-encoded Python code.
The response from this Lambda was strictly binary:
- `{"result":"Code executed successfully"}`
- `{"error":"Something went wrong!"}`

The Lambda function was deployed inside a VPC **without** an S3 VPC endpoint. Attempting any AWS API calls resulted in timeouts (4-11s).
Furthermore, there was no standard output capture, and no exception details were returned in the response.
Through systematic testing, we determined our capabilities: we could execute arbitrary Python code, import `boto3`, and create clients, but we **could not** successfully complete any AWS API calls due to network restrictions.

## Phase 3: Header Injection Bypass
To interact with the buckets and bypass the policy conditions, we utilized a `boto3` event handler to inject the required `User-Agent: Amazon CloudFront` header into our requests.
This was achieved by registering a custom event hook:
```python
s3.meta.events.register('before-send.s3.*', set_ua)
```
This successfully bypassed the bucket policy's User-Agent requirement.

## Phase 4: Timing Side-Channel Oracle
Because the Lambda execution returned no direct output, we developed a blind timing oracle based on `time.sleep()`.
By measuring the response time of the API, we could infer binary conditions:
- **True condition:** We injected `sleep(2.0)`, resulting in a total API response time of ~9.5-13.8 seconds.
- **False condition:** No sleep was injected, resulting in a response time of ~2.5-5.0 seconds.

This timing side-channel allowed us to exfiltrate data character by character.

## Phase 5: Flag Extraction

## Additional Findings
- The Lambda function contained a custom environment variable `PYD` which was empty.
- The Lambda handler located in `/var/task` contained only 1 file.
- The timing oracle technique developed here can be utilized to extract any data from the Lambda function's filesystem.
