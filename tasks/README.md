# Task suite

20 fixed tasks. Real issues from real OSS repos — not toy katas.

| Category | Count | What it probes |
|---|---|---|
| bugfix | 6 | root-causing, minimal diffs, not breaking neighbors |
| feature | 5 | reading existing architecture, matching house style |
| refactor | 4 | behavior preservation under structural change |
| test-writing | 3 | meaningful coverage, not assertion theater |
| docs | 2 | accuracy against the actual code |

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
