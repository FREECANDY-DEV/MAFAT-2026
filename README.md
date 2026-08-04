<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=40&duration=2800&pause=900&color=F79211&center=true&vCenter=true&multiline=true&width=900&height=120&lines=AWS+Cloud+Escape+CTF+2026;Operation+CloudEscape;Agent+freecandy" alt="Typing SVG" />

  <br/>

  <img src="https://img.shields.io/badge/AWS-us--east--1-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/IAM%20%7C%20Lambda%20%7C%20S3%20%7C%20API%20GW-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Services" />
  <img src="https://img.shields.io/badge/Cloud%20Security-OIDC%20%26%20VPC-F79211?style=for-the-badge" alt="Category" />
  <img src="https://img.shields.io/badge/Total-300%20PTS-00C7B7?style=for-the-badge" alt="Points" />

  <br/><br/>

  <img src="https://img.shields.io/badge/Stage%201-CAPTURED-2EA44F?style=for-the-badge" alt="S1" />
  <img src="https://img.shields.io/badge/Stage%202-IN%20PROGRESS-yellow?style=for-the-badge" alt="S2" />
  <img src="https://img.shields.io/badge/Branch-corgi-2088FF?style=for-the-badge&logo=github" alt="branch" />
</div>

---

## Campaign overview

> [!IMPORTANT]
> Official writeup package for **Cloud Escape CTF 2026**. Stage 1 is fully solved and documented. Stage 2 recon is deep-mapped; the live flag is still pending (do **not** submit `000000…`).

<div align="center">

| Stage | Challenge | Pts | Core technique | Status | Docs |
|:---:|:---|:---:|:---|:---:|:---|
| **1** | Have Some Faith | 100 | OIDC wildcard → RCE → DNS exfil | ✅ **Captured** | [Writeup](cloud-escape/Stage_1_Have_Some_Faith.md) |
| **2** | Miss Me Yet? | 200 | Blind code_exec + S3 VPC/UA policy | 🟡 **Mapped** | [Writeup](cloud-escape/Stage_2_Miss_Me_Yet.md) · [Deep enum](cloud-escape/Stage2_Deep_Enumeration.md) |

</div>

---

## Architecture

```mermaid
%%{init: {'theme':'dark', 'themeVariables': { 'primaryColor':'#232F3E','primaryTextColor':'#fff','lineColor':'#F79211','secondaryColor':'#FF9900'}}}%%
flowchart TB
    subgraph S1["Stage 1 — Have Some Faith"]
        GHA["GitHub Actions<br/>branch corgi"]
        OIDC["IAM OIDC Provider"]
        CICD["cicdRole<br/>009661764077"]
        NS["API /dev/nslookupv2"]
        L1["Lambda nslookupv2<br/>VPC + DNS 169.254.169.253"]
        B1["S3 codec…/flag.txt"]
        DNS["External DNS log"]
        GHA --> OIDC --> CICD --> NS --> L1
        L1 --> B1
        L1 --> DNS
    end

    subgraph S2["Stage 2 — Miss Me Yet?"]
        STS["Platform STS<br/>ctf_participant_role"]
        CE["API /dev/code_exec"]
        L2["Lambda user_function<br/>S3 VPCe only"]
        CF["CloudFront test site"]
        BU["userd8a2f72fe43094e8"]
        BL["logd8a2f72fe43094e8"]
        STS --> CE --> L2
        STS --> BL
        CF --> BU
        L2 -.->|path-style UNSIGNED<br/>UA + SourceVpc| BU
        BU -.->|CloudTrail| BL
    end
```

---

## Documentation hub

<div align="center">

| 📘 Document | Description |
|:---|:---|
| **[cloud-escape/README.md](cloud-escape/README.md)** | Animated writeups index |
| **[Stage 1 full writeup](cloud-escape/Stage_1_Have_Some_Faith.md)** | OIDC · injection · DNS tunnel · flag `1a1jelrlfg2yi2s0` |
| **[Stage 2 full writeup](cloud-escape/Stage_2_Miss_Me_Yet.md)** | Methodology · policy · oracles |
| **[Stage 2 deep enumeration](cloud-escape/Stage2_Deep_Enumeration.md)** | Secrets · hints · logs · runtime probes |
| **[Stage 2 AWS env map](cloud-escape/Stage2_AWS_Environment.md)** | Full allow/deny as participant |
| **[Combined summary](cloud-escape/WRITEUP.md)** | Short campaign narrative |

</div>

### Stage 1 result

```text
FLAG = 1a1jelrlfg2yi2s0
```

### Stage 2 status

```text
FLAG = [NOT CAPTURED]
```

> Participant surface is intentionally tiny: **log bucket read** + **code_exec invoke**.  
> Flag path = Lambda VPC + path-style S3 + correct `aws:UserAgent` (Statement2).  
> **cicdRole (GHA OIDC) cannot invoke Stage 2 code_exec** — confirmed.

---

## GitHub Actions

| Workflow | Purpose |
|:---|:---|
| [stage1.yml](.github/workflows/stage1.yml) | OIDC → `cicdRole` → nslookup DNS exfil PoC |
| [stage2.yml](.github/workflows/stage2.yml) | `workflow_dispatch` + **participant STS** → code_exec probes |

---

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3500&pause=1200&color=00C7B7&center=true&vCenter=true&width=700&height=40&lines=Documented+by+Agent+freecandy;Cloud+Escape+CTF+2026;Stay+curious.+Stay+ethical." alt="footer typing" />
</div>
