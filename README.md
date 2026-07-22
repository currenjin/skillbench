<div align="center">

# ⚡ SkillBench

**Do agent skills actually work? We measure.**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

English · [한국어](translations/README.ko.md) · [日本語](translations/README.ja.md) · [简体中文](translations/README.zh-CN.md) · [Español](translations/README.es.md) · [Português](translations/README.pt-BR.md)

</div>

---

Hundreds of skills, `CLAUDE.md` presets, and agent setups promise a better coding agent. Every Monday, SkillBench runs the most popular ones against the same **20 real-world coding tasks** — same model, same repos, same rubric — and publishes what actually moves the needle.

- **No sponsors. No affiliate links.** Numbers only.
- **Every raw run log is public.** Disagree with a result? Re-run it yourself.
- **If a skill regresses, we say so** — and file the issue upstream.

> 📬 **Get next Monday's results:** Watch → Custom → Releases

## 🏆 Leaderboard

> **The first benchmark run is in progress.** The first weekly leaderboard ships in **August 2026**.

Every week, for every registered skill, the leaderboard reports:

| Column | Meaning |
|---|---|
| **Solve rate** | % of tasks where the hidden test suite passes |
| **Δ week** | rank change vs last week |
| **Tokens per solve** | median token cost of a successful run |
| **vs baseline** | improvement over a stock agent with **no skill installed** |

The **baseline row is the whole point.** Most skill READMEs compare against nothing. We run a stock agent on every task, every week — a skill that can't beat "no skill" shouldn't be taking up your context window.

## 🔬 How we measure

- **20 fixed tasks** across 5 categories: bugfix (6), feature (5), refactor (4), test-writing (3), docs (2). Real issues from real OSS repos, each with a hidden test suite. Specs live in [`tasks/`](tasks/).
- **3 runs per skill per task**, same pinned model and version (currently `claude-opus-4-8`). We report medians and flag high-variance results.
- **Solve = hidden tests pass.** No LLM-as-judge for the headline number.
- **Everything is reproducible:** the harness in [`harness/`](harness/), task specs in [`tasks/`](tasks/), every raw run log in [`runs/`](runs/).

Full methodology: [`harness/README.md`](harness/README.md)

## 📥 Submit a skill

Add one entry to [`skills.yaml`](skills.yaml) via PR — it enters the next Monday bench:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # which task categories it claims to help
```

Measured skills get a live badge for their README:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 Repository layout

```
skillbench/
├── README.md            # this week's report (regenerated every Monday)
├── translations/        # auto-synced language editions
├── reports/             # weekly report archive + all-time rank history
├── harness/             # the runner — open, reproducible
├── tasks/               # 20 task specs (hidden tests kept in a private fixture repo)
├── runs/                # raw JSONL logs for every run, every week
└── skills.yaml          # the registry: one PR line = benched next Monday
```

## ❓ Why does this exist?

This repo's author previously maintained a curated bookmark list for developers. One day we measured its actual star velocity — and the numbers said the curation era was over. So we pivoted to the thing nobody was doing in the noisiest corner of GitHub: **measuring whether any of it actually works.** Measurement is the brand. It started at home.

## 📄 License

[MIT](LICENSE) — harness, task specs, and all published data.
