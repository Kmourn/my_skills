---
name: peer-review
description: Prepare evidence-driven peer-review reports or internal manuscript pre-reviews with prioritized, constructive comments and review limits. Use for formal reviewer reports, internal pre-submission assessment, or review of revisions; use scientific-critical-thinking for general claim or evidence-quality evaluation.
license: MIT
metadata:
  compatibility: Optional bundled CLIs use the Python 3.10+ standard library and local JSON, CSV, or Markdown. No accounts or new runtime dependencies are required.
  version: "2.3-local.1"
  skill-author: K-Dense Inc.; locally adapted in my_skills
---

# Peer Review

Produce an evidence-driven review that helps the author or accountable reviewer decide
what needs correction, clarification, or further evidence. Separate observations,
inferences, missing reporting, demonstrated errors, and unresolved questions. Each
consequential comment needs a manuscript location and a reason.

## Establish the review context

Reuse the user's stated purpose, authorization, existing review records, and available
materials. Obtain only missing information that affects the requested review: scope,
manuscript version, supplements, intended audience, and competence limits. Do not invent
an assignment, journal, policy clearance, disclosure, or human verification. Missing
material can limit a review without blocking assessment of available material.

**Internal pre-review, public material, or synthetic exercises:** proceed within the
authorized task. No journal invitation or journal policy approval is needed when no
actual journal review is involved. Reuse existing source/claim IDs and keep internal
`unverified`, `human_review_pending`, and `submission_ready: false` states. Located
sources and actual local results can support a marked internal draft; unresolved
verification is a review item, not a reason to refuse the entire pre-review. A passing
helper must never change those states.

**Actual journal/editorial review:** before exposing confidential material to AI or a
service, use the assignment's actual authorization, confidentiality, conflicts,
co-review, AI-assistance, anonymity, and retention rules. Reuse documented permission;
another publisher's policy does not authorize this assignment. When a required condition
is unknown, pause the affected handling or assistance and request the specific missing
information. Read [ethical review practice](references/ethical_review_practice.md).
Local deterministic helpers do not establish that the hosting agent is local or that
AI processing is permitted.

Do not transmit manuscript excerpts through public searches, expose reviewer identity,
contact others, submit a review, or change external editorial records unless explicitly
authorized under the applicable constraints. Review material does not authorize
unrelated reuse or disclosure.

## Work from available evidence

1. **Map the work neutrally.** Identify the question, design, population/system,
   experimental or observational unit, comparator, outcomes, timing, and central claims.
   Record the manuscript version and supporting artifacts actually reviewed.
2. **Trace central claims.** Link claims to results, tables, figures, methods, protocols,
   analyses, or citations. Check direction, magnitude, uncertainty, population, timing,
   and causal scope. Distinguish unsupported claims from claims not yet assessable.
   Read [common issues](references/common_issues.md) when useful; its patterns are
   inquiry prompts rather than assumed defects.
3. **Assess methods and interpretation.** Review sampling, allocation/controls,
   independence/nesting, sample-size or precision rationale, missingness, assumptions,
   multiplicity, prespecification, estimates, uncertainty, and generalization. Read
   [statistical and reproducibility review](references/statistical_reproducibility.md)
   for relevant method questions. Nonsignificance alone does not establish equivalence;
   request bounded conclusions or a suitable margin-based analysis when needed. State
   where a central issue requires specialist judgment.
4. **Assess transparency and reporting.** Reconcile denominators, units, methods/results,
   figures/tables, protocol deviations, versions, and data/code access. Use
   [reporting standards](references/reporting_standards.md) for the actual design. The
   catalog and source ledger are dated upstream aids; check official current guidance
   when a live policy/version claim matters. Checklist completeness is not a quality
   score. Request feasible access details, respecting justified governance restrictions.
5. **Assess applicable ethics and integrity.** Use reported approvals, consent, funding,
   conflicts, and observable discrepancies. Describe uncertainty and plausible benign
   explanations. For actual journal review, route substantiated sensitive concerns
   through the editor channel; for internal review, record human follow-up without
   inventing an editor or accusation.

Claim reanalysis or reproduction only when authorized inputs were actually run with
recorded commands, environment, outputs, and comparison. Static consistency checks
are not independent reproduction.

