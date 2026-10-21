# End-to-end walkthrough: publish a credential with an AI assistant

> **Audience:** Someone who has never used this project before, or an AI assistant being asked to run it for the first time. This document is written for a GitHub fork **or** a new repository created from the ZIP. Read the companion [AI prompt](Prompt-to-use-with-AI.md).

## The essential difference

This project turns a PNG into a **self-issued, hosted Open Badges 2.0 record** referencing an existing credential. Your badge's **original issuer remains the organization that awarded the credential**, verified at its original URL. Your own GitHub Pages issuer profile is the issuer of the **self-issued Open Badges record**, not a representation that Microsoft or another provider issued an OB2 badge. Successful import into Credly is not original-issuer signature verification.

## What the human supplies

**Per credential (minimum):**

1. The **original badge PNG** as a file attachment or a file available in the repository.
2. The **official public verification URL** for that exact credential, not merely the certification landing page.
3. Permission to update **their** repository. If there is no access, the AI must produce exact files and instructions rather than claim to have uploaded anything.

**One-time configuration (AI should read existing configuration first and only ask if missing):**

- GitHub repository URL and owner; whether GitHub Pages is enabled at `main /docs`.
- Public display name, website/profile and **public email** of the self-issued issuer.
- Recipient identity, usually an email verified in Credly; confirm the user agrees that `hashed:false` publishes this address.
- Exact credential title and dates **only if confirmed**. `self_attestation_date` is the date the personal declaration is issued, not when Microsoft awarded a certification. `expires` must come from the official credential.
- Desired destination: Credly or another Open Badges 2.0 importer.

**Optional:** public source of skills measured, custom description, criteria, and evidence label. AI may research public exam skills, but must distinguish the examination scope from individual verified proficiencies.

### Minimum prompt for a credential already configured

```text
Use my GitHub repository https://github.com/OWNER/REPOSITORY and follow
Guide/AI-End-to-End-Workflow.md.
Add the attached ORIGINAL badge PNG as a new Open Badges 2.0 record.
Official verification URL: https://ORIGINAL-ISSUER/credential/UNIQUE-ID
Update config.json, generate the BadgeClass/Assertion/issuer references and
both PNGs, publish what you can to GitHub, validate GitHub Pages, and give
me the final baked PNG URL for Credly. Ask me only for missing facts.
Do not invent dates or claim the original issuer generated the Open Badge.
```

**Do not omit the PNG and the official credential-specific verification URL.** Without both, the AI must ask for the missing item rather than use a random image or substitute an issuer's home page.

## Phase 0 — First-time setup (once per fork / fresh repository)

**Human:** Fork the repository, or download the ZIP from [Downloads](../Downloads/README.md) and extract its contents into the **root** of a new repository. Preserve `.github/workflows/`; GitHub Pages will not unpack a ZIP uploaded as a single file. In **Settings → Pages**, publish branch `main`, folder `/docs`.

**AI:**
1. Read `README.md`, `Guide/README.md`, this file, `Guide/Prompt-to-use-with-AI.md`, `config.example.json`, `config.json`, `build.py`, `validate_config.py`, and `.github/workflows/build-badges.yml`.
2. Read the actual repository tree and Pages workflow status; identify owner-specific values and existing records. Never reissue the original owner's badges as the new user's own.
3. For a fresh repository, start from `config.example.json`; for an existing repository, **preserve all legitimate records** and add another. Set exact case-sensitive `base_url` to `https://OWNER.github.io/REPOSITORY` (or the actual Pages custom domain/path).
4. Set `issuer` (the person publishing the personal record) and `recipient`; confirm the implications of publicly exposing a plain email.
5. Remove inherited source owner's `docs/assertions`, `docs/badges`, and baked PNGs if forking. Rebuild only the new owner's records. **Avoid deleting valid records belonging to the current owner.**

## Phase 1 — Research and prepare one badge

**AI must:**

