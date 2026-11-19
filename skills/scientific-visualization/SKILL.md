---
name: scientific-visualization
description: Create, revise, or review scientific plots and figure panels based on measured data, analysis outputs, or experiment results. Use when the task involves how those data are encoded, read, or delivered.
license: MIT
allowed-tools: Read Write Edit Bash Glob Grep
metadata:
  compatibility: Works with the project's plotting tools. Optional bundled helpers use Python 3.11+. The pinned examples use uv. Kaleido v1 needs compatible Chrome/Chromium for Plotly static export.
  version: "1.2"
  skill-author: K-Dense Inc.
---

# Scientific Visualization

Start with the comparison or result the reader needs to see. Build on the project's plotting tools when available. Choose the panel layout, scales, colors, line styles, and labels to fit the data and intended display size. Keep visual mappings consistent across comparable panels. When color identifies groups or conditions, reinforce it with a suitable cue such as line style, marker shape, hatching, or direct labels. Check contrast against the actual background.

Preserve the raw data and native images. Keep the figure traceable to its sources and record the transformations that affect interpretation, including exclusions, normalization, aggregation, and random seeds that affect the result. Distinguish missing, censored, excluded, and zero values. Identify interpolated or modeled values when displayed. Label variables and units, and describe the estimator, interval, sample size, and unit of replication where relevant. Use baselines, axis limits, and color normalization that represent the data faithfully. Apply image adjustments consistently and disclose processing and composites in experimental images.

Choose export settings for the intended medium. Check the delivered figure at its intended size for readable labels, legends, and panel markings, adequate contrast, and clipping. Inspect the relevant file properties, such as physical dimensions, effective raster resolution, embedded fonts, or transparency. For web delivery, provide a text or data alternative and check interaction accessibility where applicable. When preparing files for journal submission, verify the current official guidance for the exact journal, article and figure type, and submission stage. Automated metadata or palette checks provide evidence about individual properties.

## References

- [Publication figure principles](references/publication_guidelines.md) for statistical displays, image integrity, and accessibility.
- [Color and contrast](references/color_palettes.md) for palette selection, normalization, and optional contrast checks.
- [Plotting and export examples](references/matplotlib_examples.md) for Matplotlib, Seaborn, Plotly, and optional bundled presets and helpers.
- [Journal requirements](references/journal_requirements.md) for dated, stage-specific publisher snapshots. Use the journal's live guidance for submission.
- [Sources and version snapshot](references/sources.md) for the technical references and tested versions.

Adapted from K-Dense's [Scientific Agent Skills](https://doi.org/10.48550/arXiv.2609.00065) under the MIT license.
