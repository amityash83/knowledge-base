---
title: Stay script-free rather than adopt Python tooling for the wiki loop
type: decision
domain: [ai-ml, devops]
status: stable
tags: [llm-wiki, tooling, agentic-ai]
sources: [raw-sources/archive/build-llm-wiki-with-obsidian.md]
created: 2026-08-11
updated: 2026-08-11
---

# Stay script-free rather than adopt Python tooling for the wiki loop

## Summary
This vault deliberately keeps `/ingest`, `/ask`, and `/lint` as pure prompt-driven operations performed by Claude Code directly on Markdown files — no Python scripts, no `wiki_tool.py`-style deterministic tooling, no custom Obsidian CLI skill pack. A comparison source ([[llm-wiki-pattern]]) describes a more heavily tooled implementation of the same underlying pattern; this page records why this vault didn't follow that path, at least for now.

## Details

### What the alternative looks like
The comparison source builds: a Python script performing ingest/index/catalog/lint operations deterministically; per-vault custom Obsidian-aware skills; an Obsidian CLI integration; per-entity-type templates; and a vault-access firewall. The stated rationale there is that scripts make agent behavior more repeatable and token-efficient at scale ("doesn't necessarily have to understand and figure out every single time what it needs to do").

### Why this vault stayed script-free
- **Matches the original pattern's own minimalism.** Karpathy's gist defines only three layers — raw sources, wiki, schema file — with no prescribed tooling; this vault's `CLAUDE.md` already commits to "no build, lint, or test tooling" as a stated property, not an oversight.
- **Scale doesn't demand it yet.** The tooled approach's main justification is consistency at "thousands of sources, tens of thousands of concepts." This vault is currently 16 wiki pages across ~27 archived sources — well below the point where a script's determinism would outperform Claude reasoning through the schema directly each time.
- **Fewer moving parts to maintain.** A script is one more thing that can drift from the schema in `CLAUDE.md` and need updating in lockstep. Keeping the schema as the single source of truth, read fresh by Claude on every operation, avoids that sync problem entirely.
- **Obsidian CLI / skill pack wasn't needed.** This vault's `/ingest`, `/ask`, `/lint` are conversational asks to Claude Code, not something requiring a dedicated Obsidian-aware skill layer — Obsidian here is purely the read-only viewer (graph view, wikilinks, Dataview), never something Claude needs to operate through a CLI.

### When to revisit
- If the wiki grows large enough that Claude's per-ingest reasoning (re-deriving "which pages does this touch" from scratch each time) becomes noticeably slow, inconsistent, or expensive — a deterministic index-lookup script would help exactly where the comparison source argues it does.
- If a second vault is ever added to the same Claude Code environment, at which point the "Obsidian firewall" pattern (vault allowlisting) becomes directly relevant rather than theoretical.

## Open questions
- No specific scale threshold has been set for "revisit the script-free decision" — it's a judgment call for whoever notices ingest getting unreliable, not a numeric trigger.

## Related
- [[llm-wiki-pattern]]
- [[llm-wiki-design-plan]]
