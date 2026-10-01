---
name: improve-codebase-architecture
description: When the user explicitly requests architecture maintenance, inspect real code for useful module-deepening opportunities, report a small set of grounded candidates, and discuss the chosen change before implementation.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- If available, use [reviewing-code-modularity-skill](../reviewing-code-modularity-skill/SKILL.md) and its references for module ownership, public surfaces, seams, and dependency direction. Use the project's own vocabulary when it is clearer.
- Read an existing `GLOSSARY.md` or relevant ADRs when they exist; do not create them just to run this Skill.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Walk the codebase within the chosen scope. Delegate an independent scan only when the task and available agent setup justify it; otherwise explore directly. Don't follow rigid heuristics; note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present grounded candidates

Use a concise Markdown report by default. Add a small before/after diagram only when it clarifies ownership or dependency changes. If the user explicitly wants a visual report, use [HTML-REPORT.md](HTML-REPORT.md) and store the artifact in the task workspace within the current user's actual home directory, resolved from the runtime environment.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After**: a compact sketch when the change is difficult to picture
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

Use existing project domain language. If `GLOSSARY.md` defines "Order," use that term in the report.

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

Do not design new interfaces before a candidate is chosen, unless the user has already requested implementation and the interface decision is necessary for it.

### 3. Discuss and act

When the user selects a candidate, establish constraints, ownership, the smallest useful change, and the tests that should keep passing. Use [grilling](../grilling/SKILL.md) only if the user explicitly requests that intensive interview. If the user already authorized implementation, proceed within that scope; do not require another approval solely because this Skill suggested a candidate. Update `GLOSSARY.md` or an ADR only when requested or needed by the actual code change.
