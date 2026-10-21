# Reuse MyAwards-OpenBadges

This folder is a **how-to guide for people cloning or forking the project**. **Start with [AI-End-to-End-Workflow.md](AI-End-to-End-Workflow.md)** for the complete first-time user + AI process, including copyable minimum prompts, binary uploads, GitHub Actions, Pages and Credly. Then paste [Prompt-to-use-with-AI.md](Prompt-to-use-with-AI.md) into your assistant.

## What this project does

It creates a publicly hosted, **self-issued Open Badges 2.0 representation** of existing awards or certifications. It does **not** convert the original issuer's credential into an officially issued Open Badge. The original provider's verification page remains authoritative. Acceptance by Credly, Sessionize, or other platforms is not guaranteed.

## Requirements

- A GitHub account and a public repository, with GitHub Pages enabled.
- An authentic credential you are entitled to describe and publish, its official verification URL, and a PNG you may legally reuse.
- Python 3.12+ if building locally; GitHub Actions can build for you.
- A public contact email for the **self-issued** Open Badges issuer profile. The recipient email should match a verified email on your intended platform. Both are published when un-hashed.
- Optional official expiration date, skills and a public reference for those skills.

## Start from a copy

1. Fork or clone this repository into **your account**; do not modify the source owner's credentials.
2. Set **Settings → Pages → Build and deployment → Deploy from a branch → main → /docs**.
3. Replace all owner-specific values in `config.json`: `base_url`, issuer name/URL/email, recipient identity and the entire `records` collection. **Do not keep ProfKaz's MS-102 entry as though it were your own.**
4. Save your *own* original images to `docs/assets/<slug>.png` (e.g. `docs/assets/sc401.png`). The `original_image` value may alternatively point to an existing source PNG elsewhere in the repository.
5. For every record specify `slug`, `title`, `original_image`, `verification_url` and `self_attestation_date` in UTC ISO 8601 format. This last field is the date you issued *your personal record*, **not** the certification award date. Optional: `expires`, `skills`, `skills_source`.
6. Use **Actions → Build Open Badges 2.0 images → Run workflow**, or locally run `python build.py`. Generated files appear in `docs/issuer`, `docs/badges`, `docs/assertions` and `docs/assets`.
7. Check the GitHub Actions run and deployment. After publication, inspect `<base_url>/assertions/<slug>.json`, `<base_url>/badges/<slug>.json` and download `<base_url>/assets/<slug>-openbadges2.png`.
8. Upload the **baked PNG** to a platform that supports Open Badges 2.0 and check the displayed title, issuer, recipient, dates and tags. A hosted assertion may be cached; reimporting or platform support may be necessary to reflect updates.

## Configuration example

```json
{
  "base_url": "https://YOURUSER.github.io/YOURREPO",
  "issuer": {
    "name": "Your Name — personal credential records",
    "url": "https://github.com/YOURUSER",
    "email": "public-contact@example.org"
  },
  "recipient": {
    "type": "email",
    "identity": "verified-recipient@example.org",
    "hashed": false
  },
  "records": [
    {
      "slug": "example",
      "title": "Exact credential title",
      "original_image": "docs/assets/example.png",
      "verification_url": "https://original-issuer.example.org/verify/example",
      "self_attestation_date": "2026-10-20T00:00:00Z",
      "expires": "2027-10-20T00:00:00Z",
      "skills": ["Skill verified by the original issuer"],
      "skills_source": "https://original-issuer.example.org/skills"
    }
  ]
}
```

Do not copy sample dates/claims into real entries. Omit `expires` only when the underlying credential truly has no expiry or when unknown (in which case explain the uncertainty rather than claim perpetual validity). Skills should reflect documented assessment scope, not unsupported personal skill endorsements.

## Privacy, integrity, and validation

- This repository and its GitHub Pages site are **public**. Clear user-specific original values and old generated `docs` files before deploying your copy. Avoid publishing unnecessary personal identifiers. Public recipient email exposure is a deliberate configuration choice.
- Set `base_url` to the *exact* case-sensitive published GitHub Pages path. A wrong URL produces broken hosted verification.
- Do not claim an endorsement or cryptographic signature from the original issuer. The generated issuer is **you**, not Microsoft (or any other awarding body).
- Once a badge is imported elsewhere, changes to hosted metadata may not propagate because the platform caches the data.
- If GitHub Pages fails, check Actions, settings, and whether `docs/index.html` was generated.
- If a platform rejects the issuer, ask its support whether independent Open Badges 2.0 hosted issuers are supported; do not masquerade as the credential issuer.

References: [Open Badges 2.0 specification](https://www.imsglobal.org/spec/ob/v2p0/) · [Baking specification](https://www.imsglobal.org/spec/ob/v2p0/baking/).
