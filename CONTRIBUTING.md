# Contributing

Three ways in, in order of impact:

## 1. Submit a skill (one-line PR)

Add an entry to [`skills.yaml`](skills.yaml). Merged entries are benched in the next Monday run. See the format rules at the top of that file.

## 2. Dispute a number

Every leaderboard figure links to raw JSONL logs in `runs/`. If your re-run disagrees, open an issue titled `dispute: <skill> / <task>`. Disputes are re-run publicly and the resolution is documented in the weekly report.

## 3. Propose a task

Good tasks are real, discriminating, and cheat-resistant. Open an issue with:
- the OSS repo + commit and the observable symptom (for bugfix) or requirement (for feature)
- why current skills would *differ* on it — a task everyone solves discriminates nothing
- a sketch of how a hidden test suite would grade it

## What we don't take

- Sponsored placements, "featured" slots, affiliate anything. The answer is no.
- Benchmark results without public raw logs.

## Translations

Language editions in `translations/` are generated automatically on each release — please don't PR manual fixes there; open an issue instead if a translation is wrong.
