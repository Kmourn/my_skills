# Source and local adaptation

Upstream: K-Dense-AI/scientific-agent-skills, `skills/peer-review`, version 2.3.
Fixed commit: `91497e335489dcb544ec8ddc8f6b7ce5fd6d1121`.
Source: https://github.com/K-Dense-AI/scientific-agent-skills/tree/91497e335489dcb544ec8ddc8f6b7ce5fd6d1121/skills/peer-review
License: MIT. The full root `LICENSE.md` from this commit, including the K-Dense Inc.
2025 copyright and complete permission/warranty notice, is retained as `LICENSE.md`.
Local adaptation date: 2026-10-01; version 2.3-local.1.

## Decisions and resources

- Rewrote SKILL.md around formal review and authorized internal pre-review. Journal
  policy/intake gates are scoped to actual assignments; internal review keeps existing
  evidence IDs and pending-human-review states, following scientific-writing's internal
  draft versus final readiness distinction. No helper confers publication readiness.
- Routed general scientific evidence appraisal to scientific-critical-thinking and used
  paper-lookup, pdf, and scientific-writing only as available optional capabilities.
  Removed automatic library-paper citation and unrelated network lookup requirements.
- Retained all eight Python files unchanged: seven local CLIs plus `_common.py`. They
  are dependency-free; each CLI imports common helpers. The scaffold additionally
  calls `validate_review_intake` and reads `assets/review_scaffold_template.md`; the
  reporting selector reads `assets/reporting_guidelines.json`. No installed account,
  image-generation, plotting, network, or model library is needed.
- Retained all nine assets. Intake/scaffold assets serve formal review; study profile,
  reporting checklist/catalog, claim matrix, statistics checklist, and citation CSV
  support the optional audits. `assets/source_ledger.csv` is retained as dated upstream
  provenance, not claimed as fresh local verification. Template values are synthetic
  or incomplete and must not be substituted for manuscript evidence.
- Retained common_issues, statistical_reproducibility, reporting_standards,
  ethical_review_practice, and tool_reference. They provide contextual review criteria,
  schema contracts, and formal-review handling. Corrected the historical COPE statement,
  made upstream verification dates explicit, scoped ethics/intake advice to real review,
  and corrected the documented claim-matrix requested-action warning behavior.
- Omitted `references/security_validation.md`: it described upstream historical scanner
  results and removed schematic files, and pointed to unavailable repository-level tests,
  uv/scanner commands, and an outside-home `/tmp` output. No retained script or asset
  calls it; only the original SKILL.md index did. Its scan results are not local evidence.
- Moved upstream top-level `compatibility` into `metadata.compatibility` to satisfy the
  trusted local frontmatter validator.
- Added `agents/openai.yaml` using the trusted skill-creator generator. Automatic skill
  discovery remains enabled by default. No tool/account dependency is declared.

## Compatibility and limits

Upstream metadata claimed Python >=3.11. All files parse under the actual Python 3.10.12
runtime and retained CLIs execute with the standard library. Local compatibility is
therefore stated as 3.10+, with no new Python installation or runtime dependencies.
Static parsing and synthetic helper exercises establish those bounded checks only;
they do not prove full-version/platform coverage, scientific correctness, peer-review
completion, human verification, or submission readiness. Later-version support follows
the source syntax/API use rather than exhaustive testing.

The journal intake validator intentionally remains strict and may reject declarations
that are incomplete. That does not revoke an authorized internal review; internal review
does not use this journal-specific gate. Lint is English/format-specific and may flag
legitimate advisory language. Checklist audits check declarations, not their truth.

Implementation self-checks, source/adapted SHA256 manifests, and synthetic inputs/outputs
are retained in the task's local validation cache. An independent forward test is a
separate integration step; no upstream scanner or live policy/source verification is
claimed by these self-checks.
