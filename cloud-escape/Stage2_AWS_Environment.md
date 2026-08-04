<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=34&duration=2500&pause=900&color=00C7B7&center=true&vCenter=true&multiline=true&width=900&height=100&lines=AWS+Environment+Map;ctf_participant_role+%C2%B7+Allow+%2F+Deny+Surface" alt="AWS Environment Map" />

<br/>

<img src="https://img.shields.io/badge/Principal-ctf_participant_role-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=FF9900" alt="Principal" />
<img src="https://img.shields.io/badge/Account-121774052880-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Account" />
<img src="https://img.shields.io/badge/Region-us--east--1-00C7B7?style=for-the-badge" alt="Region" />
<img src="https://img.shields.io/badge/ALLOW-5-2EA44F?style=for-the-badge" alt="Allow" />
<img src="https://img.shields.io/badge/DENY-130%2B-critical?style=for-the-badge" alt="Deny" />
<img src="https://img.shields.io/badge/Generated-2026--08--04-6e7681?style=for-the-badge" alt="Generated" />

<br/><br/>

| Related docs |
|:---:|
| [Stage 2 writeup](Stage_2_Miss_Me_Yet.md) · [Deep enumeration](Stage2_Deep_Enumeration.md) · [Campaign hub](../README.md) |

</div>

---

## Executive summary

> [!IMPORTANT]
> As `ctf_participant_role`, the AWS control-plane surface is **intentionally minimal**.  
> The only high-value footholds are:
>
> 1. **Read** audit objects in `logd8a2f72fe43094e8`
> 2. **Invoke** Stage 2 `code_exec` via SigV4 (tested separately from this probe matrix)
>
> All IAM introspection, EC2/VPC describe APIs, Lambda listing, CloudFront admin, Secrets Manager, and direct access to the user / Stage 1 buckets are **denied**.

| Field | Value |
|:---|:---|
| **Assessment type** | Live identity-based surface enumeration |
| **Principal** | `arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0` |
| **Caller account** | `121774052880` |
| **Stage 1 account (cross)** | `009661764077` (`cicdRole` — not assumable from here) |
| **Probe result** | **5 ALLOW** · **134 DENY** |
| **Strategic takeaway** | Stage 2 is not an “enumerate AWS and find the flag” challenge — it is a **two-door** problem: logs + blind code_exec |

<details>
<summary><b>Table of contents</b></summary>

