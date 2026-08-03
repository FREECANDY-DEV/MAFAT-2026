# Cloud Escape CTF 2026 - Combined Writeup

This document serves as the combined summary of our approaches and solutions for Stage 1 and Stage 2 of the Cloud Escape CTF.

## Stage 1: Have Some Faith
In the first stage, we exploited a misconfigured OIDC trust policy allowing cross-repository access. After assuming the CI/CD role, we discovered a command injection vulnerability in an internal Lambda function (`nslookupv2`). Due to the Lambda's network isolation, we exfiltrated the flag using a DNS side-channel via the VPC's Route 53 resolver.

**[Read the full Stage 1 Writeup here](WRITEUP_STAGE1.md)**

## Stage 2: Miss Me Yet?
In the second stage, we encountered a restricted code execution Lambda and S3 buckets protected by strict `UserAgent` and `SourceVpc` policies. We bypassed the policy using `boto3` header injection. Because the Lambda suppressed all output and lacked VPC endpoints for direct AWS API interactions , didn't got the flag yet 

**[Read the full Stage 2 Writeup here](WRITEUP_STAGE2.md)**
