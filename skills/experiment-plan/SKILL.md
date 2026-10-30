---
name: "experiment-plan"
description: "Turn a research question or method proposal into a claim-driven software experiment plan with baselines, ablations, metrics, run order, and resource estimates. Use when the user requests detailed experimental design; this Skill plans work but does not authorize running it."
---

# Experiment Plan: Claim-Driven, Paper-Oriented Validation

Use the current task's research question, proposal, constraints, and existing records.

## Overview

Use this skill after the method is stable enough that the next question becomes: **what exact experiments should we run, in what order, to test the claims?** For a task that spans question formation through writing, use `research-cycle` to coordinate the broader work.

Turn a proposal into a compact **claim -> discriminating evidence -> run order** roadmap that tests:

1. whether the method solves the anchored problem
2. whether the dominant contribution accounts for the observed benefit
3. whether extra complexity is needed
4. whether any central frontier-model-era component adds value

## Planning heuristics

- Use the current task's research workspace and existing records; a task-local `research/` directory is one option when none exists.
- Start with one dominant claim and an optional supporting claim, a few decisive experiment blocks, and strong baseline families. Adjust their number to the question and constraints; these are compactness heuristics, not scientific acceptance thresholds.
- Choose repetitions and random seeds from the sources of stochastic variation, required precision, available variance estimates, budget, and a declared stopping rule. Do not prescribe a universal seed count or treat a completed count as sufficient evidence. If the rationale is not yet available, mark it pending; deterministic runs need no artificial seed repetition.

## Workflow

### Phase 0: Load the Proposal Context

Read the most relevant existing proposal, review, and research-record files when they exist; do not require particular filenames.

Reuse their claim/prediction IDs and artifact links. Preserve the plan version being tested and distinguish planned runs from actual outputs; do not rebuild completed work as a new plan.

Extract:

- **Problem Anchor**
- **Dominant contribution**
- **Optional supporting contribution**
- **Critical reviewer concerns**
- **Data / compute / timeline constraints**
- **Which frontier primitive is central, if any**

If these files do not exist, derive the same information from the user's prompt.

### Phase 1: State the Claims to Test

Before proposing experiments, write down the claims and predictions to test, including meaningful rival explanations.

Use this structure:

- **Primary claim**: the main testable contribution, such as better performance, efficiency, user experience, meeting a new need, or a mechanism-level advance
- **Supporting claim**: optional, only if it directly strengthens the main paper story
- **Rival explanation**: e.g. "the gain only comes from more parameters," "the gain only comes from a larger search space," or "the modern component adds no value"
- **Discriminating evidence**: what outcomes would support, challenge, or leave each claim unresolved under stated assumptions?

Keep only the claims needed to answer the question; record why additional inseparable claims are necessary when relevant.

When the contribution or its distinction from prior work needs clarification, read [research value and differentiation](../_shared/references/research-value-and-differentiation.md).

### Phase 2: Build the Experimental Storyline

Design the paper around a compact set of experiment blocks. Default to the following blocks and delete any that are not needed:

1. **Main anchor result** — does the method solve the actual bottleneck?
2. **Contribution validation** — do comparisons support the claimed value, and which contribution accounts for it?
3. **Simplicity / elegance check** — can a bigger or more fragmented version be avoided?
4. **Frontier necessity check** — if an LLM / VLM / Diffusion / RL-era component is central, is it actually the right tool?
5. **Failure analysis or qualitative diagnosis** — what does the method still miss?

For each block, decide whether it belongs in:

- **Main paper** — essential to defend the core claims
- **Appendix** — useful but non-blocking
- **Cut** — interesting, but not worth the paper budget

Prefer one strong baseline family over many weak baselines. If a stronger modern baseline exists, use it instead of padding the list.

### Phase 3: Specify Each Experiment Block

For every kept block, fully specify:

- **Claim / prediction tested**: reuse existing IDs
- **Why this block exists**
- **Dataset / split / task**
- **Compared systems**: strongest baselines, ablations, and variants only
- **Metrics**: decisive metrics first, secondary metrics second
- **Setup details**: backbone, frozen vs trainable parts, key hyperparameters, training budget, repetitions/seeds and their rationale
- **Decision criteria**: supporting, challenging, and indeterminate outcomes, plus the stopping rule
- **Failure interpretation**: distinguish an execution failure from a negative or inconclusive scientific result
- **Table / figure target**: where this result should appear in the paper

Special rules:

- **Contribution validation** should use comparisons and, where appropriate, ablations to test the claimed value and where it comes from. Originality requires comparison with prior literature; an ablation does not prove originality.
- A **simplicity check** should usually compare the final method against either an overbuilt variant or a tempting extra component that the paper intentionally rejects.
- A **frontier necessity check** should usually compare the chosen modern primitive against the strongest plausible simpler or older alternative.
- If the proposal is intentionally non-frontier, say so explicitly and skip the frontier block instead of forcing one.