- [1. Identity card](#1-identity-card)
- [2. Multi-account topology](#2-multi-account-topology)
- [3. Trust boundaries & data flow](#3-trust-boundaries--data-flow)
- [4. Effective permission model](#4-effective-permission-model)
- [5. S3 access matrix](#5-s3-access-matrix)
- [6. Log-bucket intelligence](#6-log-bucket-intelligence)
- [7. Service-by-service results](#7-service-by-service-results)
- [8. Cross-identity comparison](#8-cross-identity-comparison)
- [9. Attack-surface conclusions](#9-attack-surface-conclusions)
- [10. Appendix — raw STS identity](#10-appendix--raw-sts-identity)

</details>

---

## 1. Identity card

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#232F3E',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#00C7B7',
    'lineColor': '#FF9900',
    'secondaryColor': '#161E2D',
    'tertiaryColor': '#0D1117'
  }
}}%%
flowchart LR
    PLATFORM["Platform STS issuer"] -->|temporary session| P["ctf_participant_role<br/>session: d6d7ee068aa0"]
    P --> ID["sts:GetCallerIdentity<br/>ALLOW"]
    P --> LOG["s3:ListBucket / GetObject<br/>logd8a2f72fe43094e8 · ALLOW"]
    P --> CE["execute-api · code_exec<br/>ALLOW · SigV4 path"]
    P -.->|DENY| IAM["iam:* introspection"]
    P -.->|DENY| EC2["ec2:Describe*"]
    P -.->|DENY| USER["user bucket direct Get"]
    P -.->|DENY| CICD["sts:AssumeRole cicdRole"]
    P -.->|DENY| LR["sts:AssumeRole lambdaRole"]
```

| Attribute | Observed value |
|:---|:---|
| **UserId** | `AROARYWSMSYIPWMOE25U2:d6d7ee068aa0` |
| **Account** | `121774052880` |
| **ARN** | `arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0` |
| **Session style** | Temporary role session (not long-lived IAM user keys) |
| **Can mint new session tokens** | ❌ `sts:GetSessionToken` denied |
| **Can assume Stage 1 `cicdRole`** | ❌ `AccessDenied` (cross-account `009661764077`) |
| **Can assume `lambdaRole`** | ❌ `AccessDenied` (same account) |

---

## 2. Multi-account topology

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#232F3E',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#FF9900',
    'lineColor': '#00C7B7',
    'secondaryColor': '#161E2D'
  }
}}%%
flowchart TB
    subgraph EXT["PUBLIC EDGE"]
        CF["CloudFront<br/>d4ysu55xg7wfi.cloudfront.net"]
        API["API Gateway<br/>l8ssyaz69f…/dev/code_exec"]
    end

    subgraph A1["ACCOUNT 009661764077 · Stage 1 historical"]
        CICD["cicdRole<br/>GHA OIDC · corgi"]
        NS["nslookupv2 API / Lambda"]
        CODECB["codec4f26c862a321ef5"]
    end

    subgraph A2["ACCOUNT 121774052880 · Stage 2 live"]
        PART["ctf_participant_role<br/>PLAYER STS"]
        LR["lambdaRole<br/>code_exec runtime"]
        USERB["userd8a2f72fe43094e8<br/>flag + site objects"]
        LOGB["logd8a2f72fe43094e8<br/>CloudTrail-style data events"]
        subgraph VPC["Isolated VPC · no NAT / no IGW"]
            L2["Lambda user_function"]
            VPCE["S3 VPC Endpoint<br/>vpce-04104ef3d57a26557<br/>ENI 10.0.0.29"]
            L2 --> VPCE
        end
    end

    CF --> USERB
    PART -->|SigV4| API
    API --> L2
    L2 -.->|path-style S3 · UA + SourceVpc| USERB
    USERB -.->|audit events| LOGB
    PART -->|List / Get objects| LOGB
    CICD -.->|cannot invoke Stage 2 code_exec| API
    PART -.->|AssumeRole DENY| CICD
    PART -.->|AssumeRole DENY| LR
```

### Known Stage assets

| Asset | Value | Role in Stage 2 |
|:---|:---|:---|
| **code_exec API** | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` | Blind Python RCE foothold |
| **Test site** | [d4ysu55xg7wfi.cloudfront.net](https://d4ysu55xg7wfi.cloudfront.net/) | Public edge · policy leak at `/docs.html` |
| **User bucket** | `userd8a2f72fe43094e8` | Flag + site objects (gated) |
| **Log bucket** | `logd8a2f72fe43094e8` | Participant-readable audit trail |
| **S3 VPCe (from logs)** | `vpce-04104ef3d57a26557` | Dominant source of data-plane attempts |
| **VPCe ENI** | `10.0.0.29` | Private path into S3 from Lambda VPC |
| **Stage 1 API (historical)** | `…/dev/nslookupv2` | Not usable for Stage 2 flag |
| **Stage 1 role** | `arn:aws:iam::009661764077:role/cicdRole` | Separate trust domain |

---

## 3. Trust boundaries & data flow

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#161E2D',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#F79211',
    'lineColor': '#F79211'
  }
}}%%
sequenceDiagram
    autonumber
    actor Player as Operator
    participant STS as Platform STS
    participant P as ctf_participant_role
    participant LOG as log bucket
    participant API as code_exec API
    participant L as Lambda / lambdaRole
    participant S3 as user bucket

    Player->>STS: Request temporary session
    STS-->>P: Session keys
    Player->>P: Use session
    P->>LOG: List / Get audit objects (ALLOW)
    LOG-->>Player: Failed GetObject events · VPCe intel
    Player->>API: POST base64 Python (SigV4 as participant)
    API->>L: Invoke in isolated VPC
    L->>S3: path-style GetObject + custom User-Agent
    Note over L,S3: Needs SourceVpc AND User-Agent (Stmt2)
    S3-->>L: 200 only if conditions satisfied
    S3-->>LOG: CloudTrail-style data event
    L-->>API: stdout majority-masked
    API-->>Player: OK / FAIL shell (blind)
```

| Boundary | Crossing allowed? | Notes |
|:---|:---:|:---|
| Internet → CloudFront → public keys | ✅ (with Stmt1 UA) | `index.html`, `docs.html`, image |
| Internet → user bucket as participant | ❌ | Resource / identity deny |
| Participant → log bucket objects | ✅ | Primary recon channel |
| Participant → code_exec | ✅ | Separate SigV4 invoke path |
| Lambda → S3 virtual-hosted | ❌ | DNS failure inside VPC |
| Lambda → S3 path-style via VPCe | 🟡 | Network OK; policy UA still open |
| Participant → `lambdaRole` / `cicdRole` | ❌ | No lateral assume |

---

## 4. Effective permission model

### What this principal can do

```text
 ALLOW surface (probe matrix)
 ┌────────────────────────────────────────────────────────────┐
 │  sts:GetCallerIdentity                                     │
 │  s3:ListBucket   on logd8a2f72fe43094e8                    │
 │  s3:HeadBucket   on logd8a2f72fe43094e8                    │
 │  s3:ListBucket   prefix walk  log…/userd8…/<ApiName>/      │
 │  (+ execute-api invoke code_exec — confirmed outside probe)│
 └────────────────────────────────────────────────────────────┘

 DENY surface (everything else of note)
 ┌────────────────────────────────────────────────────────────┐
 │  iam:* · lambda:List* · apigateway:* · ec2:Describe*       │
 │  cloudfront:List* · logs:* · cloudtrail:* · ssm:*          │
 │  secretsmanager:* · kms:* · dynamodb:* · rds:* · ecs/eks   │
 │  s3:* on user / Stage1 / platform / site buckets           │
 │  sts:AssumeRole · sts:GetSessionToken                      │
 └────────────────────────────────────────────────────────────┘
```

### Permission heat map (by service family)

| Service family | Result | Signal |
|:---|:---:|:---|
| **STS identity** | 🟢 partial | `GetCallerIdentity` only |
| **S3 log bucket** | 🟢 object list/read path | Foothold #1 |
| **S3 user / Stage1 / platform** | 🔴 full deny | No direct flag grab |
| **IAM** | 🔴 full deny | Cannot self-introspect policies |
| **Lambda control plane** | 🔴 deny | Must use API Gateway entry |
| **API Gateway admin** | 🔴 deny | Invoke-only via known URL |
| **EC2 / VPC describe** | 🔴 deny | VPC facts come from **logs + runtime** |
| **CloudFront admin** | 🔴 deny | Public GET only via distribution URL |
| **Secrets / KMS / SSM** | 🔴 deny | No secret store walk |
| **Compute / data plane (ECS, EKS, RDS, DDB)** | 🔴 deny | Out of scope for this identity |
| **execute-api code_exec** | 🟢 (external test) | Foothold #2 |

---

## 5. S3 access matrix

### Bucket-level outcomes

| Bucket | Purpose | `ListBucket` | `HeadBucket` | `GetObject flag.txt` | Verdict |
|:---|:---|:---:|:---:|:---:|:---|
| **`logd8a2f72fe43094e8`** | Audit / data events | ✅ | ✅ | `NoSuchKey` (not present) | **Player log store** |
| **`userd8a2f72fe43094e8`** | Site + flag | ❌ | ❌ 403 | ❌ | **Target — not direct** |
| **`codec4f26c862a321ef5`** | Stage 1 flag store | ❌ | ❌ 403 | ❌ | Historical / out of band |
| **`platform-bucket-009661764077-us-east-1`** | Platform | ❌ | ❌ 403 | ❌ | Cross-account style deny |
| **`site781fe43f26b9eba3`** | Site-related | ❌ | ❌ 403 | ❌ | Denied |

### User bucket — denied control-plane APIs

All of the following returned **AccessDenied / 403** as participant on `userd8a2f72fe43094e8`:

| Category | APIs probed |
|:---|:---|
| Inventory | `ListBucket`, `ListBucketVersions`, `HeadBucket` |
| Policy / ACL | `GetBucketPolicy`, `GetBucketAcl`, `GetBucketOwnershipControls` |
| Config | `GetBucketLocation`, `GetBucketVersioning`, `GetBucketEncryption`, `GetBucketLogging`, `GetBucketTagging`, `GetBucketCORS`, `GetBucketWebsite`, `GetBucketNotification`, `GetPublicAccessBlock` |
| Objects | `GetObject(flag.txt)`, `GetObject(index.html)`, `HeadObject(flag.txt)` |

> Direct participant → user bucket is a dead end. Flag path is **through Lambda + policy conditions**, not through this role’s identity policy.

### Log bucket — allowed vs denied

| Operation | Result | Notes |
|:---|:---:|:---|
| `ListBucket` (root + prefixes) | ✅ | Full API-name tree visible |
| `HeadBucket` | ✅ | Exists + reachable |
| Object GET under known keys | ✅ | Used for forensics (see deep enum) |
| `GetBucketPolicy` / ACL / encryption / … | ❌ | Metadata locked down |
| `GetObject(flag.txt)` | ❌ `NoSuchKey` | Flag is not stored here |

---

## 6. Log-bucket intelligence

Even without EC2 describe rights, the log bucket reconstructs the data-plane topology.

### Prefix taxonomy

```text
s3://logd8a2f72fe43094e8/
└── userd8a2f72fe43094e8/          ← source bucket being audited
    ├── CopyObject/
    ├── GetObject/                 ← majority of events
    ├── GetObjectAcl/
    ├── GetObjectAttributes/
    ├── GetObjectTagging/
    ├── HeadBucket/
    ├── HeadObject/
    ├── ListObjectVersions/
    ├── ListObjects/
    ├── PutObject/
    ├── RestoreObject/
    └── SelectObjectContent/
```

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#232F3E',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#00C7B7',
    'lineColor': '#FF9900'
  }
}}%%
flowchart LR
    subgraph LOG["logd8a2f72fe43094e8 · ALLOW"]
        ROOT["/"] --> SRC["userd8a2f72fe43094e8/"]
        SRC --> G["GetObject/"]
        SRC --> L["ListObjects/"]
        SRC --> V["ListObjectVersions/"]
        SRC --> H["Head* / Put / Select / …"]
    end
    G --> INTEL["VPCe · ENI · errorCode<br/>userAgent · principalId"]
    INTEL --> PLAY["UA oracle · path discovery<br/>0 success events so far"]
```

### What the prefixes prove

| Observation | Implication |
|:---|:---|
| Top-level prefix = user bucket name | Logs are **scoped data events** for that bucket |
| API folders mirror S3 API names | Trail is action-oriented (CloudTrail-like layout) |
| Dominant source `vpce-04104ef3d57a26557` | S3 access from Lambda goes through **one VPCe** |
| ENI `10.0.0.29` | Concrete private path / network footprint |
| **0 success-like events** in sampled set | No one (including us) has satisfied Stmt2 yet |

---

## 7. Service-by-service results

### STS

| Probe | Result | Detail |
|:---|:---:|:---|
| `get_caller_identity` | ✅ ALLOW | Full ARN / account |
| `get_session_token` | ❌ DENY | Cannot refresh as IAM user |
| `assume_role(cicdRole)` | ❌ DENY | Cross-account Stage 1 role |
| `assume_role(lambdaRole)` | ❌ DENY | Cannot steal runtime role |
| `get_access_key_info` | ❌ DENY | — |

### IAM

| Probe | Result |
|:---|:---:|
| `ListRoles` / `ListUsers` / `ListPolicies` | ❌ |
| `GetUser` / `GetRole` | ❌ |
| `ListAttachedRolePolicies` / `ListRolePolicies` | ❌ |
| `SimulatePrincipalPolicy` | ❌ |

> No self-service policy dump. Effective rights must be **inferred from allow/deny probes** and challenge leaks (`docs.html`).

### Lambda / API Gateway (control plane)

| Probe | Result |
|:---|:---:|
| `lambda:ListFunctions` | ❌ |
| `apigateway:GET /restapis` | ❌ |
| `apigatewayv2:GetApis` | ❌ |

Invoke of the **known** `code_exec` URL is a separate data path (SigV4) and is **allowed** for this principal.

### EC2 / networking

| Probe | Result |
|:---|:---:|
| `DescribeVpcs` / `Subnets` / `SecurityGroups` | ❌ |
| `DescribeInstances` / `NetworkInterfaces` | ❌ |
| `DescribeVpcEndpoints` / `RouteTables` | ❌ |
| `DescribeNatGateways` / `InternetGateways` | ❌ |

VPC topology is reconstructed from **runtime + logs**, not from describe APIs.

### CloudFront

| Probe | Result |
|:---|:---:|
| `ListDistributions` | ❌ |

Public edge remains available via the known distribution hostname only.

### Other services (smoke — all DENY)

| Cluster | Probes |
|:---|:---|
| **Secrets plane** | SSM parameters/instances · Secrets Manager · KMS |
| **Data plane** | DynamoDB · RDS · SQS · SNS |
| **Containers** | ECS · EKS · ECR |
| **Observability** | CloudWatch Logs · CloudTrail · EventBridge |
| **Delivery / CI** | CloudFormation · CodeBuild · CodePipeline |
| **Identity pools** | Cognito IdP · Cognito Identity |

---

## 8. Cross-identity comparison

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#232F3E',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#FF9900',
    'lineColor': '#00C7B7'
  }
}}%%
flowchart TB
    subgraph IDs["IDENTITIES IN PLAY"]
        P["ctf_participant_role<br/>Account 121774052880"]
        C["cicdRole<br/>Account 009661764077"]
        L["lambdaRole<br/>inside code_exec"]
    end

    P -->|ALLOW| LOG["Log bucket read"]
    P -->|ALLOW| CE["code_exec invoke"]
    C -->|ALLOW Stage1| NS["nslookupv2"]
    C -->|DENY Stage2| CE
    L -->|network| VPCE["S3 VPCe"]
    L -->|signed S3| IDENY["Identity-based DENY"]
    L -->|UNSIGNED path-style| POL["Bucket policy Stmt2<br/>SourceVpc ∧ User-Agent"]
```

| Capability | Participant | cicdRole (GHA) | lambdaRole (runtime) |
|:---|:---:|:---:|:---:|
| Stage 2 `code_exec` invoke | ✅ | ❌ | n/a |
| Log bucket read | ✅ | ❌ | side-channel only |
| Direct user-bucket GetObject | ❌ | ❌ | needs policy conditions |
| Path-style S3 from VPC | n/a | n/a | ✅ required |
| Virtual-hosted S3 from VPC | n/a | n/a | ❌ DNS fail |
| Assume the other roles | ❌ | n/a | n/a |

---

## 9. Attack-surface conclusions

### Design intent (inferred)

The organizers gave the player a **deliberately starved** IAM principal:

1. **Just enough** to read their own audit trail  
2. **Just enough** to enter the blind execution sandbox  
3. **Nothing** that lets them dump infrastructure or self-read policies  

That forces the real puzzle into:

```text
logs  →  learn VPCe / failures / UA artifacts
code_exec  →  act from SourceVpc
bucket policy Stmt2  →  match User-Agent (unknown)
path-style UNSIGNED  →  avoid lambdaRole identity deny + DNS fail
```

### Operator checklist

| # | Action | Status |
|:---:|:---|:---:|
| 1 | Confirm identity with `GetCallerIdentity` | ✅ |
| 2 | Enumerate log prefixes under `userd8a2f72fe43094e8/` | ✅ |
| 3 | Harvest VPCe / ENI / error codes / user agents | ✅ (deep enum) |
| 4 | Stop wasting probes on IAM/EC2/CF admin APIs | ✅ dead |
| 5 | Invoke `code_exec` only with **participant** STS | ✅ required |
| 6 | From Lambda: path-style S3 + UA search | 🟡 residual |
| 7 | Never submit `000000…` | ⚠️ hard rule |

### Bottom line

| Question | Answer |
|:---|:---|
| Can this role own the AWS account? | **No** — nearly total control-plane deny |
| Can this role read the flag directly? | **No** — user bucket denied |
| Can this role still win Stage 2? | **Yes** — via log intel + `code_exec` + policy match |
| Is GHA `cicdRole` a Stage 2 shortcut? | **No** — invoke denied |

---

## 10. Appendix — raw STS identity

<details>
<summary><b>sts:GetCallerIdentity response (200)</b></summary>

```json
{
  "UserId": "AROARYWSMSYIPWMOE25U2:d6d7ee068aa0",
  "Account": "121774052880",
  "Arn": "arn:aws:sts::121774052880:assumed-role/ctf_participant_role/d6d7ee068aa0",
  "ResponseMetadata": {
    "RequestId": "befeeea3-1e4d-47c7-be97-091a558cbe8f",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "x-amzn-requestid": "befeeea3-1e4d-47c7-be97-091a558cbe8f",
      "x-amz-sts-extended-request-id": "MTp1cy1lYXN0LTE6UzoxNzg1ODMxMTkzMDU4OlI6SmZ2eHdKNlk=",
      "content-type": "text/xml",
      "content-length": "451",
      "date": "Tue, 04 Aug 2026 08:13:13 GMT"
    },
    "RetryAttempts": 0
  }
}
```

</details>

<details>
<summary><b>Full deny catalogue (condensed)</b></summary>

**IAM** — `ListRoles`, `ListUsers`, `ListPolicies`, `GetUser`, `ListAttachedRolePolicies`, `ListRolePolicies`, `GetRole`, `SimulatePrincipalPolicy`  

**S3 (non-log buckets)** — full inventory of list/head/get policy/acl/versioning/cors/website/logging/tagging/encryption/ownership/notification + object get/head on `userd8a2f72fe43094e8`, `codec4f26c862a321ef5`, `platform-bucket-009661764077-us-east-1`, `site781fe43f26b9eba3`  

**S3 (log bucket metadata)** — location, policy, acl, versioning, list versions, public access block, cors, website, logging, tagging, encryption, ownership, notification  

**Lambda / API GW** — `ListFunctions`, REST + HTTP API list  

**EC2** — VPCs, subnets, SGs, instances, VPC endpoints, route tables, NAT, IGW, ENIs  

**CloudFront** — `ListDistributions`  

**Other** — SSM, Secrets Manager, KMS, DynamoDB, RDS, ECS, EKS, ECR, SNS, SQS, EventBridge, Logs, CloudTrail, CloudFormation, CodeBuild, CodePipeline, Cognito IdP, Cognito Identity, `sts:GetAccessKeyInfo`

</details>

---

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3000&pause=1000&color=00C7B7&center=true&vCenter=true&width=700&height=40&lines=5+ALLOW+%C2%B7+134+DENY+%C2%B7+Two+doors+only;logs+%2B+code_exec+%E2%86%92+VPC+%E2%86%92+flag" alt="footer" />

<br/>

**Cloud Escape CTF 2026 · Stage 2 · Environment assessment**  
Agent freecandy · generated from live participant probes

</div>
