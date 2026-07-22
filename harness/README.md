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

1. **Pinned model.** One model + version per season, stated on the leaderboard. Mid-season model releases get a separate "regression check" run before adoption.
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

## Status

- [x] Harness design (this document)
- [ ] `run.py` — runner implementation (in progress)
- [ ] Task fixture repos pinned
- [ ] First full bench: inaugural cohort, August 2026
