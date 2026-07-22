# The SkillBench harness

The harness answers one question, the same way, every week:

> Given the same model, the same 20 tasks, and the same rubric —
> does installing this skill change the outcome?

## Design

```
for each skill in skills.yaml (+ the baseline with NO skill):
    for each task in tasks/:
        for run in 1..3:
            1. clone the task's fixture repo at the pinned commit
            2. install the skill (or nothing, for baseline)
            3. run Claude Code headless with the task prompt
            4. apply the hidden test suite
            5. record: pass/fail, tokens in/out, wall time, transcript
→ write runs/<week>/<skill>/<task>-<run>.jsonl
→ aggregate medians → leaderboard in README.md + reports/<week>.md
```

## Fairness rules

1. **Pinned model, pinned Python.** One model + version per season, stated on the leaderboard (season 1: `claude-opus-4-8`, CPython 3.11). Mid-season model releases get a separate "regression check" run before adoption.
2. **Hidden tests.** Task fixtures are public; the grading test suites live in a private fixture repo so skills can't overfit. Suites are published one season after retirement.
3. **Medians of 3.** Single runs lie. We report the median and flag any skill whose runs disagree (variance note on the leaderboard).
4. **Baseline first.** The stock agent (no skill) runs every task, every week, before anything else. All "vs baseline" deltas are same-week, never historical.
5. **No LLM-as-judge for the headline.** Solve = tests pass. Judged dimensions (code style, diff size) may appear as secondary columns, clearly marked.

## Running it yourself

```bash
cd harness
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python run.py --skill obra/superpowers:tdd --task tasks/bugfix-01 --runs 1
```

Every number on the leaderboard links to its raw JSONL in `runs/`. If your re-run disagrees, open an issue titled `dispute: <skill> / <task>` — disputes get re-run publicly.

## Cost policy

SkillBench runs on **zero cash**: bench runs go through the maintainer's
Claude subscription (headless `claude` CLI), never a metered API key.
Consequences, embraced openly:

- Weekly benches run as a **trickle** (batches spread across off-hours),
  not one burst — the Monday report aggregates the week's runs.
- Scale comes from scope discipline, not spend: 6 skills × 20 tasks × 3 runs
  is sized to fit a subscription week.
- Disputes are re-run on the maintainer's quota, one at a time, publicly.

## Status

- [x] Harness design (this document)
- [x] `run.py` — runner implementation
- [x] `aggregate.py` — leaderboard generator
- [x] End-to-end smoke run (`tasks/smoke-01`, log in `runs/dev/`)
- [ ] Season task selection (20 tasks, pinned fixtures)
- [ ] First full bench: inaugural cohort, August 2026
