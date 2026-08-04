<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=36&duration=2600&pause=900&color=F79211&center=true&vCenter=true&width=860&height=90&lines=Stage+2+Deep+Enumeration;Secrets+%C2%B7+Hints+%C2%B7+Runtime+Intel;Miss+Me+Yet%3F" alt="Typing SVG" />

  <p>
    <img src="https://img.shields.io/badge/Stage%202-Deep+Enum-F79211?style=for-the-badge" alt="s2" />
    <img src="https://img.shields.io/badge/Flag-NOT+CAPTURED-yellow?style=for-the-badge" alt="flag" />
    <img src="https://img.shields.io/badge/Account-121774052880-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="acct" />
  </p>
</div>

---

> [!NOTE]
> Live recon as `ctf_participant_role`. No invented flags. Do **not** submit `000000…`.  
> Canonical consolidation: **[Stage2_Technical_Report.md](Stage2_Technical_Report.md)**.

## Latest network findings (pivot)

| Probe from `code_exec` | Result |
|:---|:---|
| IMDS `169.254.169.254` | **Connection refused** — no `vpc-xxxx` recovery |
| STS endpoint | Unreachable |
| Path-style S3 | Reaches S3 via VPCe → HTTP **403** (wrong UA) |
| Virtual-hosted S3 DNS | Fail |
| Hyperplane | DNS/GW `169.254.100.5` · src `169.254.100.6` · iface `vint_runtime` |
| Log successes | **0** successful data-plane events in large samples |
| Doctrine | Stop blind multi-k UA spray; residual is exact Stmt2 UA |

## Campaign assets

