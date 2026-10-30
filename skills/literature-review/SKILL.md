---
name: literature-review
description: Build lightweight, source-grounded technical or narrative literature reviews, surveys, and related-work syntheses. Use to compare method families, reconcile disagreements, identify evidence gaps, or draft a cited review from existing papers. Systematic reviews require an additional agreed design and search/screening record.
license: MIT
---

# Literature Review

Answer a bounded review question through sources and a claim-evidence matrix,
then synthesize method families, disagreements, and gaps. This is a lightweight
technical or narrative review workflow, not a claim of exhaustive retrieval or
PRISMA compliance. Never invent papers, metadata, quotations, results, or details
that the reviewed sources do not disclose.

## Scope and existing work

Read the project's existing review, research record, source IDs, and claim IDs
before adding records. Reuse their formats and links. Only if useful records are
missing, adapt [review-plan.md](assets/review-plan.md),
[source-ledger.csv](assets/source-ledger.csv), and
[claim-evidence-matrix.csv](assets/claim-evidence-matrix.csv). These are optional
starting formats, not a requirement to create duplicate ledgers.

Establish the question, audience, retrieval cutoff, unit of comparison, source
and date boundaries, comparison axes, available material, and requested product.
Use existing choices; ask only about a missing decision that affects the next
step. Clarify what a request for “all” covers. Record material scope changes in
the existing project record.

If the user requests a systematic review, first establish the additional design
and record scope: protocol, databases and queries, screening and exclusions,
deduplication, extraction, appraisal, synthesis, and applicable reporting
requirements. The templates here do not establish those procedures or authorize
an exhaustive search. Do not describe a narrative review as systematic.

## Sources and evidence

Read [evidence-workflow.md](references/evidence-workflow.md) when building or
checking the evidence matrix. Use available `paper-lookup` for scholarly
retrieval, metadata, full text, and reproducible provenance; read its relevant
API reference before using that API. If it or another optional tool is absent,
use actually available, authorized tools or supplied material and report the
coverage limit. Do not invent a tool result or add a paid provider dependency.

Record the search source, query or endpoint and parameters, access date, bounds,
and meaningful failures in the existing record. A supplied-paper review should
say it covers that corpus rather than imply a new field-wide search. Distinguish
metadata, abstract-only access, and full text. Discovery snippets and secondary
summaries are leads, not full-text evidence.

For each important source and claim, retain:

- stable source ID, title, authors, year, identifier/URL, and version when available;
- method family or topic, source type, and access level;
- exact supporting page, section, table, or artifact heading;
- a claim-to-source mapping, competing evidence, and missing details;
- evidence state and verification state, kept distinct.

Label evidence `reported`, `derived`, `inferred`, `conflicting`, or
`not-disclosed`. Record derivations and qualify interpretations. “Not disclosed”
means absent from the sources actually reviewed, not absent from all literature.
An AI source check does not confer human verification.

## Compare and synthesize

Build the matrix before drafting substantive claims. Choose comparison axes
that answer the question: assumptions, architecture, objectives, data, training,
evaluation, practical constraints, or chronology where inheritance matters.
Use the optional technical extraction axes in the evidence reference for model
or training-recipe comparisons; do not impose them on other fields.

Group papers into meaningful method families rather than a list of isolated
summaries. Explain agreements and disagreements, including differences in
versions, tasks, datasets, metrics, evaluation settings, or evidence quality.
Keep family claims separate from release, checkpoint, or experiment claims.
Do not infer a mechanism from a leaderboard score without supporting controls
or ablations, and do not transfer an undisclosed recipe from a related model.

State gaps as bounded findings: an inaccessible source, missing comparison,
conflicting report, limited evaluation, or question unsupported in the reviewed
corpus. A failed search does not prove novelty. Separate proposed next steps
from conclusions supported by existing evidence.

When the user asks to evaluate a specific idea or contribution, read
[research value and differentiation](../_shared/references/research-value-and-differentiation.md)
and apply it to the closest reviewed work. Ordinary reviews do not require this
reference or a contribution statement.

## Draft and check the requested product

Honor the user's Markdown, document, LaTeX, or other chosen format and project
conventions. Use available `scientific-writing` for a scientific manuscript or
report where its evidence and consistency workflow is useful; do not require
undeployed sibling writing skills or automatic style-service calls.

An authorized internal draft may use located source material and actual local
results, with missing facts left missing and human review explicitly pending.
Retain existing evidence/claim IDs, mark affected links `unverified`, and keep
`submission_ready: false` until the applicable verification and final review
are complete. Do not invent verifier identities or dates. Reuse prior human
verification only when the source version, proposition, and locator still match.

Cite near each supported proposition or table cell. Distinguish source reports
from cross-source interpretations, and keep conclusions within the available
evidence. Check citation targets, bibliographic metadata, support locations,
versions, names, numbers, qualifiers, conflicting evidence, and unresolved
facts after revisions. Use available format-specific build and rendering tools
when the requested output requires them; a successful build does not verify
scientific claims.

Deliver the review and requested comparison tables with the retrieval cutoff,
actual corpus/coverage, material gaps, verification status, and artifact links.
State any checks that could not be performed. Do not call the draft final or
submission-ready while evidence or required human approval remains unresolved.
