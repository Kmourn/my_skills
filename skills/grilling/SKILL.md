---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Use this skill when the user explicitly requests the interview or a stress test of their thinking. Interview within the named plan, decision, or idea; do not expand a narrow question into a full project redesign. Map the material decisions as a **design tree**: each decision branches into the decisions that depend on it. Carry forward decisions already settled by the user.

Work the tree in **rounds**. The **frontier** contains decisions whose prerequisites are settled: questions you can ask now without guessing at answers you have not heard. Ask a manageable set of material questions, prioritizing those that change the next step. Number each question and give a recommended answer with its reason. Wait for the user's answers before asking dependent questions; omit branches that have no practical effect on the scoped decision.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job. Inspect available files and tools yourself; delegate only when independent investigation adds value and delegation is available and authorized. Do not ask the user for facts you can obtain. A running investigation is an unsettled prerequisite: defer its dependent questions and continue with independent ones. Ask the user for missing context that cannot be obtained and would change the decision. The material _decisions_ are the user's: put them to the user and wait.

Conclude when the scoped decisions are settled or the user ends the interview. Present the decisions, consequential assumptions, and any unresolved choices. The interview itself does not authorize implementation; obtain a missing implementation decision or authorization when needed, and preserve any implementation authority the user has already given. Do not ask again merely to reconfirm settled choices.
