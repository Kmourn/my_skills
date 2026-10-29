# GPT–DeepSeek Academic Writing

Use the locally configured DeepSeek API when it helps drafting or revising scholarly
prose. This is an allowed writing collaboration, not a requirement to call both models
for every task. Honor an explicit provider choice or a local-only restriction.

## Division of work

- **GPT develops the content:** propose ideas, organize the argument, explain the
  method and mathematics, and identify the evidence and conditions supporting each
  claim. Treat proposed ideas and interpretations according to their actual evidence.
- **DeepSeek develops the expression:** improve explanation, information order,
  paragraph development, transitions, and the target journal's register using that
  content. Allow sentence and paragraph restructuring and useful explanatory expansion;
  preserving meaning does not require preserving the original wording or sentence count.
- **GPT integrates the result:** check scientific meaning, resolve concrete discrepancies,
  and keep successful prose. Human authors retain scientific decisions and final approval.

For an expression pass, apply the relevant `academic-voice` or `ieee-polishing` guidance
when available. Keep the manuscript voice convention in `writing_principles.md`,
including the established first-person preference; avoid mechanical passive rewriting.

## Prepare and delegate

Give DeepSeek the passage or sections needed for the task, the intended reader and
journal, the argument to convey, and the facts, formulas, terms, citations, conditions,
and uncertainties that must survive. Include an authorized reference passage when its
expression is useful. Resolve scientific decisions in GPT's content brief or leave
them explicitly open; do not ask a language pass to invent the missing answer.

Ask for the revised prose and any material ambiguity encountered. Limit the assignment
to expression rather than source discovery, additional provider calls, or recursive
delegation. A passage may need more explanation, not fewer words. Necessary technical
conditions should be legible beside the claim without becoming repeated defensive prose.

## Review without undoing the expression work

Compare the revision with the supplied scientific content: facts and numbers, formula
meaning, terminology, citation intent, method details, causal strength, assumptions,
sampling units, negative findings, and scope. Check the actual differences; do not
turn an ordinary language edit into a full submission audit.

Retain improvements in explanatory depth, continuity, emphasis, and journal register
when the meaning is faithful. Do not replace them with GPT's earlier wording merely to
make the prose shorter, more guarded, or stylistically uniform. Supported conclusions
should remain clear and affirmative, with qualifications matched to the evidence.

For a concrete discrepancy, return the affected span and its scientific constraint for
targeted correction, or correct that discrepancy directly. Keep accepted passages
intact unless the change affects their meaning or continuity. Evaluate readability and
scientific fidelity separately; a structural check alone establishes neither.

## Call boundary and records

Reuse the client's existing DeepSeek route or API configuration; on a machine that
already provides `codex-task deepseek`, that route may be used. Resolve the actual
provider, model, credentials, and supported parameters locally rather than embedding
a machine path, API key, or model assumption in the skill. Keep the active GPT
configuration in place. If the route is unavailable, report that and keep any draft
work local.

Apply the existing confidentiality boundary. Authorization already covering the task's
material, purpose, provider, and processing scope carries forward without per-call
confirmation. This permission does not expand access to unrelated private files or
override a known restriction; clarify only a genuinely unresolved transfer boundary.

Record the actual provider/model, relevant request settings, affected source version,
and accepted changes in the task's existing record. Distinguish a requested parameter
from a returned value and a proposed call from an executed one. Keep credentials in
the existing client credential storage or environment and never commit them. Private
request/response bodies stay in the authorized local task workspace, outside the
portable Skill repository. The bundled scientific-writing CLIs remain offline.
