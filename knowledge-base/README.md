# Leukerbad Robotics Hackathon 2026 — Knowledge Base

Unofficial research on the 20 hardware and platform companies at the hackathon, organised by the four tracks: T01 Autonomous Urban Services · T02 Resilient & Safe City · T03 Sustainable City · T04 Elderly Care & Rehabilitation. Compiled from public sources on 14 Nov 2026; ⚠️ marks claims that could not be verified, and fit scores are our own assessment.

## Start here

- **[00-START-HERE.md](00-START-HERE.md)** — fit matrix (every company scored 0–5 per track) and links to everything.
- **[Event intel](Event/Event-Intel.md)** — rules, judging, schedule, insurance requirement.
- **`Challenges/<track>/`** — track overview with the 7 official directions, hardware shortlist, solution patterns, cross-vendor plays, research library, and every company's solutions, projects and plans for that track.
- **`Companies/<Company>/`** — profile, product catalogue with pictures, developer guide, roadmap, solutions register, papers, and one folder per track (Brief, Products & solutions, Playbook).

## Ways to read it

| Where | How |
|---|---|
| GitHub | Browse the Markdown here; links and pictures work. |
| Browser | Download or clone, then open `index.html`: searchable, works offline. |
| Obsidian | Open this folder as a vault; `Hackathon-Map.canvas` and `Companies.base` add a board and a table view. |

## Gaps

[01-Coverage-Audit.md](01-Coverage-Audit.md) lists exactly which docs exist. Still missing: solutions registers for D-Robotics, Dobot, Leadshine, ROKAE and XREAL; papers for Galbot, ROKAE and XREAL; Galaxea's product catalogue; Leadshine's developer guide and roadmap; the T01 cross-vendor page; the second-pass per-track registers and fact-checks for most companies.

## Editing

The Markdown is plain and safe to edit. After changing docs, rebuild the generated pages (hub, shortlists, viewer data) from this folder with `python3 _pipeline/build_kb.py .` — details in [_pipeline/README.md](_pipeline/README.md).
