---
name: datalad
description: Retrieve and version DataLad datasets with selective content access, record authorized computations with run/rerun, and distinguish Git history remotes from annex content storage. Use for a DataLad dataset, unavailable annexed file content, an explicitly requested DataLad provenance workflow, or publication of an existing DataLad dataset. Ordinary small code/text Git projects do not require this skill.
license: MIT
metadata:
  version: "1.2-local.1"
  skill-author: Dylan Pulver; locally adapted in my_skills
  compatibility: Dataset operations need DataLad, Git, and git-annex in the selected environment. Python API use additionally needs a compatible Python environment. Containers need the optional datalad-container extension and the selected compatible runtime. Remote access may need network access and provider credentials.
---

# DataLad

DataLad combines Git history with git-annex content tracking. A clone can contain
the history and file pointers without the large file bytes; subdatasets also keep
their own histories and may remain uninstalled. Retrieve the requested content
with `datalad get` rather than assuming that a listed file is readable.

## Scope and environment

Reuse the selected dataset, existing research records, run/output IDs, task
authorization, and available environment. DataLad run records supplement those
records; they do not replace a research plan or establish scientific validity.
Installing this skill grants no additional permission to fetch an entire dataset,
execute or replay research, delete data, create remotes, or publish content. Carry
out operations covered by the current task; resolve only missing authorization
that affects the next operation.

Use plain Git for a small code/text project unless the user asks for DataLad or the
task needs annexed content, selective retrieval, independent subdatasets, or its
execution records. Do not migrate an existing project merely to add provenance.

Check the selected environment before proposing installation:

- **Dataset operations:** DataLad, Git, and git-annex executables. Use the installed
  command help/version information; version-specific options in the references
  are examples from the source snapshot.
- **Python API:** a compatible Python environment with DataLad, only when the task
  uses the API rather than an existing CLI.
- **Containers:** `datalad-container` plus the runtime and image actually selected
  for the task. The runtime may be Apptainer, Singularity, or Docker when supported
  by that extension/image configuration; do not assume interchangeability.
- **Remote access:** the selected backend's network access and credentials.
  Existing local content can be inspected without remote access.

Reuse working environments. If a required component is absent, explain which
operation it blocks and choose an installation method only within the user's
authorized environment and filesystem boundary. Skill installation does not
require installing the full DataLad or container runtime. Avoid global Git identity,
package, credential, or client configuration changes. Optional diagnostics such
as `datalad wtf --section dependencies` may help; do not publish secrets or private
configuration from diagnostic output.

## Inspect and retrieve data

Start from the task's actual dataset and requested paths. Useful inspections are
`datalad status --annex availability`, `datalad subdatasets`, and
`git annex whereis PATH` (replace `PATH` with the selected file). `whereis` reports
recorded locations, not a live guarantee that another copy is reachable.

Within the selected dataset, these are command templates; substitute the task's
paths and options before execution:

```bash
datalad get path/to/input
datalad get -n path/to/subdataset
```

The first retrieves selected file content. The second installs a subdataset's
structure without fetching its file bytes. Bound recursive retrieval to the
requested paths/depth; a broad `get -r .` can retrieve a large hierarchy.

A broken symlink, small pointer file, or unreadable annexed file can mean absent
content. Confirm the annex state before diagnosing corruption. Before modifying
annexed content, use the dataset's unlock/save workflow or declare it as a run
output. Preserve unsaved user work and do not discard it to make a command pass.
Read [data access](references/data-access.md) for clone/get, subdatasets, content
states, and requested drop/verification operations. Dropping local bytes, removing
a tracked path, and uninstalling a subdataset have different effects; select the
operation the user requested and retain the normal availability checks.

## Record and replay an authorized computation

Identify the command, versioned scripts/environment description, inputs, outputs,
seeds/settings, and the existing research record before running. Save intended
dependencies within the task's scope. An unchanged dataset produces no run commit.

For a task whose actual paths match this example:

```bash
datalad run --dry-run basic \
  --input code/analyze.py --input data/input.csv \
  --input environment.lock --output results/summary.csv \
  "python code/analyze.py {inputs[1]} {outputs[0]}"
```

`--dry-run` shows preparation and expansion; it does not execute or validate the
analysis. After checking the command and authorization, omit `--dry-run basic` to
execute and record the changed outputs. Use the task's actual interpreter and
interface instead of assuming the illustrative `python` command is available.
Inputs are retrieved and outputs prepared for writing. `--explicit` records only
declared outputs and can permit a dirty dataset; it does not capture unsaved input
changes. Use it only when that scope is intentional.

`datalad rerun --report REVISION` inspects a selected replay without executing it.
An authorized `rerun` executes commands and can alter files or check out a branch;
`-b` still uses the same worktree. Use a separate permitted clone/worktree for an
independent replay when needed and restore recorded subdataset revisions. Compare
actual output identities/checksums and appropriate numerical tolerances, and
retain errors and deviations in the existing research record.

`run`/`rerun` do not freeze host software, credentials, external services, or random
state. A tracked environment specification or optional container improves the
record, but actual replay and comparison are needed for a reproducibility claim.
Read [computational provenance](references/provenance.md) for command semantics,
replay ranges, optional YODA/STAMPED guidance, containers, and export limits.
Preserve the current project layout unless changing it is part of the task.

## Distinguish history publication from content publication

A Git sibling carries history and pointers. Annex content needs an accessible
data store: a git-annex special remote or a capable Git-annex sibling. One service
can support both, but a Git hosting repository alone does not imply that large
content is available. S3 and similar storage URLs are not Git remote URLs.

For requested publication, inspect the existing siblings and task-selected target,
content scope, access policy, and credentials. A publication dependency can arrange
for content storage to be pushed before the Git sibling. `datalad push` may transfer
content by default; `--data nothing` skips annex content, while other policies
depend on selected paths, available bytes, and preferred-content settings. It does
not archive every historical content key.

Creating/configuring a remote and publishing are separate mutations. Reuse the
actual authorization for each; do not create a cloud account, bucket, or repository
as a default setup step. For an authorized publication, verify representative
`clone`/`get` access from an appropriate separate location and report any access or
content gaps. Keep credentials out of tracked files and logs. Read
[publishing and credentials](references/publishing.md) for siblings, optional RIA
stores/backends, transfer policies, and backend-specific access requirements.

## Sources and validation limits

This is a local adaptation of K-Dense-AI/scientific-agent-skills, package v2.72.0,
DataLad skill 1.2. The source commit, exact MIT notice, adaptation scope, and checks
are recorded in [source provenance](references/source-provenance.md) and
[LICENSE.md](LICENSE.md). Upstream test claims are historical source information;
they do not establish that DataLad works in the current environment.

For options or compatibility beyond the installed help, consult the primary
[DataLad manual](https://docs.datalad.org/en/stable/),
[DataLad Handbook](https://handbook.datalad.org/en/latest/),
[container extension](https://docs.datalad.org/projects/container/en/stable/), and
[git-annex documentation](https://git-annex.branchable.com/).