1. Identify a unique, lowercase `slug` such as `sc401`. Check it does not collide with an existing entry.
2. Confirm the exact public verification URL resolves to the actual credential and extract only information it truly supports. The original PNG does not itself prove title, skills or expiration.
3. Confirm expiry on Microsoft Learn or ask the user. **If unknown, do not fabricate a date.** Leaving `expires` out can cause Credly to display `does not expire`; tell the user about this limitation and encourage an official check.
4. If skills are requested, use an authoritative source such as the official Microsoft Learn exam study guide and preserve the actual skill category names in `skills`; supply its link as `skills_source`.
5. Decide `self_attestation_date` as the actual date of the new self-issued record (not certification award date), with the user's approval if the date is not determined.
6. Create/modify exactly one entry inside `config.json.records`, keeping all other records intact.

### Fields in `config.json`

| Field | Where it comes from | Used for |
| --- | --- | --- |
| `base_url` | GitHub Pages configuration | Hostname and paths for all JSON-LD IDs |
| `issuer.name/url/email` | Public self-issued record publisher | `docs/issuer/profile.json` |
| `recipient.type/identity/hashed` | Badge owner, agreed with user | `Assertion.recipient`, Credly account match |
| `slug` | Unique short ID | All per-badge filenames |
| `title` | Official badge title | `BadgeClass.name` (no `Personal record:` prefix) |
| `original_image` | Source image path | Source PNG used for baking |
| `verification_url` | Original provider's credential-specific link | Evidence and original verification |
| `self_attestation_date` | Actual self-issuance date | `Assertion.issuedOn` |
| `expires` (optional) | Official individual expiry | `Assertion.expires` |
| `skills`, `skills_source` (optional) | Official skills/objectives | `BadgeClass.tags` and `alignment` |
| `description`, `criteria_narrative`, `evidence_name` | Truthful description and provenance | BadgeClass and Assertion evidence |

Example per-badge entry (**illustrative only; do not copy dates**):

```json
{
  "slug": "example-cert",
  "title": "Verified certification name",
  "original_image": "docs/assets/example-cert.png",
  "verification_url": "https://issuer.example/verify/real-id",
  "self_attestation_date": "2026-10-21T00:00:00Z",
  "expires": "2027-10-21T00:00:00Z",
  "description": "Self-issued reference to a credential verifiable at its original issuer; not an issuer-created Open Badge.",
  "criteria_narrative": "Verify the original credential using the credential-specific URL.",
  "evidence_name": "Original issuer verification",
  "skills": ["Example documented examination area"],
  "skills_source": "https://issuer.example/official-skill-guide"
}
```

## Phase 2 — Image delivery and repository publishing

There are **two distinct PNGs**:

- `docs/assets/<slug>.png` — original image, with unchanged artwork; `BadgeClass.image` links here.
- `docs/assets/<slug>-openbadges2.png` — the original PNG with a correctly encoded **uncompressed `iTXt` chunk named `openbadges`** containing the Assertion JSON-LD; this is what the user downloads for Credly.

**Preferred workflow:** AI writes the original image to `docs/assets/<slug>.png` using an authorized binary-capable GitHub tool, adds the entry to `config.json`, and lets the repository workflow generate the baked PNG and JSONs. If the AI can run Python locally, `python build.py` can generate both PNG and JSON outputs for inspection first.

**When AI cannot upload binary PNGs:** AI must create a downloadable ZIP with **exactly named** `<slug>.png` and `<slug>-openbadges2.png` (if it can bake locally), tell the user to upload both into `docs/assets/`, and **wait for confirmation**. Do not claim the badge is published merely because the JSON files exist. After the human uploads the source PNG, the AI must continue with the next phase.

**Important:** committing `config.json` before the source PNG exists may start a failing build. This is expected; once the PNG exists the next successful run should regenerate metadata.

## Phase 3 — Generate and publish (AI resumes after upload)

**AI must:**

