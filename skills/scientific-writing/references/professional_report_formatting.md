# Safe Formatting for Reports and Manuscripts

## Source format and draft status

Reuse the project's TeX, Word, or Markdown source, established template, and evidence
records. The bundled Markdown scaffold is an option for a new workspace, not a
conversion requirement for an existing manuscript.

An internal draft may use the venue's template while keeping its draft status,
placeholders, and unresolved verification states visible in the established locations.
Do not label it submission-ready while any required gate is incomplete. Visual polish
is not evidence.

## Workflow

1. Continue in the existing source, or select a suitable format for a new draft.
2. Draft or revise the requested content, preserving evidence links and review states.
3. Check affected claims, references, numbers, and method-result mappings. Use the
   bundled CLIs only for their supported input formats; prose revision does not require
   reconstructing all records or exporting a full Markdown copy.
4. Inspect the affected rendered output when formatting or layout changes. After a
   conversion, recheck the citations, symbols, tables, or references it could alter.
5. Before final readiness, complete the applicable manifest, claim, reference,
   consistency, authorship, coverage, and lint audits and obtain accountable human
   approval. Formatting and ordinary editing do not waive these requirements.

For a journal or conference, use its current author instructions and official template.
For an institutional report or thesis, use the institution's controlled template.

## Fail-closed placeholder policy

Permitted draft markers are intentionally conspicuous, such as `[[TODO:...]]`. The
language linter treats them as errors. Never replace an unresolved marker with generic
boilerplate, a guessed number, a fabricated statement, or an invented citation.

Keep:

- `submission_ready` false;
- the draft banner visible;
- missing declaration statuses explicit;
- human and confidentiality gates incomplete;

until the underlying records are verified.

## Headings and navigation

- Use a single title and logical heading levels.
- Preserve heading order when converting formats.
- Include lists of tables or figures only when useful or required.
- Use stable internal labels for tables, figures, appendices, and supplements.
- Ensure generated bookmarks and reading order match the visible structure.

## Typography and layout

- Use the venue's prescribed font, spacing, margins, page size, and line numbering.
- Do not use color, weight, or position as the only carrier of meaning.
- Keep equations, symbols, units, subscripts, and superscripts intact through
  conversion.
- Check widows, orphans, clipped content, broken links, and misplaced floats manually.

## Tables, figures, and accessibility

Follow `figures_tables.md`. Verify alt text, captions, provenance, permissions, color
independence, reading order, label legibility, and final-size rendering. Do not create a
decorative visual simply to make a report appear complete.

## References and declarations

Final references must render from verified metadata. Internal drafts may retain located
source IDs and explicit pending human review. After conversion, inspect identifier
links, special characters, author order, and citation order.

Declarations must come from validated records. A style template must never supply a
default ethics approval, consent statement, funding source, conflict statement, author
contribution, data or code promise, or AI disclosure.

## Archival handoff

Retain:

- the manuscript's editable source in its actual format;
- the structured registries;
- the exact venue template version;
- conversion instructions and software versions;
- the final rendered file;
- validator outputs and human approval record.

Do not archive sensitive source documents alongside a public manuscript package unless
authorization, consent, law, contracts, and policy permit it.
