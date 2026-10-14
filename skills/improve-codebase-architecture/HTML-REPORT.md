# HTML Report Format

When an HTML report is needed, render a single self-contained file at the user's requested location within the applicable write boundary; otherwise use the task workspace within the current user's actual home directory. Use inline CSS and native HTML/SVG. If an existing local Mermaid renderer is useful, embed its rendered output rather than loading remote scripts. Report the artifact path and any actual remaining dependencies.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Architecture review for {{repo name}}</title>
    <style>
      body { margin: 0; background: #fafaf9; color: #0f172a; font: 16px/1.5 system-ui, sans-serif; }
      main { max-width: 64rem; margin: auto; padding: 2rem 1rem; }
      header, section { margin-bottom: 2rem; }
      article, .diagram-card { border: 1px solid #cbd5e1; border-radius: .5rem; background: white; padding: 1rem; }
      svg { max-width: 100%; height: auto; }
      code, pre { font-family: ui-monospace, monospace; }
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body>
    <main>
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph. Straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is plain and follows the project's terms. When additional structural vocabulary helps, consult the available [modularity language reference](../reviewing-code-modularity-skill/references/language.md); no separate glossary Skill is required.

Each candidate is one `<article>`:

- **Title**: short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row**: recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files**: a readable monospaced list using inline CSS.
- **Before / After diagram**: the centrepiece. Two columns, side by side. See patterns below.
- **Problem**: one sentence. What hurts.
- **Solution**: one sentence. What changes.
- **Wins**: bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable): one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same. Variety is part of the point.

### Dependencies / call flow

Use a small native SVG or locally rendered Mermaid graph when dependency or call flow is the point. Embed the result in a card; color relevant leakage edges red. A local renderer is optional, and raw Mermaid text is not a rendered diagram.

```html
<div class="diagram-card">
  <!-- Insert the actual native SVG or locally rendered diagram here. -->
</div>
```

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals, since Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands styled with inline CSS to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module: one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Use generous whitespace and a readable existing font; serif headings are optional.
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use readable labels sized for the final view; inline CSS can distinguish structural labels from UI text.
- The default report is static and has no external script, stylesheet, font, or image dependency. An optional external resource must be disclosed rather than called self-contained.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Use concise language and the project's architectural nouns. Terms such as module, interface, implementation, depth, seam and adapter are useful when their meaning matches the code; retain component, service or API when those are the project's actual concepts.

**Phrasings that fit the style:**

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name a concrete gain: *"bugs concentrate in one module"*, *"one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Explain a maintainability gain through the actual change rather than a generic label.

Keep prose proportionate to the decision. Use a short definition only when a reader needs it; do not require a missing glossary or rename the project's concepts to fit the report format.
