# About this pipeline

This folder holds the tooling that builds and packages the Leukerbad hackathon knowledge base. Nothing in here needs to be opened to use the knowledge base.

## How to read the knowledge base

| You have | Do this |
|---|---|
| The share link | Open it in any browser, phone included. Search covers every doc. |
| The zip / the folder | Open `index.html` in a browser. It works from disk; pictures and docs load locally. |
| Obsidian | "Open folder as vault" on this `DocsPipline` folder. Start at `00-START-HERE.md`; `Hackathon-Map.canvas` and `Companies.base` give a board and a table view. |
| Any Markdown editor | Every doc is plain Markdown with relative links. |

## What is generated and what is written by research

- **Research docs** (written by research agents, edit freely): everything under `Companies/` and the `T0x-0-Track-Overview.md`, `T0x-1-Solution-Patterns.md`, `T0x-3-Cross-Vendor-Solutions.md` files under `Challenges/`, plus `Event/Event-Intel.md`.
- **Generated pages** (rebuilt from the research docs, do not hand-edit): `00-START-HERE.md`, `01-Coverage-Audit.md`, `02-Developer-Cheatsheet.md`, `Companies.base`, `Hackathon-Map.canvas`, the `T0x-2`, `T0x-4`, `T0x-5` and `T0x-6` files under `Challenges/`, `index.html` and the `kb/` folder.

## Rebuild after editing docs

```bash
python3 DocsPipline/_pipeline/build_kb.py DocsPipline
```

Options: `--check` lists broken links and picture references; `--final` adds cross-links to second-pass docs; `--fix-images` removes dangling picture lines and shrinks oversized pictures.

Change a fit score by editing `fit:` in the frontmatter of a company's `…-T0x-1-Brief.md`; the matrix, shortlists, canvas and web viewer follow on the next rebuild.

## Files here

| File | Purpose |
|---|---|
| `build_kb.py` | Builds every generated page and the web viewer data |
| `viewer.fragment.html` | The web viewer (source of `index.html` and of the shared web page) |
| `vendor/` | Markdown renderer copies so `index.html` also works offline |
| `workflows/` | The research workflow scripts used with Claude Code (company first pass, track research, second pass) |

## How the research was run

Each company went through: profile → three docs per track → product catalogue with pictures, developer guide, roadmap → solutions-and-projects register and papers. A second pass per track (mapping everything onto the seven official directions) and a final fact-check audit have run for only some companies so far; `01-Coverage-Audit.md` shows exactly which docs exist.

Limits to know about: web search was capped during the build, so docs state where a check rested on official pages only; items marked ⚠️ could not be verified; fit scores are an assessment from public sources, not a statement about the hardware actually on site.
