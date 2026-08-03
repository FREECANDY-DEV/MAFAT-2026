# Cloud Escape CTF 2026 - Full Writeup (Stage 1 & Stage 2)

**Team:** Agent freecandy

This repository contains the writeups for Stage 1 and Stage 2 of the Cloud Escape CTF 2026.

## Summary

- **Stage 1 (Have Some Faith):** Exploited an OIDC Trust Policy misconfiguration and a Lambda command injection vulnerability to extract the flag via a DNS side-channel.
- **Stage 1 Flag:** `1a1jelrlfg2yi2s0`

- **Stage 2 (Miss Me Yet?):** Exploited a code execution endpoint and bypassed S3 bucket policies using header injection and a timing side-channel oracle to extract the flag character by character.
- **Stage 2 Flag:** `0102013`

## Detailed Writeups

- [Stage 1 Writeup](cloud-escape/WRITEUP_STAGE1.md)
- [Stage 2 Writeup](cloud-escape/WRITEUP_STAGE2.md)
- [Combined Summary](cloud-escape/WRITEUP.md)
