# MyAwards-OpenBadges

A reusable GitHub Pages + Python project that packages **personal/self-issued Open Badges 2.0 references** to externally verifiable certifications and awards. Each credential has its own Assertion, BadgeClass, and baked PNG, sharing one issuer profile.

**Start here: [End-to-end AI workflow](Guide/AI-End-to-End-Workflow.md)** · **[Human setup guide](Guide/README.md)** · **[Copyable AI prompt](Guide/Prompt-to-use-with-AI.md)**

## Use your own copy

Fork or clone the repository. Replace the original owner's `config.json` details and all credential records, and remove inherited generated records in `docs/` before publishing. Upload your original PNGs to `docs/assets/`, update `config.json`, then run `python build.py` or the workflow in **Actions → Build Open Badges 2.0 images**. Configure **Settings → Pages → Deploy from a branch → main → /docs**.

The `Guide/` folder explains the inputs, testing, security/privacy cautions, and troubleshooting. It also contains a copyable AI prompt designed to walk a new owner through configuration.

## Generated content

- `docs/issuer/profile.json`: self-issued issuer profile
- `docs/badges/<slug>.json`: BadgeClass and measured skills
- `docs/assertions/<slug>.json`: hosted Assertion, recipient, issue and expiry dates
- `docs/assets/<slug>-openbadges2.png`: baked PNG with `iTXt:openbadges`
- `docs/index.html`: public badge links

## Important provenance warning

These are **self-issued declarations**, not Open Badges issued or cryptographically signed by Microsoft or any original certification provider. Verify the underlying achievement using its official credential verification URL. Third-party import and issuer support vary; successful imports are not proof of original-issuer OB2 issuance.

The original repository includes an example record for MS-102 owned by ProfKaz. It must be removed or replaced in a fork before another user's publication.

Built around [Open Badges 2.0](https://www.imsglobal.org/spec/ob/v2p0/) and the [baking specification](https://www.imsglobal.org/spec/ob/v2p0/baking/).
