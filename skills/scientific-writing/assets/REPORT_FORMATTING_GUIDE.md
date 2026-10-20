# Fail-Closed Report Formatting Guide

Use the project's existing editable source and evidence records. The bundled Markdown
scaffold is optional for a new workspace; an existing TeX or Word manuscript can remain
in its established format and template.

## Safe default

1. Reuse the current workspace. If a new one needs a scaffold,
   `scripts/scaffold_manuscript.py` is an optional starting point.
2. Keep the `DRAFT — NOT FOR SUBMISSION` banner while any placeholder or verification
   gate remains.
3. Draft and revise in the chosen source format. Publisher formatting may be used for
   an internal draft without clearing pending verification states.
4. Treat the target journal's current author instructions and supplied template as
   controlling.
5. Recheck citations, symbols, tables, and references affected by formatting or
   conversion. Run the applicable full audits before declaring final readiness.

## Hierarchy

- Use one document title and a predictable heading hierarchy.
- Do not encode scientific meaning only with typography or color.
- Keep terminology, abbreviations, units, and statistical notation consistent.
- Preserve machine-readable identifiers and evidence markers until final rendering.
- Never replace a missing value with an aesthetically plausible value.

## Tables

- Every cell must derive from a named evidence record.
- Include units, analysis population, numerator and denominator where relevant.
- Distinguish missing, not measured, not applicable, and zero.
- Keep exact values consistent with prose and the numeric registry.
- Use editable tables unless the venue explicitly requires another format.

## Figures

Figures are optional. This skill does not generate images. A retained figure must have:

- a provenance record linking it to data, code, or a licensed source;
- a caption that identifies the analysis population, units, uncertainty, and panels;
- alt text that communicates the figure's purpose and principal pattern without adding
  unsupported interpretation;
- labels or patterns in addition to color;
- a manual check at the final display size;
- documented permissions and transformations for reused or adapted material.

Never invent a figure, image, diagram, graphical abstract, or missing visual result.

## Submission readiness gate

Before labeling a manuscript submission-ready or submitting it, confirm:

- placeholders are absent;
- factual and numeric claims map to verified evidence IDs;
- citations and reference identifiers pass local checks;
- methods, results, units, denominators, and sample sizes agree;
- authorship, CRediT roles, declarations, and AI use are human-approved;
- confidentiality and target-journal policy reviews are complete;
- reporting-guideline coverage was reviewed without treating it as a quality score.

Formatting quality cannot make incomplete evidence submission-ready.
