---
name: experimental-design
description: Plan randomization, blocking, independent replication, factorial/DOE combinations, and treatment or run layouts before data collection. Use when a scientific question depends on how units or runs are assigned to conditions.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
  compatibility: Python >=3.10 for optional local helpers. randomization.py needs numpy and pandas; DOE generators additionally need pyDOE3. Check existing dependencies before use.
  version: "1.4"
  skill-author: K-Dense Inc.
---

# Experimental Design

Choose the allocation and replication structure that can answer the research question. Randomization balances assignment in expectation; it does not guarantee balance in a realized sample or establish a causal conclusion on its own. Count independent experimental units separately from repeated measurements of those units.

## Scope and execution boundary

This Skill supplies general design and layout work. `experiment-plan` supplies software baselines, ablations, claim-driven run order, and resource estimates; `statistical-analysis` supplies analysis and reporting after collection. Use these only when actually available and relevant. A sample-size or model-specific Skill is optional, not a prerequisite: use authorized existing libraries or documented methods, and mark unsupported calculations pending.

A plan or generated schedule does not authorize data collection, software experiments, equipment operation, or external disclosure. Reuse existing ordinary software authorization within its scope; do not ask again merely because the work is called an experiment. ROS nodes or physical-motion tests remain human-first; automated execution needs explicit permission covering the device test. Respect applicable human/animal, data-use, and institutional boundaries when they are relevant.

## Workflow

1. **Resume the question and evidence.** Read the existing research record, claim/prediction IDs, data dictionary, constraints, and prior design versions. Add links or missing details there instead of starting a new registry.
2. **Define units and contrasts.** Record treatments/factor levels, outcome, allocation unit, independent replicate, measurement unit, and nesting/repeated-measure structure. Identify feasible factor ranges and what comparison or interaction the design must distinguish.
3. **Choose the structure.** Decide whether nuisance factors need blocks/strata, whether assignment occurs to individuals or clusters, and whether hard-to-change factors require restricted randomization. A permuted allocation block is not automatically an experimental batch/block; retain both labels when they differ.
4. **Justify replication and resources.** Base independent replicate counts on the precision/effect target, variance or correlation assumptions, design structure, budget, and stopping rule. State assumptions or pending estimates; no universal sample/seed minimum. Layout seeds reproduce an allocation, not independent scientific replication.
5. **Generate and inspect the planned layout.** Use the narrowest local helper or existing tooling. Check row counts, treatment combinations, unit-to-condition mapping, completed-block ratios, factor limits, aliasing/model estimability, and allowable processing order. Fixed-block schedules balance completed blocks; a truncated final block can be unbalanced. Run-order shuffling is insufficient for split-plot, batch, or position constraints unless those constraints are represented.
6. **Link the handoff.** In the current record, connect claim/prediction → design version/layout → proposed run IDs, with unit/block/cluster IDs, seed, helper/library versions, and analysis assumptions. Generated layouts are planned artifacts, not completed experiments. Later execution and deviations retain their own actual outputs and versions; analysis and figures link back to them.

## Choose references as needed

| Design question | Reference |
| --- | --- |
| Simple, blocked, stratified, or cluster allocation; batch/position constraints | [Randomization and blocking](references/randomization_and_blocking.md) |
| Full/fractional factorial, screening, response surface, or space filling; aliasing | [Factorial and DOE](references/factorial_and_doe.md) |
| Repeated measures, crossover, split plot, Latin square, or nesting | [Design types](references/design_types.md) |
| Planned interim looks or adaptive changes | [Sequential and adaptive designs](references/sequential_and_adaptive.md) |

These references describe design options, not universal clinical recommendations or execution permission. Confirm design-specific assumptions and current authoritative guidance for the actual domain; planning or preregistration alone does not make an analysis confirmatory.

## Optional local helpers

Read a helper's source before its first use and check installed dependencies. `scripts/randomization.py` provides allocation schedules and `assign_factorial_runs`; `scripts/doe_designs.py` provides full/fractional factorial, screening, response-surface, and Latin-hypercube matrices. Both return pandas DataFrames and make no network calls or experimental runs. They do not validate study suitability, model rank, alias structure, ethics, or allocation concealment.

Use the current project environment; dependency examples are not installation instructions or additional authorization. Install only missing capabilities within the authorized task and user home. Output paths, temporary files, and caches stay under the current user's actual home; do not use sudo. Keep real identifiers local where required and avoid overwriting an existing schedule.

For example, from an already available helper import path:

```python
from randomization import stratified_block_randomization

# Synthetic independent unit positions: real units need an existing ID mapping.
strata = ["batch_A", "batch_B"] * 4
layout = stratified_block_randomization(
    strata, arms=["condition_A", "condition_B"], block_size=4, seed=42
)
# unit_id retains each input position; inspect before saving to the task workspace.
```

The example seed is arbitrary. A counts dictionary creates synthetic sequential IDs; a stratum sequence preserves positional IDs. Neither replaces the project's real unit identifiers. Archive the actual layout and versions, and verify that serializing it preserves the inspected assignment. Public examples do not provide a secure allocation-concealment mechanism.

For central-composite designs, `face="circumscribed"` can create axial settings outside the supplied low/high factorial levels. Inspect every actual setting; use a suitable constrained design when ranges are hard limits, and do not clip rows to pretend the original design was retained. See the [NIST CCD comparison](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3361.htm).

## Source and license

Adapted from K-Dense Scientific Agent Skills, commit `91497e335489dcb544ec8ddc8f6b7ce5fd6d1121`; upstream metadata version `1.4`. This package includes the [K-Dense MIT license](LICENSE). Local changes clarify scope, record reuse, and helper behavior; they do not certify the upstream references.

## Citing Scientific Agent Skills

If these tools materially contributed to a research artifact, record their source/version in its methods or software provenance. Add a formal paper citation only after verifying the bibliographic record and the venue's requirements; never invent a reference or claim a network check that was not performed. Upstream suggests `arXiv:2609.00065` / `https://doi.org/10.48550/arXiv.2609.00065`; treat that suggestion as a lookup target until verified.
