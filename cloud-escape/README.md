<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=36&duration=2500&pause=800&color=00C7B7&center=true&vCenter=true&width=800&height=80&lines=Cloud+Escape+Writeups;CTF+2026+Documentation+Hub" alt="Typing SVG" />

  <p>
    <img src="https://img.shields.io/badge/Stage%201-Solved-2EA44F?style=for-the-badge" alt="s1" />
    <img src="https://img.shields.io/badge/Stage%202-Deep+Mapped-yellow?style=for-the-badge" alt="s2" />
    <img src="https://img.shields.io/badge/Team-Agent+freecandy-F79211?style=for-the-badge" alt="team" />
  </p>
</div>

---

## Navigation

<table>
  <tr>
    <td width="50%" valign="top">

### Stage 1 — Have Some Faith
**100 PTS** · Flag **captured**

| Link | What |
|:---|:---|
| [Full writeup](Stage_1_Have_Some_Faith.md) | OIDC wildcard, injection, DNS exfil |
| Flag | `1a1jelrlfg2yi2s0` |

    </td>
    <td width="50%" valign="top">

### Stage 2 — Miss Me Yet?
**200 PTS** · Flag **pending**

| Link | What |
|:---|:---|
| [Full writeup](Stage_2_Miss_Me_Yet.md) | Attack methodology |
| [Deep enumeration](Stage2_Deep_Enumeration.md) | Secrets · hints · logs · runtime |
| [AWS environment map](Stage2_AWS_Environment.md) | Full allow/deny matrix |
| Flag | `[NOT CAPTURED]` |

    </td>
  </tr>
</table>

### Campaign

| Link | What |
|:---|:---|
| [WRITEUP.md](WRITEUP.md) | Combined short narrative |
| [../README.md](../README.md) | Master hub (animated) |

---

## Stage 2 at a glance

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart LR
    P[Participant STS] --> L[log bucket]
    P --> C[code_exec]
    C --> V[Lambda VPC + VPCe]
    V --> S[user bucket / flag.txt]
    CF[CloudFront site] --> S
    S -.->|CloudTrail| L
```

| Asset | Value |
|:---|:---|
| Test site | `https://d4ysu55xg7wfi.cloudfront.net/` |
| code_exec | `…/dev/code_exec` |
| User bucket | `userd8a2f72fe43094e8` |
| Log bucket | `logd8a2f72fe43094e8` |

> [!WARNING]
> Do **not** submit `00000000000000000000`.  
> Stage 2 requires **participant STS**, not Stage 1 `cicdRole` OIDC (API denies cicdRole).

---

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3000&pause=1000&color=F79211&center=true&vCenter=true&width=600&height=35&lines=Agent+freecandy+%E2%80%A2+Cloud+Escape+CTF+2026" alt="footer" />
</div>
