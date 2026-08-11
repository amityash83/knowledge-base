---
title: Stay script-free rather than adopt Python tooling for the wiki loop
type: decision
domain: [ai-ml, devops]
status: stable
tags: [llm-wiki, tooling, agentic-ai]
sources: [raw-sources/archive/build-llm-wiki-with-obsidian.md, "https://github.com/wanderloots-tutorials/vibe-coding/blob/main/wanderloots-llm-wiki-core-setup-v1.0.0.md"]
created: 2026-08-11
updated: 2026-08-11
---

# Stay script-free rather than adopt Python tooling for the wiki loop

## Summary
This vault keeps `/ingest`, `/ask`, and `/lint` as prompt-driven operations performed by Claude Code — no custom Obsidian CLI skill pack, no `wiki_tool.py`-style catalog/build system. It draws the line at judgment vs. bookkeeping: one small script, `scripts/wiki_lint.py`, was added for mechanical, read-only validation (frontmatter correctness, dangling links) since that work has no judgment component and was previously costing tokens for something formulaic. Deciding what a source means, which pages it touches, and how a page reads stays entirely a Claude Code operation. A comparison source ([[llm-wiki-pattern]]) describes a more heavily tooled implementation of the same underlying pattern; this page records where and why this vault drew a different, narrower line.

## Details

### What the alternative looks like
The comparison source builds: a Python script performing ingest/index/catalog/lint operations deterministically; per-vault custom Obsidian-aware skills; an Obsidian CLI integration; per-entity-type templates; and a vault-access firewall. The stated rationale there is that scripts make agent behavior more repeatable and token-efficient at scale ("doesn't necessarily have to understand and figure out every single time what it needs to do").

### Why this vault stayed script-free
- **Matches the original pattern's own minimalism.** Karpathy's gist defines only three layers — raw sources, wiki, schema file — with no prescribed tooling; this vault's `CLAUDE.md` already commits to "no build, lint, or test tooling" as a stated property, not an oversight.
- **Scale doesn't demand it yet.** The tooled approach's main justification is consistency at "thousands of sources, tens of thousands of concepts." This vault is currently 16 wiki pages across ~27 archived sources — well below the point where a script's determinism would outperform Claude reasoning through the schema directly each time.
- **Fewer moving parts to maintain.** A script is one more thing that can drift from the schema in `CLAUDE.md` and need updating in lockstep. Keeping the schema as the single source of truth, read fresh by Claude on every operation, avoids that sync problem entirely.
- **Obsidian CLI / skill pack wasn't needed.** This vault's `/ingest`, `/ask`, `/lint` are conversational asks to Claude Code, not something requiring a dedicated Obsidian-aware skill layer — Obsidian here is purely the read-only viewer (graph view, wikilinks, Dataview), never something Claude needs to operate through a CLI.

### Where the line actually got drawn (2026-08-11 update)
Reading the comparison source's more concrete setup guide (a public build spec, not just the video) made the split sharper: its `wiki_tool.py` commands split cleanly into mechanical checks (`doctor`, `lint`, `source-lint`) versus a catalog/search layer (`build`, `search-catalog`) meant to avoid re-scanning the whole wiki at "thousands of sources" scale. Only the first category applied here:
- **Adopted:** `scripts/wiki_lint.py` — validates frontmatter (`type`/`domain`/`status` against the schema, required fields present, dates well-formed), checks `sources` paths resolve on disk, and checks `[[wikilinks]]` resolve to a real page. Read-only, stdlib-only, no external dependencies. Run after `/ingest`, before a semantic `/lint` pass.
- **Not adopted:** a `catalog.jsonl`/search-index layer. At 20 wiki pages, `wiki/index.md` (already read on every ingest) *is* the catalog — there's no lookup-speed problem yet for a build step to solve.

This linter caught a real inconsistency on its first real run: three project pages used `status: active`, which wasn't a valid value under the schema documented in `CLAUDE.md` at the time (`stable | evolving | stub`). Rather than force those pages to fit an ill-suited value, the schema itself was extended — projects now use their own lifecycle (`active | paused | done`) distinct from content-maturity status. Recorded here because it's exactly the kind of small, real bug the "no script" approach could have left unnoticed indefinitely.

### When to revisit further
- If the wiki grows large enough that Claude's per-ingest reasoning (re-deriving "which pages does this touch" from scratch each time) becomes noticeably slow, inconsistent, or expensive — a `build`/`search-catalog`-style script would help exactly where the comparison source argues it does.
- If a second vault is ever added to the same Claude Code environment, at which point the "Obsidian firewall" pattern (vault allowlisting) becomes directly relevant rather than theoretical.

## Open questions
- No specific scale threshold has been set for "add a catalog/search script" — it's a judgment call for whoever notices ingest getting unreliable, not a numeric trigger.

## Related
- [[llm-wiki-pattern]]
- [[llm-wiki-design-plan]]
