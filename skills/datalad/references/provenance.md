# Computational provenance with DataLad

Use this reference for an authorized record or replay of the selected computation.
Command forms and release-specific details come from the pinned upstream snapshot;
check the installed help before using them. Preserve existing research records and
the project layout. YODA, STAMPED, containers, and provenance exports below are
optional guidance, not prerequisites or an instruction to rebuild the project.

## Why this is the interesting half

Version control tells you that a file changed. Provenance tells you what produced it, from
what, and with which software. `datalad run` records the command and tracked inputs/outputs
in the same commit as the change. Capturing software versions additionally requires a
versioned environment specification or a tracked container; an executable name alone
does not identify its installed build. `datalad rerun` reads the record and re-executes
it. Actual output comparison and the relevant scientific checks remain separate.

## Principles: STAMPED, and the YODA layout it grew out of

YODA ("YODAs Organigram on Data Analysis") is the convention DataLad analyses were
originally built on, and it is still what `datalad create -c yoda` configures. Its three
principles (one thing one dataset, record where the data came from, record what was done
to it) describe what a well-formed analysis looks like, but they were inspirational rather
than operational: there is nothing in them to check a dataset against.

STAMPED (<https://stamped-principles.org>) is the operationalized successor, formalized by
some of the original YODA authors. It states seven properties of a reproducible research
object, each backed by normative MUST/SHOULD/MAY requirements:

| Property | Core requirement |
|---|---|
| **S**elf-contained | Everything essential to replicate the computation is reachable within a single top-level research object |
| **T**racked | Persistent content identification and provenance are recorded for every component and every modification, including the versions involved |
| **A**ctionable | The object carries enough instruction to reproduce all results, specified as *executable* specifications rather than prose |
| **M**odular | Components are organized as independently versioned modules, included directly or linked as subdatasets |
| **P**ortable | Procedures depend on no undocumented host state; environments are explicitly specified and version controlled |
| **E**phemeral | Results are produced in disposable environments built only from the object's own contents |
| **D**istributable | Every referenced module and component is persistently retrievable by others |

**Actionable is the property `datalad run` exists to satisfy.** A README describing how a
figure was produced is documentation; a run record is an executable specification, and
`datalad rerun` is what makes it executable. The same commit satisfies Tracked, because
the command, its inputs, its outputs, and the versions they were taken at are recorded
next to the change rather than in a separate log that can drift away from it. Modular maps
onto subdatasets, Portable onto tracked images and runtime specifications, Ephemeral onto disposable
execution environments, and Distributable onto
siblings and RIA stores (see [publishing.md](publishing.md)).

Two companion resources make this checkable rather than aspirational:
<https://checklist.stamped-principles.org> walks the requirements as a MUST/SHOULD/MAY
checklist, and <https://examples.stamped-principles.org> collects worked patterns,
including ones built directly on `datalad run` and `datalad rerun`.

### The YODA layout in practice

If creating a new analysis dataset with this layout is part of the task:

```bash
datalad create -c yoda "my_analysis"
```

That produces:

```text
.
├── .gitattributes
├── CHANGELOG.md
├── code
│   ├── .gitattributes
│   └── README.md
└── README.md
```

The configuration matters more than the directories. Everything in `code/`, plus
`README.md` and `CHANGELOG.md`, is tracked by Git rather than git-annex, so scripts stay
directly readable and diffable in a clone that has fetched no data at all. Input data is
then added as a subdataset:

```bash
datalad clone -d . "$dataset_url" inputs/raw
```

Set `dataset_url` to the dataset selected for the task. `-d .` registers the clone
as a subdataset of the current analysis dataset.

## datalad run

```
datalad run [-h] [-d DATASET] [-i PATH] [-o PATH] [--expand {inputs|outputs|both}]
    [--assume-ready {inputs|outputs|both}] [--explicit] [-m MESSAGE]
    [--sidecar {yes|no}] [--dry-run {basic|command}]
    [--on-cmd-failure {error|save|all}] [-J NJOBS]
    [--version] ...
```

| Option | Documented behaviour | Practical consequence |
|---|---|---|
| `-i/--input PATH` | Retrieve content for the specified dependency before execution | Makes the declared input available and records what replay should prepare |
| `-o/--output PATH` | Prepare the selected target for writing | Unlocks or removes the target so git-annex write protection does not block the write |
| `--explicit` | Permit a dirty dataset and save only declared outputs | Does not capture unsaved input changes; use only for an intentional, documented scope |
| `--assume-ready {inputs\|outputs\|both}` | Skip the selected preparation steps | Use only when inputs are already present and outputs already writable |
| `--expand {inputs\|outputs\|both}` | Save expanded file lists for the selected globs | Makes the recorded selection explicit when a glob's meaning could change |
| `--dry-run {basic\|command}` | Display execution details without running the command | Does not validate numerical results or scientific conclusions |
| `--sidecar {yes\|no}` | Store the run record in a separate file rather than in the commit message | Keeps long records out of `git log` output |

Placeholders available in the command string: `{pwd}` (current working directory),
`{dspath}` (dataset path), `{tmpdir}` (a temporary directory), `{inputs}` and `{outputs}`
(the values of the corresponding flags), and `{inputs[0]}` for indexed access.

Globs are permitted in `--input` and `--output`, and multiple flags may be given:

```bash
datalad run -m "second-level model" \
  -i "derivatives/sub-*/func/*_bold.nii.gz" \
  -i "code/model.py" \
  -o "results/group_map.nii.gz" \
  --expand inputs \
  "python code/model.py {outputs}"
```

### The run record

The commit message carries a machine-readable JSON block between the markers
`=== Do not change lines below ===` and `^^^ Do not change lines above ^^^`. It records
the command, the dataset ID, the exit status, and the input and output specifications. The
record is parsed by `datalad rerun`. Preserve it during editing/rebasing;
hand-edited records can make replay fail or misrepresent the command.

Two behaviours that surprise people:

- A run producing no change to the dataset produces no commit at all, exactly as a
  `datalad save` with nothing to save does. An empty history entry is not evidence the run
  failed to execute, only that it changed nothing.
- `datalad run` refuses to start in a dirty dataset. This is the point of the command: a
  record built on an unknown starting state does not establish reproducibility. Save
  intended dependencies within the task's scope or use an intentional `--explicit`
  scope; do not discard unrelated user work.

### Failed command provenance

DataLad 1.6.5 exposes `--on-cmd-failure error|save|all`. The default `error` stops
without saving; `save` records changed outputs and returns success; `all` saves
changed outputs and preserves the failing exit code. Inspect the run record
`exit` field when evaluating results: a successful DataLad invocation need not
mean the scientific command succeeded. On replay, a recorded nonzero code can
be accepted when repeated, and a zero exit is accepted even if the original failed.
A run producing no tracked changes still has no commit. These options are distinct
from global result handling via `--on-failure`.

## datalad rerun

```
datalad rerun [-h] [--since SINCE] [-d DATASET] [-b NAME] [-m MESSAGE] [--onto base]
    [--script FILE] [--report] [--assume-ready {inputs|outputs|both}] [--explicit]
    [--on-cmd-failure {error|save|all}] [-J NJOBS] [--version] [REVISION]
```

- `REVISION` selects which recorded command to replay and defaults to `HEAD`.
- `--since SINCE` selects the commits reachable from the chosen revision but not
  from `SINCE`, corresponding to `git log SINCE..REVISION`.
- `--onto base` selects the starting state; the default uses `HEAD`.
  Use `--onto ''` to start at the parent of the first run commit selected
  for replay. This resets the top-level dataset only; installed subdataset worktrees
  do not automatically move to their recorded commits.
- `-b/--branch NAME` creates and checks out a branch before replaying in the same
  worktree. A new branch does not isolate modified files from another user of that tree.
- `--report` displays the selected replay without executing it.
- `--script FILE` extracts the commands to a file instead of running them, with `-` for
  stdout. This is how a DataLad history becomes a plain shell script for a reviewer or a
  cluster submission.

For an authorized replay, use a separate permitted clone when the check needs
isolation. The variables below must name the actual first run commit and recorded
result revision; inspect with `--report` before the selected execution:

```bash
datalad rerun --report --since "${first_run_commit}^" "$recorded_result_revision"
datalad rerun --onto= -b repro-check --since "${first_run_commit}^" "$recorded_result_revision"
git diff "$recorded_result_revision" HEAD -- results/
```

This comparison checks tracked output identities, including annex keys. It does not
by itself establish numerical or scientific validity. Use a disposable clone for a
fresh-environment check, restore recorded subdataset revisions, and inspect tolerances,
randomness, and software versions separately. The example is a template, not a
runtime test performed for this adaptation.

## Containers

The optional `datalad-container` extension can record a selected image alongside
the command. The pinned upstream source reviewed release 1.2.6; reuse a compatible
installed extension/runtime and check its help rather than installing that version
automatically.

```
datalad containers-add [-h] [-u URL] [-d DATASET] [--call-fmt FORMAT]
    [-i IMAGE] [--update] [--extra-input FILE] [--version] NAME
```

Container source options from the upstream review (runtime examples illustrative):

- A local SIF file plus `--call-fmt 'apptainer exec {img} {cmd}'` avoids assuming a
  `singularity` executable exists when only Apptainer is installed.
- `docker://debian:stable-slim` builds a Singularity image. In 1.2.6 the released
  `containers-add` implementation invokes `singularity build` and its guessed call
  format uses `singularity exec`; it does not automatically substitute `apptainer`
  for this path. Build the SIF externally with Apptainer, then register the local file.
- `dhub://debian:stable-slim` uses Docker, saves the pulled image into the dataset,
  and configures a Docker adapter with the current directory mounted at `/tmp`.
- `shub://` remains recognized by the extension, but its legacy Singularity Hub
  service was not verified in this review. Prefer a retrievable local image or an
  actively maintained registry source.

Use an immutable registry digest when building an image, retain the resulting image,
and record its architecture. A mutable tag alone does not pin software. Configure
required binds/environment/GPU options in the tracked call format and declare overlays
with `--extra-input`. Container tracking alone does not isolate host mounts or ensure
cross-platform numerical equivalence.

```
datalad containers-run [-h] [-n NAME] [-d DATASET] [-i PATH] [-o PATH] [-m MESSAGE]
    [--expand {inputs|outputs|both}] [--explicit] [--sidecar {yes|no}] [--version] ...
```

`-n/--container-name` selects a configured container by name or path. With exactly
one container configured it may be
omitted. During execution the environment variable `DATALAD_CONTAINER_NAME` holds the name
of the container in use, which is available to the command itself.

The image is tracked in the dataset like any other file, so it is annexed content: a
collaborator gets it with `datalad get` and the provenance record points at a specific
image rather than at a tag someone may have re-pushed.

## Exporting provenance to a standard form

DataLad's run records are DataLad's own format. Converting them to an interoperable
representation is an open area rather than a solved one, and this is worth stating plainly
rather than implying a pipeline exists:

- **W3C PROV** is the standard target for provenance interchange. See
  <https://www.w3.org/TR/prov-overview/>.
- **datalad-metalad** ships a `runprov` extractor that reads DataLad run records, at
  <https://github.com/datalad/datalad-metalad/blob/master/datalad_metalad/extractors/runprov.py>.
  Its source exposes run-record extraction and JSON-LD-style provenance; compatibility
  and exported graph validity were not executed here, so validate them before adoption.
- **BIDS BEP028** tracks the provenance extension at
  <https://bids.neuroimaging.io/extensions/beps/bep_028.html>. Check its current proposal and the adopted BIDS
  version before choosing an export schema; a proposal is not a validated conversion API.

Until one of those is settled, the durable artifact is the DataLad history itself plus
`datalad rerun --script`, which produces a plain, reviewable command sequence that does
not depend on DataLad to read.

## Further reading

- `datalad run` chapter of the handbook:
  <https://handbook.datalad.org/en/latest/basics/101-108-run.html>
- YODA principles: <https://handbook.datalad.org/en/latest/basics/101-127-yoda.html>
- STAMPED principles (operationalized from YODA): <https://stamped-principles.org>
  - Compliance checklist: <https://checklist.stamped-principles.org>
  - Worked examples and stencils: <https://examples.stamped-principles.org>
- datalad-container documentation:
  <https://docs.datalad.org/projects/container/en/stable/>
