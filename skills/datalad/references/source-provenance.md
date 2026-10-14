# Source provenance and local adaptation

## Fixed source

- Repository: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills).
- Package tag: `v2.72.0`; actual tag resolution on 2026-10-14 returned the lightweight
  tag commit [`526ebce143bc326f44471554e33d66a19c840360`](https://github.com/K-Dense-AI/scientific-agent-skills/commit/526ebce143bc326f44471554e33d66a19c840360).
  No `main` upgrade was used.
- Source directory: [`skills/datalad`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/datalad).
  Upstream skill metadata version: `1.2`; local adapted version: `1.2-local.1`.
- Import method: the deployed system `skill-installer` helper, using the full
  commit as `--ref` and an explicit staging destination. Temporary download data
  was kept in the actual user's home cache through `TMPDIR`; neither `HOME` nor
  `CODEX_HOME` was redirected. The reviewed package contains four Markdown files
  and no scripts, assets, global hooks, or runtime installer.
- License: upstream repository-root `LICENSE.md`, copied as
  [LICENSE.md](../LICENSE.md) with its complete MIT notice and original bytes.
  It retains `Copyright (c) 2025 K-Dense Inc.`; the upstream skill author is
  Dylan Pulver. Runtime software and remote backends have their own licenses.
- Upstream acknowledges conceptual scope informed by
  [bcmcpher's datalad-cli plugin](https://github.com/bcmcpher/my-skills/tree/main/plugins/datalad-cli).
  That plugin is not a dependency or an additional imported source in this package.

The fixed source was reviewed as data before adoption. Source commands were not
executed. The installer copy and separately fetched fixed-commit entry/reference
files were compared byte for byte. Source review copies and local check artifacts
remain outside this distributable package.

## Original source bytes

These hashes describe the upstream files before local adaptation. The license
hash also describes the unchanged packaged license; the other four hashes do not
describe the adapted local files.

| Upstream path | SHA256 | Bytes |
| --- | --- | ---: |
| `skills/datalad/SKILL.md` | `bb902427db0c501db4187aafd3433eea67fa1071348cf07adcea2558ed49debb` | 17431 |
| `skills/datalad/references/data-access.md` | `f419bd39ca536562238d7404f0eaa4836c444d38df0cf7121befe936d529b1c7` | 9714 |
| `skills/datalad/references/provenance.md` | `d9e56071463c5c118800ff5a800dd58ae5de38d04fc465c119ae0c690fc1c542` | 14087 |
| `skills/datalad/references/publishing.md` | `a5efdceeea8086549917e9e2b3bc526c8c7ec9f1e31a8a438c5e8ba9dd18d6cd` | 11174 |
| Repository-root `LICENSE.md` | `09b02a3c9df3053c55531d503357a9c7cde275970e6c3ceaa1ddf5f0e90b40c1` | 1068 |

## Adaptation scope

The entry routes DataLad datasets, missing annex content, explicit run/rerun
workflows, and dataset publication. Small ordinary Git code/text projects do not
activate a DataLad migration. It preserves current task authorization and existing
research records rather than creating a new session-control or research-record
system.

Fixed operating-system, package-manager, architecture, and version installation
recipes were replaced with environment inspection and separate dataset, optional
Python API, optional container, and remote-access dependencies. Skill adoption
does not install these runtimes, change global configuration, or grant permission
for experiments, replays, deletion, remote creation, or publication.

All three technical references remain reachable from the entry and are read by
task. Edits keep the clone/get and content-state distinctions, run/rerun caveats,
and Git-versus-storage remote model while making YODA/STAMPED optional, preserving
unsaved work, using task-selected destinations, and removing assumed `/tmp`
verification paths, default GitHub/S3 creation, and implied local test results.
Historical release-specific details are labeled as the upstream snapshot and
checked against installed help when used. No paid service is a required dependency.

## Validation and limits

The local checks on 2026-10-14 cover the Codex skill frontmatter validator,
package-local Markdown reference targets, exact license bytes, file inventory,
absence of symlinks/scripts, and whitespace errors. The official current
[run](https://docs.datalad.org/en/stable/generated/man/datalad-run.html),
[rerun](https://docs.datalad.org/en/stable/generated/man/datalad-rerun.html),
[get](https://docs.datalad.org/en/stable/generated/man/datalad-get.html), and
[push](https://docs.datalad.org/en/stable/generated/man/datalad-push.html) manuals
were read for key command and transfer semantics. This is not an exhaustive
reverification of every historical backend or release-specific reference claim.

DataLad and git-annex were absent from the implementation environment. No runtime
was installed, and no DataLad CLI help, clone/get/drop, scientific computation,
run/rerun, container execution, authenticated remote access, or publication was
executed. The successful import helper validates the download/import workflow;
it is not a DataLad functionality test. Upstream runtime checks reported in the
source are historical and are not credited as local checks.
