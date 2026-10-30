# Human-Directed Manuscript Revision

Use when an author gives suggestions and wants to decide what changes before the
manuscript is edited. Keep the existing VS Code and LaTeX workflow. The author owns
the argument and scientific decisions; AI locates the relevant text, proposes wording,
and implements accepted revisions. A request for prose in chat alone does not require
a file-edit approval round.

## Locate and propose without writing

Start from the author's comment, selected passage, or referenced PDF location. Find
the corresponding source using the file path, section, and a distinctive original-text
anchor; line numbers help navigation but can move. Use a clickable source link when
the client supports it. Read the surrounding context needed
to understand the passage. If several passages fit, show the candidates and let the
author choose. Do not require a selection when the comment is enough to locate it.

Keep the proposal short. For each change show:

- location and exact proposed edit range;
- original text and proposed replacement;
- one sentence explaining the intended improvement.

Use a temporary item number when several changes need separate decisions. Ask about
missing scientific meaning rather than inventing it. Reading adjacent text or finding
related terminology does not authorize editing those passages. Keep the source files
unchanged while presenting the proposal; do not insert red text or create revision
copies, reports, or tracking files as part of this initial discussion.

## Let the author choose

Accept decisions by item or coherent batch: for example, accept 1 and 3, revise 2 with
the author's explanation, and leave 4 pending. Unmentioned items remain pending;
silence is not approval. A rejected item stays rejected unless the author reopens it
or new evidence warrants a brief explanation. Do not ask for approval word by word.

Reuse an explicit approval that already covers the proposed text and range. If the
author supplies an exact replacement and instructs you to apply it at an unambiguous
location, that is approval. A general request to improve a passage starts the proposal
step; it does not approve unseen replacements.

## Apply the accepted scope

Before writing, re-read the original anchor. If only line numbers moved, relocate it;
if the target text or its meaning changed, update the affected proposal for confirmation.
Preserve a recoverable baseline of the author's current source, including uncommitted
work, so the actual changes from this revision can be distinguished from earlier edits.
Do not reset the working tree or treat HEAD as the baseline when it omits that work.

Apply accepted items only. Present a separate proposal before editing another passage,
moving arguments across paragraphs, changing a technical definition, formula meaning,
citation relationship, or shared macro, or adding a factual claim outside the approval.
An explicitly accepted batch may cover several listed locations; do not request the
same approval again during implementation.

Preserve LaTeX structure, numbers, equations, and label/reference/citation identifiers
unless the approved change includes them. Text within captions or emphasis commands
may be revised within the accepted scope. Check the mathematical meaning of text
inside formulas. Keep effective accepted prose; subsequent rounds address the author's
remaining comments rather than silently rewriting accepted passages.

## Show what actually changed

Show the actual source diff against the baseline, not just the proposed replacement.
Check it for edits outside the approved ranges. Briefly explain the effect on reasoning,
readability, terminology, or claim strength; keep scientific conclusions within evidence.

Use the project's existing build command on the machine that edits the manuscript.
With LaTeX Workshop, use source/PDF navigation and compare the previous and rebuilt
PDF where rendering matters. Keep the previous PDF when a before/after comparison
is needed. A separate latexdiff redline is optional for larger revisions, not a mandatory
dependency or a reason to insert markup into the working manuscript. A build failure
or unavailable compiler must be reported; do not claim the PDF was checked. Compilation
success does not establish scientific fidelity.

Keep interaction concise and reuse existing project records when continuation needs
them. Routine passage edits need no extra ledger, reply letter, or full submission audit.
This workflow adds no permission to send manuscript material to external services,
install tools, publish, or change editor settings. It supplies behavioral guidance;
editor buttons and enforced write isolation require client capabilities.
