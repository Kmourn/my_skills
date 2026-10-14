# Siblings, publishing, and credentials

Read this reference only for the requested remote/access or publication work.
Reuse the task's chosen target and existing authorization; creating/configuring
remotes and uploading data are separate mutations. All command examples are
templates, not setup steps to execute automatically. No paid service, cloud
account, or global configuration is required by this skill. Check installed help
for options that differ from the pinned upstream snapshot.

## The two-target model

Git history and annexed content can require different targets: a Git hosting
repository does not imply that annexed bytes are available. A Git sibling plus a
storage sibling, with a declared publication dependency, is one common arrangement.
Capable Git-annex services or filesystem/SSH repositories can serve both.

Getting this wrong produces the most common broken publication: collaborators clone
successfully, see every file listed, and then find every `datalad get` failing because the
content was never uploaded anywhere reachable.

## Managing siblings

```
datalad siblings [-h] [-d DATASET] [-s NAME] [--url [URL]] [--pushurl PUSHURL]
    [-D DESCRIPTION] [--fetch] [--as-common-datasrc NAME] [--publish-depends SIBLINGNAME]
    [--publish-by-default REFSPEC] [--annex-wanted EXPR] [--annex-required EXPR]
    [--annex-group EXPR] [--annex-groupwanted EXPR] [--inherit] [--no-annex-info]
    [-r] [-R LEVELS] [--version] [{query|add|remove|configure|enable}]
```

Five actions. `query` is the default and reports known siblings. `add` and `configure` are
the same operation except that adding a sibling whose name already exists fails while
reconfiguring does not. `enable` completes access for a git-annex special remote in a
fresh clone. `remove` de-configures a sibling.

Options that carry real consequences:

- `--publish-depends SIBLINGNAME` adds "a dependency such that the given existing sibling
  is always published prior to the new sibling". Set this on the Git sibling, naming the
  storage sibling, and the ordering problem stops being something anyone has to remember.
- `--annex-wanted EXPR` sets a git-annex preferred-content expression for the sibling, for
  example `standard` combined with a group, or `include=*.nii.gz`. `--annex-required`
  makes content mandatory there rather than merely wanted.
- `--pushurl` supplies a separate write URL when the read URL cannot be pushed to, the
  usual case for an HTTPS read path with an SSH write path.
- `--as-common-datasrc NAME` configures a sibling "as a common data source of the dataset
  that can be automatically used by all consumers", which is how a public mirror becomes
  usable by anyone who clones without them configuring anything.
- `--inherit` takes configuration from the superdataset's corresponding sibling, which
  matters when publishing a nested dataset hierarchy.

## Creating siblings

When remote creation is authorized, the relevant `create-sibling-*` command can
create the remote side and configure the local side together. Reuse existing
remotes when they satisfy the task:

| Command                                           | Target                          |
| ------------------------------------------------- | ------------------------------- |
| `datalad create-sibling-github`                   | A GitHub repository             |
| `datalad create-sibling-gitlab`                   | A GitLab project                |
| `datalad create-sibling-gogs` / `-gin` / `-gitea` | GOGS, GIN, and Gitea instances  |
| `datalad create-sibling-ria`                      | A RIA store                     |
| `datalad create-sibling`                          | A generic sibling over SSH      |

The `create-sibling-*` family covers *Git* siblings (a Git remote plus a hosting-service
repository or project) and the RIA layout, which packages a Git remote and a matching
git-annex special remote together. Storage-only targets — S3 buckets, WebDAV, plain SSH
directories, rclone-reachable services — are git-annex *special remotes* rather than Git
remotes, and they are created with `git annex initremote` rather than `create-sibling-*`.
That distinction is what the two-target model turns on: the Git sibling carries history,
the storage sibling carries content. RIA stores, GIN, and suitable filesystem/SSH
Git-annex repositories can serve both from one infrastructure location.

GIN is worth knowing about in a neuroscience context because it hosts annexed content
directly, which collapses the two-target model back into one target.

## RIA stores

A RIA store is a flat, filesystem-level layout for holding many datasets, designed for
cluster and institutional storage where per-dataset repositories are impractical. Clone
URLs use a `ria+` prefix and a fragment identifying the dataset:

```bash
datalad clone "$ria_clone_url" "$clone_directory"
```

Set these variables from the selected task. A clone URL's fragment is either the
full dataset ID or an alias prefixed with `~`; `ria+ssh://` and `ria+file://` use
the actual chosen host or filesystem location.

```bash
datalad create-sibling-ria -s "$ria_sibling" --alias "$dataset_alias" \
  --new-store-ok "$ria_store_url"
```

- `--new-store-ok` permits creating the store when it does not already exist. Without it,
  pointing at a nonexistent path is an error rather than a silent creation.
- `--alias` sets the friendly name used in the clone fragment.
- `--storage-sibling` controls the git-annex special remote. `off` disables it, and `only`
  creates the special remote without the regular RIA sibling.
- `--shared` sets multi-user permissions using the values `git init --shared` accepts.

