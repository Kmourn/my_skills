# Provenance and adaptation

Adapted from Max Simchowitz's `msimchowitz/writing-skills`,
`for-agents/literature-review`, at fixed commit
`214981fe02326f27b0fc8790d00eb4b731607073`:

- Source: https://github.com/msimchowitz/writing-skills/tree/214981fe02326f27b0fc8790d00eb4b731607073/for-agents/literature-review
- Root license: https://github.com/msimchowitz/writing-skills/blob/214981fe02326f27b0fc8790d00eb4b731607073/LICENSE
- Retrieved: 2026-10-01 using the deployed Codex skill-installer's fixed-ref download into a validation cache.
- License: MIT, copyright (c) 2026 Max Simchowitz. The complete upstream license is preserved in `LICENSE`.

Retained and adapted the scope plan, source ledger, claim-evidence matrix,
evidence-workflow reference, skill entrypoint, and UI metadata. Templates are
optional when existing project records suffice. Evidence support labels and
human verification are separate. Added bounded narrative/systematic routing and
handoffs to available `paper-lookup` and `scientific-writing` workflows; authorized
internal drafts remain unverified and not submission-ready pending human review.

Removed mandatory sibling `paper-writing`, `general-writing`, sentence-style,
LaTeX-convention, and embedded Humanizer dependencies because they are not
required or deployed in the target workflow. Removed fixed LaTeX filename,
compilation, and PDF-copy rules to honor the requested output and project
conventions. The upstream `scripts/audit_review.py` was inspected and omitted:
it requires TeX and BibTeX, mandates a separate ledger schema, and does not audit
a Markdown review or validate claim support. This adaptation has no bundled
helper scripts; use actual format-specific tools and evidence checks as needed.

This source is the lightweight writing-skills review workflow, not the K-Dense
systematic literature-review skill. No external paid-provider integration,
Parallel/OpenRouter dependency, credential scan, or automatic memory/configuration
change is added by this adaptation. Upstream instructions were reviewed as source
material rather than executed as task authorization.
