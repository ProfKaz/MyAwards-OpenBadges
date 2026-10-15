# MyAwards-OpenBadges

A collection of independently verifiable professional-credential references and experimental Open Badges 2.0 representations.

## Important distinction

Microsoft Learn is the authoritative verification source for Microsoft certifications. Any Open Badges 2.0 assertions published by this repository are **self-issued personal records**, not Microsoft-issued Open Badges. Do not treat the repository itself as proof of a Microsoft-issued Open Badge.

## Initial credential

- Microsoft 365 Certified: Administrator Expert (MS-102)
- [Verify original Microsoft Learn credential](https://learn.microsoft.com/api/credentials/share/en-us/ProfKaz/3676BA541D04BB6A?sharingId=MVP_473744)

## Planned structure

- `assets/`: original credential images
- `config.json`: credential inventory and original verification URLs
- `build.py`: builds hosted OB2 JSON-LD and baked PNGs
- `docs/`: GitHub Pages output, including `issuer/`, `badges/`, `assertions/`, and `assets/`

The publishing workflow is being prepared. GitHub Pages is not yet enabled. Acceptance by Sessionize is not guaranteed because the original Microsoft Learn credential is not an issuer-signed Open Badges 2.0 assertion.
