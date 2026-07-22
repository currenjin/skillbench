# Task suite

Real issues from real OSS repos — not toy katas. Every task is mined from a
merged fix (see [SOURCING.md](SOURCING.md)) and re-verified after assembly:
hidden suite fails at the fixture commit, passes at the real fix.

**Season 1 opens with 19 bugfix tasks** across 10 repos (tqdm, click, jinja,
marshmallow, tenacity, tldextract, deepdiff, pypdf, more-itertools, dateutil;
≤2 per repo). Feature / refactor / test-writing / docs categories are being
sourced and will grow the suite — skills are only measured on categories they
claim, so the leaderboard stays fair as the suite expands.

| Category | Now | Target | What it probes |
|---|---|---|---|
| bugfix | 19 | ~20 | root-causing, minimal diffs, not breaking neighbors |
| feature | 0 | 5 | reading existing architecture, matching house style |
| refactor | 0 | 4 | behavior preservation under structural change |
| test-writing | 0 | 3 | meaningful coverage, not assertion theater |
| docs | 0 | 2 | accuracy against the actual code |

Two tasks (`bugfix-18`, `bugfix-19`) come from pre-2022 fixes with high
training-data contamination risk; they are flagged and reported separately
on the leaderboard.

## Spec format

Each task is a directory:

```
tasks/bugfix-01/
├── task.yaml      # fixture repo + pinned commit, prompt, category, timeout
└── notes.md       # why this task, what it discriminates (published after season)
```

```yaml
# task.yaml
id: bugfix-01
category: bugfix
fixture: skillbench-fixtures/<repo>        # public fixture, pinned commit
commit: <sha>
prompt: |
  Users report that <observable symptom>. Find the cause and fix it.
  Do not modify the test directory.
timeout_minutes: 30
grading: hidden        # test suite lives in the private fixture repo
```

## Rules

- Fixtures are **public**, grading suites are **hidden** (published one season after retirement) — so skills can't overfit.
- Prompts state the *symptom*, never the file to change.
- A task that every skill solves — or none does — gets rotated out; it discriminates nothing.

## Status

Task selection for the inaugural season is in progress. Candidate criteria and the selection log will be published in `notes.md` files.
