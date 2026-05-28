# analyst-research · workflow overview

The actual step-by-step workflow lives in three mode-specific files. After the user picks a mode at trigger time (per `SKILL.md` Step 0), load the matching file as the working workflow document:

| Mode | Workflow file | Steps | Notes |
|---|---|---|---|
| `light` | `workflow_light.md` | 6 | Soft stops only. No charts. Pure markdown footnote citations. |
| `medium` | `workflow_medium.md` | 8 | One hard stop (sign-off after draft). 3-8 charts. Footnote citations. |
| `heavy` | `workflow_heavy.md` | 11 | Three hard stops (outline / draft / final). 20-35+ charts. BibTeX + APA. Optional multi-LLM. |

Each mode's workflow file is **self-contained** and includes:

- Scope & boundary section (when to use, when not to)
- Onboarding flow (mode-specific question set, e.g., light asks only "what's the hypothesis", heavy asks ~7 questions)
- Step skeleton with stop semantics (soft / hard) per step
- Writing discipline (style red lines, grep self-check table)
- Retrospective rules (how to promote project learnings back to the skill)

The three workflow files share the same **visual spec** (`report_style_spec.md`) for chart production — light mode skips it (no charts), medium and heavy both consume it.

## Cross-mode invariants

These rules apply to all three modes regardless of which workflow file you loaded:

1. **Hypothesis first**: every project starts with a single-sentence hypothesis lock. The hypothesis travels with the project file from day one — never re-derive it from the draft.
2. **Source provenance**: every number cited in the final deliverable must trace to a primary source. Cite-as-you-write, never cite-after-draft.
3. **Three-state labeling**: facts (per source), estimates (per market consensus), inferences (your derivation) get distinct wording. Never collapse the three.
4. **No fabricated numbers**: "not publicly available" or "to be verified" beats a plausible guess. Always.
5. **Reply language matches question language**; **report language defaults to English**. Chinese question → Chinese answer; English question → English answer. The deliverable draft defaults to English regardless of conversation language — at onboarding ask "report language: English (default) / Chinese / other?" and lock the answer in the project CLAUDE.md. This supersedes the older "draft follows hypothesis language" rule (see SKILL.md "Reply language").

## Upgrading a project mid-flight

If a `light` project turns out to need more depth, re-trigger the skill in `medium` mode — the hypothesis lock and early source work transfer because all three modes start the same way. Same path `medium → heavy`. Downgrading is generally not worth it — cut deliverables rather than re-run the workflow.

## File-loading directive for AI

When you (the AI) read this file as part of the analyst-research skill load sequence:

1. The user has already picked a mode (per SKILL.md Step 0). Confirm which.
2. Load the matching `workflow_<mode>.md` file as the authoritative procedure document.
3. Load `report_style_spec.md` only if mode is `medium` or `heavy`.
4. Proceed to the onboarding section inside the loaded `workflow_<mode>.md`.

Do not try to merge or compare the three workflow files at runtime — they are independently maintained and intentionally have different step counts, stop semantics, and deliverable shapes.
