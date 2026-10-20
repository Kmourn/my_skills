# Evidence and Provenance Workflow

## Core separation

Drafting and evidence verification are different activities.

- **Drafting** organizes language from already recorded evidence IDs. A draft may remain
  incomplete and uncertain. Authorized internal drafts may use located source material
  and actual local results, with claim-linked pending-human-review marks and a draft banner.
- **Verification** requires an accountable human to open the source, confirm the exact
  support and locator, check bibliographic metadata, and record who verified it and
  when.
- A fluent sentence is not evidence. Search snippets, generated summaries, memory, and
  another paper's reference list are discovery aids, not verified support.

## Registries

Reuse current research records, IDs, and artifact links. The optional scaffold creates
five linked records for the bundled CLIs; do not regenerate suitable existing records.
If their required C/E formats differ from existing IDs, retain one mapping and link the
original records, preserving source and result versions instead of copying evidence.

1. `source_manifest.json` assigns each source an `E` ID and records identifiers,
   location, confidentiality class, and verification state.
2. `claims.csv` assigns each claim a `C` ID, stores a hash rather than raw claim text,
   and maps the claim to one or more `E` IDs, with verification pending during an internal
   draft and completed for submission-ready claims.
3. `consistency_manifest.json` binds numeric facts, methods, outcomes, analysis intent,
   units, denominators, sample sizes, and result locations.
4. `authorship.json` records human authorship criteria, CRediT roles, accountability,
   declarations, and AI use.
5. `reporting_coverage.json` records high-level coverage without scoring or certifying
   the manuscript.

These registries contain metadata, not full source documents. Do not paste unpublished
manuscripts, peer-review files, PHI, sensitive datasets, proprietary content, or source
documents into them.

Local results should link back through analysis to the actual run, raw output or failure,
the plan tested, and the code/data versions. Add figure and manuscript links as they are
created; distinguish planned settings from actual execution and preserve deviations.

## Claim and evidence links

Every factual or numeric assertion needs an auditable link to evidence and a review
state. Preserve existing source annotations or linked review records for TeX, Word,
or other manuscript formats; do not require conversion or a duplicate ledger.

For the bundled Markdown/CSV auditor, append machine-readable markers:

```text
[claim:C001] [evidence:E001,E002]
```

An alternative citation marker is `[@E001]`. In that Markdown input, keep the claim and
evidence markers on the same line until the audit passes. This syntax is a CLI input
requirement, not a universal manuscript format. Final rendered citations may replace
internal evidence IDs only while preserving their auditable mapping and review states.

## Verification procedure

For each new or changed source-to-claim link requiring human verification:

1. Open the authoritative source or record.
2. Confirm title, author or organization, publication state, year, and identifiers.
3. Record the exact supporting location, such as section, page, table, figure, or
   registry field.
4. Confirm that the source supports the claim's direction, population, intervention or
   exposure, outcome, time point, and uncertainty.
5. Record caveats, retractions, corrections, expressions of concern, or version status.
6. Mark the source verified only after a named human completes the check.

Reuse an existing human verification when the source version, claim, and supporting
locator are unchanged. Otherwise preserve its history in the existing record, mark the
affected current link unverified, and recheck it. Until human review, retain
`verification.status: unverified`; do not fabricate verifier identity or date. Keep AI
source-check notes and pending reviews in the existing research record, without adding
fields to the verification object or creating a second ledger.

For each claim:

1. Classify it as factual, numeric, method, result, interpretive, or declaration.
2. When using the bundled CSV format, hash the normalized claim text and store the hash
   in `claims.csv`; otherwise retain the project's existing versioned claim mapping.
3. Map it to evidence IDs; retain pending review in an internal draft and require verified
   support for submission-ready prose.
4. Record uncertainty and whether the analysis was confirmatory, exploratory,
   descriptive, or not applicable.
5. Keep unsupported or conflicting claims out of submission-ready prose. If useful,
   retain them in a clearly marked unresolved-issues log.

## Drafting gates

Do not infer or complete missing:

- citations, identifiers, quotations, or source locators;
- data values, denominators, units, sample sizes, or statistical results;
- methods, protocol details, analysis decisions, or deviations;
- approvals, consent, registrations, author contributions, conflicts, funding, or
  availability statements.

Use explicit missing states. Preserve negative, null, adverse, unexpected, and
inconclusive findings. Never convert absence of evidence into evidence of no effect.

## Final audit

Run these strict checks before claiming final readiness:

```bash
python3 scripts/validate_manifest.py source_manifest.json --kind source --require-verified
python3 scripts/audit_claims.py manuscript.md claims.csv source_manifest.json
python3 scripts/check_consistency.py consistency_manifest.json
python3 scripts/check_references.py source_manifest.json
```

These commands require their documented Markdown/JSON/CSV inputs. For another source
format, use the established records and compatible checks to cover the same evidence,
verification, citation, and consistency requirements. Do not claim that the Markdown
auditor checked TeX or Word directly.

Tool output contains IDs and line numbers, not manuscript or source text. A passing
machine audit supports review; it does not replace human scientific judgment. During
authorized internal drafting, findings about unverified claims or sources are pending
review items, not permission to mark them verified and not a requirement to stop drafting.
Keep the draft banner and `submission_ready: false`; final audits and human approval
remain required for submission-ready status.
