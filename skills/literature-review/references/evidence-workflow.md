# Evidence Workflow

## Source choice

Use the artifact that supports the particular proposition:

- A versioned paper or appendix for its method and experiments.
- An official model or data card for the exact release, intended use, license,
  or configuration it names.
- A tagged repository or release note for version-specific implementation.
- An official technical blog for release chronology or attributed statements;
  treat promotional comparisons cautiously.
- Independent studies for reproduction, criticism, and external comparisons.

Primary status does not establish quality or independently confirm the
originator's claim. Secondary sources can supply attributed context and leads;
open the primary artifact where possible for a specific technical claim.

## Retrieval and claim records

Reuse project records and IDs. Retain the search date/cutoff, database or site,
query and bounds, and source access level. Preserve bibliographic metadata and
version discrepancies rather than choosing a plausible value. An identifier
must come from a located record, not an invented completion.

Map each major synthesis claim to source IDs and exact locators. A citation must
support the whole proposition at the stated scope; table cells need citations
or an explicit source mapping. An abstract can support only what it actually
states. Do not claim to have read unavailable methods, results, or appendices.

Evidence states describe support, independently of verification:

| State | Meaning |
| --- | --- |
| `reported` | The source states the fact directly. |
| `derived` | It follows deterministically from recorded values; retain the derivation. |
| `inferred` | Interpretation across evidence, not a source's direct report. |
| `conflicting` | Reviewed sources disagree; record versions and settings. |
| `not-disclosed` | The reviewed sources do not supply the detail. |

Keep missing, uncertain, or unverified facts explicit. For an authorized internal
draft, AI source checks and pending human review belong in the existing record;
human verification remains `unverified` until an accountable human opens the
source and confirms the proposition, locator, and metadata. Never fabricate
`verified_by` or `verified_on`. If using `scientific-writing` tools, reuse their
required records with one mapping to existing IDs rather than duplicate content.

## Optional technical extraction

For a model lineage or training-recipe comparison, select relevant axes:

| Axis | Evidence to capture |
| --- | --- |
| Identity | family, release, checkpoint, parameter scale, date |
| Inheritance | base model, reused weights, predecessor components |
| Architecture | encoders, adapters, decoder, fusion, tokenization |
| Data | modality, sources, scale, mixture, filtering, synthesis |
| Stages | order, frozen/trainable modules, initialization |
| Objectives | next-token, contrastive, reconstruction, preference, RL |
| Curriculum | resolution, sequence length, temporal sampling, task mix |
| Alignment | instruction/preference data, reward, safety treatment |
| Optimization | disclosed compute, batch, optimizer, schedule, duration |
| Evidence | controls or ablations tied to claimed mechanisms |
| Gaps | details absent from reviewed sources or inaccessible artifacts |

Keep checkpoint-specific findings separate from family-level statements. Do not
fill a missing cell from a related release unless the source explicitly transfers
that setting. For other domains choose a relevant extraction scheme instead.

## Synthesis and stopping

Assess whether compared results share tasks, datasets, metrics, versions, and
conditions. Differences can explain disagreement; they do not license averaging
incompatible results or inferring a causal mechanism. Preserve contradictory
and negative evidence that changes the synthesis.

Track coverage by the in-scope units and comparison axes. Within the authorized
search bounds, stop when the review question is adequately addressed, additions
mostly duplicate evidence, or the agreed budget/access limit is reached. Report
remaining gaps and why retrieval stopped. Saturation is a practical stopping
rule, not proof that every relevant source was found. Living reviews retain the
existing evidence record and note the new cutoff and changed conclusions.