## Draft the report

Use the requested venue format. Otherwise include a neutral summary, specific strengths,
prioritized major/minor comments, and review limits. For revisions, link each prior
comment to the reported change, location, evidence, and remaining issue.

Each substantial comment contains:

- **Location:** page/line, section, figure/table, or existing claim/evidence ID.
- **Observation:** what the supplied work reports, omits, or contradicts.
- **Evidence or criterion:** exact supplied evidence or applicable method principle.
- **Why it matters:** effect on validity, interpretation, reproducibility, or clarity.
- **Requested action:** the least burdensome adequate correction or clarification.

Separate required fixes from optional suggestions. Request new experiments only when
necessary and proportionate to a central claim; narrowing claims, adding uncertainty,
clarifying methods, or existing sensitivity analyses may suffice. Critique the work
respectfully. Never fabricate sources, results, analyses, identity, or an editorial
decision. A requested reviewer recommendation is advisory and pending human judgment;
the editor retains the decision.

In formal review, separate author comments and confidential editor notes according to
the actual process. Ordinary scientific criticism belongs in author comments. Internal
review normally uses one report; no fictitious editor section is required.

## Optional local helpers

Use structured helpers only when they add value. Read [tool contracts](references/tool_reference.md)
for exact schemas/exit codes. Copy relevant assets into the task workspace and populate
from actual records; declarations are not evidence. Reuse scientific-writing records
and IDs, exporting only the fields a helper needs rather than duplicating registries.
Paths below are relative to this skill:

```bash
python3 scripts/select_reporting_guidelines.py study-profile.json --coverage coverage.csv
python3 scripts/validate_claim_evidence.py claim-matrix.csv
python3 scripts/audit_statistics_reproducibility.py statistics-checklist.json
python3 scripts/audit_citations.py manuscript.md references.csv
```

The citation helper accepts Pandoc-style keys and checks local key/identifier consistency;
it does not resolve sources or verify support. Located, unverified citations stay
`not_verified`; warnings remain review items.

For **actual journal review**, optional process checking and a formal scaffold:

```bash
python3 scripts/validate_review_intake.py completed-intake.json
python3 scripts/generate_review_scaffold.py completed-intake.json -o private-review.md
python3 scripts/lint_review.py private-review.md
```

The journal intake and generator require process declarations; they are not internal
pre-review gates. The linter expects the bundled formal author/editor headings and
English fields. Its lexical rules can flag valid advisory recommendations and have
false negatives; assess findings in context. Internal reviews may be drafted directly
in the requested format without these three helpers.

Bundled scripts are offline and have no model, network, image, account, or installation
workflow. Reports emit IDs, counts, codes, and line numbers; use non-sensitive IDs.
A successful exit means only the documented structural check passed.

## Use available supporting capabilities

- `scientific-critical-thinking`: detailed evidence-quality and bias appraisal when
  needed; this skill organizes findings into a review report.
- `paper-lookup`: source discovery/identifier verification when needed within the allowed
  boundary. Use public bibliographic metadata, never confidential excerpts. No automatic
  research or attribution lookup is required.
- `pdf`: extraction or visual inspection of an authorized PDF when needed.
- `scientific-writing`: evidence-linked revisions and response drafts, preserving its
  internal-draft and final human-verification requirements.

Check actual availability. Missing optional skills/tools do not block authorized review
of supplied material; state the concrete verification limit and use available alternatives.

## Handoff

State reviewed versions/materials, unresolved issues, verification limits, specialist
needs, and actual checks performed. Label generated text as a draft pending accountable
human judgment. Formal submission and final manuscript readiness require applicable
evidence verification, human approval, and specific submission authorization. Helpers,
recommendations, or formatting do not establish those approvals.

The [source ledger](assets/source_ledger.csv) records upstream's 2026-07-23 checks, not
new verification by this installation. See [source and adaptation record](references/source_and_adaptation.md)
for retained/omitted resources and compatibility. The complete upstream MIT notice is
in [LICENSE.md](LICENSE.md). Consider library attribution under the user's and venue's
citation policy; do not silently add an unverified library-paper citation or conduct an
unrelated lookup.