1. Inspect actual GitHub tree for `docs/assets/<slug>.png` and ensure `config.json.records` contains the badge (the image alone does NOT create the record).
2. If missing, update `config.json` now. Do not rely on manually written JSON that will be overwritten on the next build.
3. Run `python validate_config.py` and `python build.py` locally, or wait for / manually dispatch **Actions → Build Open Badges 2.0 images**.
4. Check the **latest relevant workflow execution** and its logs, not an unrelated prior successful run. Then verify the **Pages deployment** succeeded.
5. Confirm all artifacts exist:
   - `docs/issuer/profile.json` — public issuer of the self-issued declaration.
   - `docs/badges/<slug>.json` — BadgeClass: title, description, criteria, original image, skills, issuer pointer.
   - `docs/assertions/<slug>.json` — Assertion: credential recipient, issuedOn, optional expires, original verification evidence, BadgeClass pointer.
   - `docs/assets/<slug>.png` — original artwork.
   - `docs/assets/<slug>-openbadges2.png` — baked image for Credly.
   - `docs/index.html` — generated website listing.
6. Check JSON syntax and exact URI relationships. Inspect the **actual uploaded baked PNG** for its `iTXt:openbadges` block; parse that Assertion and compare its ID, `recipient`, `badge`, date and evidence with the hosted `docs/assertions/<slug>.json`. Do not just trust the filename.
7. Check the **public** Pages endpoints return useful JSON and PNG bytes, not a GitHub repository `blob` page or HTTP 404. If browsing is unavailable, say the check could not be performed and ask the user to test the URLs. Only mark the result fully verified when all checks are complete.

## Phase 4 — Import into Credly

**Human:**

1. Open `https://OWNER.github.io/REPOSITORY/assets/<slug>-openbadges2.png` in a browser and **download a fresh PNG**; never upload the visual-only original `<slug>.png`.
2. Sign in to Credly using the account whose verified email matches `recipient.identity`.
3. Use Credly's option to **add an external/other badge**, and select the baked PNG.
4. Confirm the displayed title, **self-issued issuer identity**, original verification evidence, date and any skills. The displayed date `issuedOn` is the personal record's issue date.
5. Report exact errors/screenshots to the AI. Existing imported badges may be cached.

**AI:** Provide exactly these links:
- `<base_url>/assets/<slug>-openbadges2.png`
- `<base_url>/assertions/<slug>.json`
- `<base_url>/badges/<slug>.json`
- `<base_url>/issuer/profile.json`
- Official `verification_url`

### Error map

| Credly / workflow symptom | First check |
| --- | --- |
| No Open Badges metadata | Original PNG uploaded by mistake; inspect baked `iTXt:openbadges` |
| Unable to retrieve badge data | Missing `config.json` record, missing published JSON, wrong base URL, Pages deployment or cache |
| Badge associated with another email | `recipient.identity` vs email verified with Credly (not `issuer.email`) |
| Issuer unsupported | Platform's issuer policy or Profile compliance; do **not** pretend to be Microsoft |
| No expiration shown | `expires` absent; confirm genuine expiry first |
| Old title/skills | Credly cache or generator stale; inspect BadgeClass and fresh import |
| Workflow fails | Missing original PNG, invalid config, branch write permissions, job logs |
| Generic processing error | Record failure details; retry prudently and contact platform support |

## Phase 5 — Multiple credentials and maintenance

Add another `records[]` entry with a **new slug** and repeat phases 1–4. Reuse the same issuer/recipient if appropriate. Keep `config.example.json` free of the source owner's identity; never copy personal credentials into a public starter ZIP. Avoid stale `docs` generated files when switching accounts.

### Final AI acceptance checklist

- [ ] User gave original PNG and official credential-specific verification URL
- [ ] Confirmed badge title, correct recipient, no invented expiry or skills
- [ ] `config.json` updated; previous records preserved
- [ ] Original PNG and baked PNG exist in correct paths
- [ ] Issuer, BadgeClass, Assertion JSON-LD agree with PNG metadata
- [ ] Successful relevant GitHub workflow and Pages deployment verified
- [ ] Public endpoints checked or clearly marked unverified
- [ ] User given fresh baked PNG link and exact Credly steps
- [ ] Issuer/provenance limitations accurately disclosed

References: [Open Badges 2.0](https://www.imsglobal.org/spec/ob/v2p0/) · [Baking](https://www.imsglobal.org/spec/ob/v2p0/baking/).