### Phase 4: Turn the Plan Into an Execution Order

Build a realistic run order so the user knows what to do first.

Use this milestone structure:

1. **Sanity stage** — data pipeline, metric correctness, one quick overfit or toy split
2. **Baseline stage** — reproduce the strongest baseline(s)
3. **Main method stage** — run the final method on the primary setting
4. **Decision stage** — run the decisive comparisons and ablations for contribution validation, simplicity, and frontier necessity
5. **Polish stage** — robustness, qualitative figures, appendix extras

For each milestone, estimate:

- compute cost
- expected turnaround time
- stop / go decision gate
- risk and mitigation

Separate **must-run** from **nice-to-have** experiments.

### Phase 5: Write the Outputs

#### Step 5.1: Update the existing plan or research record

Reuse the existing file, section, IDs, and links. Create a separate plan only when it helps review or execution; `EXPERIMENT_PLAN.md` is an example filename. Adapt this structure to missing information rather than duplicating an existing record:

```markdown
# Experiment Plan

**Problem**: [problem]
**Method Thesis**: [one-sentence thesis]
**Date**: [today]
**Plan version / existing record**: [version and link]

## Claim Map
| Claim / Prediction ID | Why It Matters | Discriminating Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1    | ...             | ...                         | B1, B2        |

## Paper Storyline
- Main paper must test and report:
- Appendix can support:
- Experiments intentionally cut:

## Experiment Blocks

### Block 1: [Name]
- Claim / prediction tested:
- Why this block exists:
- Dataset / split / task:
- Compared systems:
- Metrics:
- Setup details and repetition/seed rationale:
- Decision criteria and stopping rule:
- Failure interpretation:
- Table / figure target:
- Priority: MUST-RUN / NICE-TO-HAVE

### Block 2: [Name]
...

## Run Order and Milestones
| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0        | ...  | ...  | ...           | ...  | ...  |

## Compute and Data Budget
- Total estimated GPU-hours:
- Data preparation needs:
- Human evaluation needs:
- Biggest bottleneck:

## Risks and Mitigations
- [Risk]:
- [Mitigation]:

## Final Checklist
- [ ] Main paper tables are covered
- [ ] Core claims have supporting, challenging, and indeterminate outcome criteria
- [ ] Contribution validation, simplicity, and any frontier contribution are tested where claimed
- [ ] Negative results, execution failures, and deviations have a place in the existing record
- [ ] Nice-to-have runs are separated from must-run runs
```

#### Step 5.2: Extend existing run tracking when useful

Use the current run table or linked run records. A separate `EXPERIMENT_TRACKER.md` is optional. Keep detailed setup and metrics in their existing records; this table can provide the connections:

```markdown
# Experiment Tracker

| Run ID | Claim / Prediction / Block | Plan version / planned setup | Actual run / output or failure | Analysis / figure / manuscript | Status / deviations |
|--------|----------------------------|------------------------------|--------------------------------|--------------------------------|---------------------|
| R001   | C1 / P1 / B1               | [plan and setup link]        | pending                        | pending                        | planned             |
```

After an authorized run, link its command, code/data/environment versions, actual parameters and seeds, and raw output or failure record. Analysis and figure/manuscript links are added when available. Preserve unsuccessful runs and the plan they tested; record deviations instead of silently rewriting the plan. Reuse existing IDs, or retain one mapping when a downstream tool requires a different format. Do not copy the same result into several registries.

#### Step 5.3: Present a Brief Summary to the User

```
Experiment plan ready.

Must-run blocks:
- [Block 1]
- [Block 2]

Highest-risk assumption:
- [risk]

Next proposed runs, subject to existing task authorization:
- [run or unresolved prerequisite]

Plan / research record: <existing file or section>
Run tracking, when needed: <existing table or file>
```

## Key Rules

- **Planning is not execution permission.** Run only software experiments already authorized for the task; never auto-run ROS nodes or physical-motion tests.

- **Every experiment needs a purpose.** Test a claim or prediction, distinguish rivals, or establish that the pipeline and metrics can produce interpretable evidence; cut runs that add no useful information.
- **Prefer a compact paper story.** Design the main comparisons first, then add the ablations needed to interpret them.
- **Defend simplicity explicitly.** If complexity is a concern, include a deletion study or a stronger-but-bloated variant comparison.
- **Test frontier choices explicitly.** If a modern primitive is central, compare it with the strongest plausible simpler alternative and report what the evidence supports.
- **Prefer strong baselines over long baseline lists.** A short, credible comparison set is better than a padded one.
- **Separate must-run from nice-to-have.** Do not let appendix ideas delay the core paper evidence.
- **Reuse proposal constraints.** Do not invent unrealistic budgets or data assumptions.
- **Do not fabricate results.** Plan evidence; do not claim evidence.

For broader research coordination use `research-cycle`; this Skill contributes the detailed experimental roadmap without requiring the upstream package's other commands.