By default the command creates both a regular sibling and a storage sibling named with a
`-storage` suffix and sets their publication dependency. RIA HTTP(S) access is read-only;
provide an SSH/file `--push-url` for writes. Quote RIA URLs so shell `#`, `~`, and bracket
interpretation cannot change them. Do not run ordinary git-annex commands directly
inside a RIA store; access its special layout through the ORA remote.

## Pushing

```
datalad push [-h] [-d DATASET] [--to SIBLING] [--since SINCE] [--data
    {anything|nothing|auto|auto-if-wanted}] [-f
    {all|gitpush|checkdatapresent}] [-r] [-R LEVELS] [-J NJOBS]
    [--version] [PATH ...]
```

`--data` controls annexed content transfer, and the default is `auto-if-wanted`:

| Value | Behaviour |
|---|---|
| `anything` | Transfer selected current annexed content without preferred-content filtering |
| `nothing` | Skip `git annex copy` entirely, publishing history only |
| `auto` | Let wanted expressions and required copy counts select transfers |
| `auto-if-wanted` | Default. Apply auto mode when wanted is configured; otherwise behave as `anything` |

Without a wanted expression, the default does transfer selected content; it is not a
history-only push. All modes are bounded by selected paths/current revision and local
content availability. A push is not an archive of every historical key. If later `get`
fails, inspect transfer results, missing local bytes, remote access, and wanted filters.
The upstream source reports a tiny directory-special-remote check of the default;
it was not repeated for this adaptation.

`--since SINCE` limits what is considered, and `--since '^'` uses the last known state of
the sibling's branch as the baseline. `-f/--force` accepts `gitpush` (override Git push
safety), `checkdatapresent` (skip the git-annex copy optimisation and transfer regardless
of what the remote is believed to hold), or `all`.

For an authorized publication to existing siblings, set the variables to the
selected Git sibling, storage sibling, and transfer policy. Configure a dependency
only if changing that configuration is within the task:

```bash
datalad siblings configure -s "$git_sibling" --publish-depends "$storage_sibling"
datalad push --to "$git_sibling" --data "$transfer_policy"
```

If the chosen storage backend is S3, its special remote is configured through
`git annex initremote`, not by treating an S3 URL as a Git sibling URL. Select the
backend's access/encryption options for the actual task; no new bucket is assumed.
`autoenable=true` lets a fresh clone reach the storage sibling
without a manual `enableremote` step when its other requirements are met. It does not
grant bucket access. `encryption=none` disables git-annex encryption; it does not make
an S3 bucket public. Configure access policy separately. For intended anonymous
downloads, set the special remote's `publicurl` to the reachable bucket/object URL and
verify it from an unauthenticated clone. Do not use the deprecated S3 `public` ACL
option for modern buckets. Private access and encryption are separate choices.

For a requested access check, use a separate permitted location and the task's
actual URL and representative file:

```bash
datalad clone "$published_dataset_url" "$verification_directory"
datalad get -d "$verification_directory" path/to/representative-file
```

## Credentials

DataLad resolves credentials in a defined order and stores interactively entered secrets
through the `keyring` package, using whichever backend that package finds on the system.
Configuration (including environment overrides) is checked before keyring lookup;
interactive prompting is a fallback. Review the active backend on headless hosts.

Three ways to supply them, in increasing order of automation:

1. **Interactive.** DataLad prompts when a credential is needed and not available, and
   stores the answer in the active keyring backend.
2. **Local configuration.** `datalad.credential.<name>.<component>` can supply a
   component, but keep secrets out of tracked `.datalad/config` and shared config files.
   Prefer a suitable keyring or process environment for credentials.
3. **Environment.** "Variable names take the form of `DATALAD_CREDENTIAL_<NAME>_<COMPONENT>`,
   and standard replacement rules into configuration variable names apply." The
   transformation replaces `__` with a hyphen, then `_` with a dot, then lowercases. Keep
   credential names simple and free of underscores so this stays predictable.

Setting `datalad.credentials.force-ask` can request interactive re-entry. Use it
only when credential replacement is part of the task; do not change global
credential configuration as a generic repair step or print secret values.

For git-annex special remotes on a fresh clone, the credential is not enough on its own.
The special remote also has to be enabled locally:

```bash
datalad siblings -d . enable -s store
# or, at the git-annex level
git annex enableremote store
```

A clone that reads Git history but cannot get content may have a disabled remote,
missing credentials, an inaccessible URL, or unpublished content. Check `git annex info`
and the transfer error to distinguish them. DataLad credentials do not automatically
configure every git-annex backend: the S3 special remote reads `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN` during initialization or
enabling. Keep `embedcreds` disabled unless its sharing/encryption behavior is intended.

Official contracts: [push](https://docs.datalad.org/en/stable/generated/man/datalad-push.html),
[GitHub sibling](https://docs.datalad.org/en/stable/generated/man/datalad-create-sibling-github.html),
[RIA](https://docs.datalad.org/en/stable/generated/man/datalad-create-sibling-ria.html),
[S3 special remote](https://git-annex.branchable.com/special_remotes/S3/), and
[credentials](https://docs.datalad.org/en/stable/design/credentials.html).

Keep credentials out of tracked files and shared logs. Git history can retain a
secret after it is removed from the current file.
