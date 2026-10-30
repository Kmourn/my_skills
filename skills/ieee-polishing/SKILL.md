---
name: ieee-polishing
description: Polish, translate, diagnose, and restructure technical manuscript text into IEEE-style academic English using routed failure-mode guidance. Use for IEEE abstracts, introductions, related work, methods, experiments, conclusions, figure captions, rebuttals, Chinese-to-English technical writing, AI-like or template-like academic prose, and engineering prose that needs clearer problem logic, contribution framing, method rationale, evidence discipline, natural author voice, or reviewer-ready wording.
---

# IEEE Polishing Router

Use this skill for IEEE-style language and logic polishing. Polishing means repairing both prose and technical argument structure.

Preserve the project and author's established voice choices. The local manuscript
default favors concrete technical subjects over first person, except when explicitly
naming the authors' own concept or method. This is a local preference, not an IEEE
rule; honor an explicitly requested voice and avoid mechanical passive constructions.

Do not polish only from memory. Follow the routing protocol and load the selected fragments.

For author-directed edits to manuscript files, first follow
[human-directed revision](../scientific-writing/references/human-directed-revision.md)
to propose the location, replacement, and scope for approval before writing. Return
the polished proposal in chat while approval is pending.

## Routing Protocol

1. Read `manifest.yaml`.
2. Read every file listed under `always_load`.
3. Detect the axes:
   - `section`: title / abstract / introduction / related-work / method / experiments / conclusion / caption / response / standalone.
   - `language`: en / zh-to-en.
   - `failure_mode`: vague-claims / unsupported-novelty / weak-contribution / poor-method-rationale / chinglish / result-underreporting / ai-like-prose.
   - `polish_depth`: light / standard / structural.
4. State the detected axes in one short line before editing.
5. Load only the matching fragments.
6. Polish with this priority order:
   - preserve facts,
   - repair IEEE engineering logic,
   - align with section purpose,
   - apply failure-mode repair,
   - improve sentence-level English.

## Red Lines

Do not invent numerical results, datasets, baselines, citations, equations, algorithms, or claims.

Do not hide a missing-evidence problem behind fluent English. Flag it.

Do not over-polish into Nature-style broad-interest prose. Keep IEEE direct, technical, and verifiable.

## Output Contract

Default: return the polished text first, then a short `Notes` block only when you made structural repairs or the text still needs evidence.

For intensive editing requests, return a table with `Issue | Revision | Reason`.