| Asset | Value |
|:---|:---|
| Test site | [`d4ysu55xg7wfi.cloudfront.net`](https://d4ysu55xg7wfi.cloudfront.net/) |
| code_exec | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| User bucket | `userd8a2f72fe43094e8` |
| Log bucket | `logd8a2f72fe43094e8` |
| VPCe (logs) | `vpce-04104ef3d57a26557` · ENI `10.0.0.29` |

![Stage 2 Attack & Audit Traffic Flow (Animated Recon Map)](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA3MDAgNDYwIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIj4KICA8ZGVmcz4KICAgIDwhLS0gR2xvd2luZyBmaWx0ZXIgZm9yIG5lb24gY3lhbiBlZmZlY3QgLS0+CiAgICA8ZmlsdGVyIGlkPSJnbG93LWN5YW4iIHg9Ii0yMCUiIHk9Ii0yMCUiIHdpZHRoPSIxNDAlIiBoZWlnaHQ9IjE0MCUiPgogICAgICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIzIiByZXN1bHQ9ImJsdXIiIC8+CiAgICAgIDxmZUNvbXBvc2l0ZSBpbj0iU291cmNlR3JhcGhpYyIgaW4yPSJibHVyIiBvcGVyYXRvcj0ib3ZlciIgLz4KICAgIDwvZmlsdGVyPgogICAgPCEtLSBHbG93aW5nIGZpbHRlciBmb3IgbmVvbiBvcmFuZ2UgZWZmZWN0IC0tPgogICAgPGZpbHRlciBpZD0iZ2xvdy1vcmFuZ2UiIHg9Ii0yMCUiIHk9Ii0yMCUiIHdpZHRoPSIxNDAlIiBoZWlnaHQ9IjE0MCUiPgogICAgICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIzIiByZXN1bHQ9ImJsdXIiIC8+CiAgICAgIDxmZUNvbXBvc2l0ZSBpbj0iU291cmNlR3JhcGhpYyIgaW4yPSJibHVyIiBvcGVyYXRvcj0ib3ZlciIgLz4KICAgIDwvZmlsdGVyPgogICAgPCEtLSBBcnJvd2hlYWRzIC0tPgogICAgPG1hcmtlciBpZD0iYXJyb3ctY3lhbiIgdmlld0JveD0iMCAwIDEwIDEwIiByZWZYPSI2IiByZWZZPSI1IiBtYXJrZXJXaWR0aD0iNiIgbWFya2VySGVpZ2h0PSI2IiBvcmllbnQ9ImF1dG8tc3RhcnQtcmV2ZXJzZSI+CiAgICAgIDxwYXRoIGQ9Ik0gMCAxIEwgMTAgNSBMIDAgOSB6IiBmaWxsPSIjMDBDN0I3IiAvPgogICAgPC9tYXJrZXI+CiAgICA8bWFya2VyIGlkPSJhcnJvdy1vcmFuZ2UiIHZpZXdCb3g9IjAgMCAxMCAxMCIgcmVmWD0iNiIgcmVmWT0iNSIgbWFya2VyV2lkdGg9IjYiIG1hcmtlckhlaWdodD0iNiIgb3JpZW50PSJhdXRvLXN0YXJ0LXJldmVyc2UiPgogICAgICA8cGF0aCBkPSJNIDAgMSBMIDEwIDUgTCAwIDkgeiIgZmlsbD0iI0ZGOTkwMCIgLz4KICAgIDwvbWFya2VyPgogICAgPG1hcmtlciBpZD0iYXJyb3ctYmx1ZSIgdmlld0JveD0iMCAwIDEwIDEwIiByZWZYPSI2IiByZWZZPSI1IiBtYXJrZXJXaWR0aD0iNiIgbWFya2VySGVpZ2h0PSI2IiBvcmllbnQ9ImF1dG8tc3RhcnQtcmV2ZXJzZSI+CiAgICAgIDxwYXRoIGQ9Ik0gMCAxIEwgMTAgNSBMIDAgOSB6IiBmaWxsPSIjM0I4MkY2IiAvPgogICAgPC9tYXJrZXI+CiAgPC9kZWZzPgoKICA8c3R5bGU+CiAgICB0ZXh0IHsKICAgICAgZm9udC1mYW1pbHk6ICdDb3VyaWVyIE5ldycsIENvdXJpZXIsIG1vbm9zcGFjZSwgc2Fucy1zZXJpZjsKICAgICAgZm9udC1zaXplOiAxM3B4OwogICAgICBmb250LXdlaWdodDogNzAwOwogICAgICBmaWxsOiAjRTZFREYzOwogICAgICB0ZXh0LWFuY2hvcjogbWlkZGxlOwogICAgICBkb21pbmFudC1iYXNlbGluZTogbWlkZGxlOwogICAgfQoKICAgIC5zdWJ0ZXh0IHsKICAgICAgZm9udC1zaXplOiAxMHB4OwogICAgICBmb250LXdlaWdodDogYm9sZDsKICAgICAgZmlsbDogIzhCOTQ5RTsKICAgIH0KCiAgICAvKiBCYWNrZ3JvdW5kIHBhbmVsIHN0eWxpbmcgKi8KICAgIC5iZy1wYW5lbCB7CiAgICAgIGZpbGw6ICMwRDExMTc7CiAgICAgIHN0cm9rZTogIzMwMzYzRDsKICAgICAgc3Ryb2tlLXdpZHRoOiAxLjU7CiAgICAgIHJ4OiAxMjsKICAgIH0KCiAgICAvKiBCb3ggbm9kZXMgKi8KICAgIC5ub2RlLWJveCB7CiAgICAgIGZpbGw6ICMxNjFCMjI7CiAgICAgIHN0cm9rZTogIzMwMzYzRDsKICAgICAgc3Ryb2tlLXdpZHRoOiAyOwogICAgICByeDogODsKICAgIH0KCiAgICAubm9kZS1jeWFuIHsKICAgICAgc3Ryb2tlOiAjMDBDN0I3OwogICAgfQoKICAgIC5ub2RlLW9yYW5nZSB7CiAgICAgIHN0cm9rZTogI0ZGOTkwMDsKICAgIH0KCiAgICAubm9kZS1ibHVlIHsKICAgICAgc3Ryb2tlOiAjM0I4MkY2OwogICAgfQoKICAgIC8qIEZsb3cgbGluZSBhbmltYXRpb25zIC0gbWFyY2hpbmcgZGFzaGVzICovCiAgICBAa2V5ZnJhbWVzIGZsb3ctZG93biB7CiAgICAgIGZyb20geyBzdHJva2UtZGFzaG9mZnNldDogMjQ7IH0KICAgICAgdG8geyBzdHJva2UtZGFzaG9mZnNldDogMDsgfQogICAgfQoKICAgIEBrZXlmcmFtZXMgZmxvdy1hdWRpdCB7CiAgICAgIGZyb20geyBzdHJva2UtZGFzaG9mZnNldDogMjQ7IH0KICAgICAgdG8geyBzdHJva2UtZGFzaG9mZnNldDogMDsgfQogICAgfQoKICAgIEBrZXlmcmFtZXMgcHVsc2UtYm94IHsKICAgICAgMCUsIDEwMCUgeyBvcGFjaXR5OiAxOyBmaWx0ZXI6IGRyb3Atc2hhZG93KDAgMCA0cHggcmdiYSgwLCAxOTksIDE4MywgMC40KSk7IH0KICAgICAgNTAlIHsgb3BhY2l0eTogMC44NTsgZmlsdGVyOiBkcm9wLXNoYWRvdygwIDAgMTBweCByZ2JhKDAsIDE5OSwgMTgzLCAwLjgpKTsgfQogICAgfQoKICAgIEBrZXlmcmFtZXMgcHVsc2Utb3JhbmdlIHsKICAgICAgMCUsIDEwMCUgeyBvcGFjaXR5OiAxOyBmaWx0ZXI6IGRyb3Atc2hhZG93KDAgMCA0cHggcmdiYSgyNTUsIDE1MywgMCwgMC40KSk7IH0KICAgICAgNTAlIHsgb3BhY2l0eTogMC44NTsgZmlsdGVyOiBkcm9wLXNoYWRvdygwIDAgMTBweCByZ2JhKDI1NSwgMTUzLCAwLCAwLjgpKTsgfQogICAgfQoKICAgIC5hbmltYXRlZC1wYXRoLWN5YW4gewogICAgICBmaWxsOiBub25lOwogICAgICBzdHJva2U6ICMwMEM3Qjc7CiAgICAgIHN0cm9rZS13aWR0aDogMi4yOwogICAgICBzdHJva2UtZGFzaGFycmF5OiA4IDQ7CiAgICAgIGFuaW1hdGlvbjogZmxvdy1kb3duIDEuMnMgbGluZWFyIGluZmluaXRlOwogICAgfQoKICAgIC5hbmltYXRlZC1wYXRoLWJsdWUgewogICAgICBmaWxsOiBub25lOwogICAgICBzdHJva2U6ICMzQjgyRjY7CiAgICAgIHN0cm9rZS13aWR0aDogMjsKICAgICAgc3Ryb2tlLWRhc2hhcnJheTogNiA0OwogICAgICBhbmltYXRpb246IGZsb3ctZG93biAxLjVzIGxpbmVhciBpbmZpbml0ZTsKICAgIH0KCiAgICAuYW5pbWF0ZWQtcGF0aC1vcmFuZ2UgewogICAgICBmaWxsOiBub25lOwogICAgICBzdHJva2U6ICNGRjk5MDA7CiAgICAgIHN0cm9rZS13aWR0aDogMjsKICAgICAgc3Ryb2tlLWRhc2hhcnJheTogNSA1OwogICAgICBhbmltYXRpb246IGZsb3ctYXVkaXQgMS44cyBsaW5lYXIgaW5maW5pdGU7CiAgICB9CgogICAgLnB1bHNlLXRhcmdldCB7CiAgICAgIGFuaW1hdGlvbjogcHVsc2UtYm94IDNzIGVhc2UtaW4tb3V0IGluZmluaXRlOwogICAgfQoKICAgIC5wdWxzZS1sb2cgewogICAgICBhbmltYXRpb246IHB1bHNlLW9yYW5nZSAzcyBlYXNlLWluLW91dCBpbmZpbml0ZTsKICAgIH0KCiAgICAvKiBMYWJlbCBiYWRnZXMgb24gbGluZXMgKi8KICAgIC5iYWRnZS1iZyB7CiAgICAgIGZpbGw6ICMxNjFCMjI7CiAgICAgIHN0cm9rZTogIzMwMzYzRDsKICAgICAgc3Ryb2tlLXdpZHRoOiAxOwogICAgICByeDogNDsKICAgIH0KICAgIC5iYWRnZS10ZXh0IHsKICAgICAgZm9udC1zaXplOiAxMHB4OwogICAgICBmaWxsOiAjRkY5OTAwOwogICAgICBmb250LXdlaWdodDogNzAwOwogICAgfQogIDwvc3R5bGU+CgogIDwhLS0gT3V0ZXIgYmFja2dyb3VuZCBjb250YWluZXIgLS0+CiAgPHJlY3QgY2xhc3M9ImJnLXBhbmVsIiB4PSIxMCIgeT0iMTAiIHdpZHRoPSI2ODAiIGhlaWdodD0iNDQwIiAvPgoKICA8IS0tIFRJVExFIC0tPgogIDx0ZXh0IHg9IjM1MCIgeT0iMzgiIHN0eWxlPSJmb250LXNpemU6IDE0cHg7IGZpbGw6ICM1OEE2RkY7Ij7imqEgU1RBR0UgMiBBVFRBQ0sgJmFtcDsgQVVESVQgVFJBRkZJQyBGTE9XIChBTklNQVRFRCBSRUNPTiBNQVApIOKaoTwvdGV4dD4KCiAgPCEtLSBDT05ORUNUSU5HIEZMT1cgTElORVMgKGRyYXduIGJlaGluZCBib3hlcykgLS0+CgogIDwhLS0gUGFydGljaXBhbnQgU1RTIC0+IGNvZGVfZXhlYyAodmVydGljYWwgZHJvcCkgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtY3lhbiIgbWFya2VyLWVuZD0idXJsKCNhcnJvdy1jeWFuKSIgZD0iTSAyMjAgOTQgTCAyMjAgMTI2IiAvPgoKICA8IS0tIFBhcnRpY2lwYW50IFNUUyAtPiBsb2cgYnVja2V0IFJFQUQgKGxvbmcgdmVydGljYWwgZG93bi1yaWdodCBjdXJ2ZSkgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtb3JhbmdlIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93LW9yYW5nZSkiIGQ9Ik0gMTcwIDk0IEwgMTcwIDM0MCBRIDE3MCAzODAgMjMwIDM4MCBMIDI2OCAzODAiIC8+CgogIDwhLS0gY29kZV9leGVjIC0+IExhbWJkYSBWUEMgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtY3lhbiIgbWFya2VyLWVuZD0idXJsKCNhcnJvdy1jeWFuKSIgZD0iTSAyMjAgMTc0IEwgMjIwIDIwNiIgLz4KCiAgPCEtLSBMYW1iZGEgVlBDIC0+IHBhdGgtc3R5bGUgUzMgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtY3lhbiIgbWFya2VyLWVuZD0idXJsKCNhcnJvdy1jeWFuKSIgZD0iTSAyMjAgMjU0IEwgMjIwIDI4NiIgLz4KCiAgPCEtLSBwYXRoLXN0eWxlIFMzIC0+IHVzZXIgYnVja2V0IChob3Jpem9udGFsIGFycm93IHJpZ2h0KSAtLT4KICA8cGF0aCBjbGFzcz0iYW5pbWF0ZWQtcGF0aC1jeWFuIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93LWN5YW4pIiBkPSJNIDMwMCAzMTAgTCA0MTYgMzEwIiAvPgoKICA8IS0tIHBhdGgtc3R5bGUgUzMgLT4gbG9nIGJ1Y2tldCBSRUFEIChmYWlsZWQvZGVuaWVkIGFjY2VzcyBsb2cgcGF0aCkgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtYmx1ZSIgbWFya2VyLWVuZD0idXJsKCNhcnJvdy1ibHVlKSIgZD0iTSAyMjAgMzMyIEwgMjIwIDM2NSBRIDIyMCAzODAgMjY4IDM4MCIgLz4KCiAgPCEtLSBDbG91ZEZyb250IC0+IHVzZXIgYnVja2V0IC0tPgogIDxwYXRoIGNsYXNzPSJhbmltYXRlZC1wYXRoLWN5YW4iIG1hcmtlci1lbmQ9InVybCgjYXJyb3ctY3lhbikiIGQ9Ik0gNTAwIDI1NCBMIDUwMCAyODYiIC8+CgogIDwhLS0gdXNlciBidWNrZXQgLS4tPiBDbG91ZFRyYWlsIC0+IGxvZyBidWNrZXQgLS0+CiAgPHBhdGggY2xhc3M9ImFuaW1hdGVkLXBhdGgtb3JhbmdlIiBtYXJrZXItZW5kPSJ1cmwoI2Fycm93LW9yYW5nZSkiIGQ9Ik0gNTAwIDMzMiBMIDUwMCAzODAgTCA0NDIgMzgwIiAvPgoKICA8IS0tIEFVRElUIFRSQUZGSUMgTEFCRUwgQkFER0UgLS0+CiAgPHJlY3QgY2xhc3M9ImJhZGdlLWJnIiB4PSI0NjAiIHk9IjM0OCIgd2lkdGg9IjgwIiBoZWlnaHQ9IjIwIiAvPgogIDx0ZXh0IGNsYXNzPSJiYWRnZS10ZXh0IiB4PSI1MDAiIHk9IjM1OSI+Q2xvdWRUcmFpbDwvdGV4dD4KCiAgPCEtLSBOT0RFUyAoQk9YRVMpIC0tPgoKICA8IS0tIDEuIFBhcnRpY2lwYW50IFNUUyAtLT4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxNDAsIDUwKSI+CiAgICA8cmVjdCBjbGFzcz0ibm9kZS1ib3ggbm9kZS1jeWFuIiB3aWR0aD0iMTYwIiBoZWlnaHQ9IjQ0IiAvPgogICAgPHRleHQgeD0iODAiIHk9IjIyIj5QYXJ0aWNpcGFudCBTVFM8L3RleHQ+CiAgPC9nPgoKICA8IS0tIDIuIGNvZGVfZXhlYyBTaWdWNCAtLT4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxNDAsIDEzMCkiPgogICAgPHJlY3QgY2xhc3M9Im5vZGUtYm94IG5vZGUtY3lhbiIgd2lkdGg9IjE2MCIgaGVpZ2h0PSI0NCIgLz4KICAgIDx0ZXh0IHg9IjgwIiB5PSIyMiI+Y29kZV9leGVjIFNpZ1Y0PC90ZXh0PgogIDwvZz4KCiAgPCEtLSAzLiBMYW1iZGEgVlBDIC0tPgogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE0MCwgMjEwKSI+CiAgICA8cmVjdCBjbGFzcz0ibm9kZS1ib3ggbm9kZS1jeWFuIiB3aWR0aD0iMTYwIiBoZWlnaHQ9IjQ0IiAvPgogICAgPHRleHQgeD0iODAiIHk9IjIyIj5MYW1iZGEgVlBDPC90ZXh0PgogIDwvZz4KCiAgPCEtLSA0LiBwYXRoLXN0eWxlIFMzIC0tPgogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE0MCwgMjg4KSI+CiAgICA8cmVjdCBjbGFzcz0ibm9kZS1ib3ggbm9kZS1jeWFuIHB1bHNlLXRhcmdldCIgd2lkdGg9IjE2MCIgaGVpZ2h0PSI0NCIgLz4KICAgIDx0ZXh0IHg9IjgwIiB5PSIxOCI+cGF0aC1zdHlsZSBTMzwvdGV4dD4KICAgIDx0ZXh0IGNsYXNzPSJzdWJ0ZXh0IiB4PSI4MCIgeT0iMzMiPlVOU0lHTkVEIHZpYSBWUENlPC90ZXh0PgogIDwvZz4KCiAgPCEtLSA1LiBDbG91ZEZyb250IC0tPgogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQyMCwgMjEwKSI+CiAgICA8cmVjdCBjbGFzcz0ibm9kZS1ib3ggbm9kZS1ibHVlIiB3aWR0aD0iMTYwIiBoZWlnaHQ9IjQ0IiAvPgogICAgPHRleHQgeD0iODAiIHk9IjIyIj5DbG91ZEZyb250PC90ZXh0PgogIDwvZz4KCiAgPCEtLSA2LiB1c2VyIGJ1Y2tldCAtLT4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MjAsIDI4OCkiPgogICAgPHJlY3QgY2xhc3M9Im5vZGUtYm94IG5vZGUtY3lhbiBwdWxzZS10YXJnZXQiIHdpZHRoPSIxNjAiIGhlaWdodD0iNDQiIC8+CiAgICA8dGV4dCB4PSI4MCIgeT0iMTgiPnVzZXIgYnVja2V0PC90ZXh0PgogICAgPHRleHQgY2xhc3M9InN1YnRleHQiIHg9IjgwIiB5PSIzMyI+dXNlcmQ4YS4uLiAvIGZsYWcudHh0PC90ZXh0PgogIDwvZz4KCiAgPCEtLSA3LiBsb2cgYnVja2V0IFJFQUQgLS0+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjcwLCAzNTYpIj4KICAgIDxyZWN0IGNsYXNzPSJub2RlLWJveCBub2RlLW9yYW5nZSBwdWxzZS1sb2ciIHdpZHRoPSIxNzAiIGhlaWdodD0iNDgiIC8+CiAgICA8dGV4dCB4PSI4NSIgeT0iMTkiIHN0eWxlPSJmaWxsOiAjRkY5OTAwOyI+bG9nIGJ1Y2tldCBSRUFEPC90ZXh0PgogICAgPHRleHQgY2xhc3M9InN1YnRleHQiIHg9Ijg1IiB5PSIzNSI+czM6Ly9sb2dkOGEuLi4vdXNlcmQ4YS4uLjwvdGV4dD4KICA8L2c+CgogIDwhLS0gRk9PVEVSIExFR0VORCAtLT4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MCwgNDIyKSI+CiAgICA8IS0tIEN5YW4gbGluZSAtLT4KICAgIDxsaW5lIHgxPSIwIiB5MT0iOCIgeDI9IjI4IiB5Mj0iOCIgY2xhc3M9ImFuaW1hdGVkLXBhdGgtY3lhbiIgLz4KICAgIDx0ZXh0IHg9Ijg1IiB5PSI5IiBzdHlsZT0iZm9udC1zaXplOiAxMXB4OyBmaWxsOiAjOEI5NDlFOyI+RGF0YSAvIFByb2JlczwvdGV4dD4KICAgIDwhLS0gT3JhbmdlIGxpbmUgLS0+CiAgICA8bGluZSB4MT0iMTYwIiB5MT0iOCIgeDI9IjE4OCIgeTI9IjgiIGNsYXNzPSJhbmltYXRlZC1wYXRoLW9yYW5nZSIgLz4KICAgIDx0ZXh0IHg9IjI2MCIgeT0iOSIgc3R5bGU9ImZvbnQtc2l6ZTogMTFweDsgZmlsbDogIzhCOTQ5RTsiPkNsb3VkVHJhaWwgQXVkaXQgRmxvdzwvdGV4dD4KICAgIDwhLS0gQmx1ZSBsaW5lIC0tPgogICAgPGxpbmUgeDE9IjM0MCIgeTE9IjgiIHgyPSIzNjgiIHkyPSI4IiBjbGFzcz0iYW5pbWF0ZWQtcGF0aC1ibHVlIiAvPgogICAgPHRleHQgeD0iNDQ1IiB5PSI5IiBzdHlsZT0iZm9udC1zaXplOiAxMXB4OyBmaWxsOiAjOEI5NDlFOyI+Q2xvdWRGcm9udCAvIERlbnk8L3RleHQ+CiAgPC9nPgo8L3N2Zz4K)

---

## 1. CloudFront surface

| Path | Status | Size | Note |
|:---|:---:|---:|:---|
| `/` · `index.html` | **200** | 1972 | Narrative + title `???` |
| `/docs.html` | **200** | 3099 | **Leaked dual-statement policy** |
| `/junior_developer.png` | **200** | 3,052,187 | Clean PNG · no post-IEND payload |
| `/flag.txt` | **403** | 263 | Exists / gated (not 404) |
| Other guesses (`.git`, `secret`, `.env`, …) | **404** | — | Missing |

### Site narrative (hints)

> I worked hard on this site, but I had a lot of fun doing it!  
> I made sure not to include any secret information here—pretty sure I deleted it all.

<details>
<summary><b>Leaked bucket policy structure (REDACTED values)</b></summary>

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["…/index.html", "…/docs.html", "…/junior_developer.png", "bucket"],
      "Condition": { "StringEquals": { "aws:UserAgent": "REDACTED" } }
    },
    {
      "Sid": "Statement2",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["bucket/*", "bucket"],
      "Condition": {
        "StringEquals": {
          "aws:SourceVpc": "REDACTED",
          "aws:UserAgent": "REDACTED"
        }
      }
    }
  ]
}
```

| Field | Observation |
|:---|:---|
| Operators | `StringEquals` only (no `StringLike`) |
| SourceVpce | **Not** in leaked HTML |
| Stmt2 | **AND** of SourceVpc + UserAgent on `/*` (includes flag) |

</details>

---

## 2. Log forensics (sampled ~140 events)

### Layout

```text
logd8a2f72fe43094e8/userd8a2f72fe43094e8/<ApiName>/<timestamp>.json
```

| Metric | Value |
|:---|:---|
| Success-like (no `errorCode`) | **0** |
| Dominant VPCe | `vpce-04104ef3d57a26557` |
| Dominant ENI IP | `10.0.0.29` |

### API mix

| API | Count | API | Count |
|:---|---:|:---|---:|
| GetObject | 80 | SelectObjectContent | 6 |
| ListObjects | 13 | PutObject | 5 |
| ListObjectVersions | 13 | HeadObject | 4 |
| GetObjectAcl / Tagging | 7 each | Copy / Restore / Attr | few |

### Principals

| Count | Principal |
|---:|:---|
| 85 | anonymous |
| 50 | `ctf_participant_role/d6d7ee068aa0` |
| 3 | `lambdaRole/user_function` |
| 1 | CognitoIdentityCredentials |
| 1 | cicdRole/GitHubActions |

### Keys requested

| Count | Key |
|---:|:---|
| 53 | `flag.txt` |
| 45 | `index.html` |
| 2–3 | docs/png/secret probes, put/copy tests |

### Top User-Agents (intel)

| Count | UA |
|---:|:---|
| 27 | `Amazon CloudFront` |
| 13+ | Full Boto3/Botocore strings (Windows/Linux) |
| 6 | `aws-internal/3`, `AWS Internal`, `Python-urllib/3.1x`, empty, narrative tokens |

> Anonymous GetObject with UA `Amazon CloudFront` via VPCe still **Access Denied** → that string is **not** the secret Statement2 UA (or not sufficient alone).

---

## 3. code_exec runtime

| Probe | Result |
|:---|:---|
| Smoke pass / fail | True / False |
| Handler only file, **571 bytes** | True |
| Function name `user_function` | True |
| No FLAG/secret env | True |
| `s3.us-east-1.amazonaws.com` DNS | True |
| `{bucket}.s3…` DNS | **Fails** (use path-style) |
| Path-style UNSIGNED → 403 | True (reaches S3) |
| lambdaRole signed GetObject | **identity** deny |
| Lambda list log bucket | deny |
| IMDS | blocked |

**Handler:** pure `base64` + `exec` sandbox — no embedded UA/flag/bucket secrets.

---

## 4. Secrets & hints board

| # | Finding | Type | Relevance |
|---:|:---|:---|:---|
| 1 | Dual-statement redacted policy | Hint | Stmt1 UA · Stmt2 VPC+UA |
| 2 | “pretty sure I deleted it all” | Hint | Versioning hypothesis |
| 3 | Title `???` | Hint | Possible UA joke/literal |
| 4 | CF `flag.txt` 403 ≠ 404 | Intel | Object exists |
| 5 | Log read + code_exec only | Access | Designed foothold |
| 6 | Path-style required in Lambda | Intel | DNS trap avoided |
| 7 | Do not sign as lambdaRole | Intel | Use UNSIGNED |
| 8 | CF UA ≠ Stmt2 secret | Intel | Falsified under VPCe |
| 9 | cicdRole ≠ Stage2 code_exec | Intel | Use participant STS |
| 10 | 0 success data events | Intel | No free UA leak yet |
| 11 | PNG clean (no stego payload) | Negative | Visual only |
| 12 | Handler has no secrets | Intel | Policy is elsewhere |

---

## 5. Account map

```text
121774052880  participant + lambdaRole
009661764077  Stage1 cicdRole (OIDC corgi) — not Stage2 API
186769093912  user-bucket owner (CloudTrail recipient)
```

---

## 6. Next steps

1. Participant STS → code_exec only  
2. Path-style UNSIGNED `GetObject flag.txt` + recovered UA  
3. Boolean oracle → real flag  
4. Never submit placeholder zeros  

---

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3000&pause=1000&color=00C7B7&center=true&vCenter=true&width=640&height=35&lines=Agent+freecandy+%E2%80%A2+Cloud+Escape+CTF+2026" alt="footer" />
</div>
