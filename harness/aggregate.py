#!/usr/bin/env python3
"""Aggregate a week's raw runs into the leaderboard table.

Usage:
  python3 aggregate.py --week 2026-W32 [--prev 2026-W31]

Prints the leaderboard as GitHub markdown. A task counts as solved for a
skill when the majority of its runs pass. Tokens-per-solve is the median
of (in+out) over solved runs only.
"""
import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_week(week):
    """-> {skill: {task: [records]}}"""
    data = defaultdict(lambda: defaultdict(list))
    week_dir = ROOT / "runs" / week
    if not week_dir.exists():
        raise SystemExit(f"error: no runs for week {week!r}")
    for path in week_dir.glob("*/*.jsonl"):
        for line in path.read_text().splitlines():
            r = json.loads(line)
            data[r["skill"]][r["task"]].append(r)
    return data


def summarize(by_task):
    tasks = solved = 0
    token_costs = []
    for records in by_task.values():
        tasks += 1
        wins = [r for r in records if r["solved"]]
        if len(wins) * 2 > len(records):
            solved += 1
            # total tokens the model actually processed, cache reads included —
            # fresh-input-only numbers make cached runs look absurdly cheap
            costs = [r["agent"]["tokens_in"] + r["agent"]["tokens_out"]
                     + (r["agent"]["cache_read"] or 0)
                     for r in wins
                     if r["agent"]["tokens_in"] is not None]
            if costs:
                token_costs.append(statistics.median(costs))
    variance = sum(1 for records in by_task.values()
                   if len({r["solved"] for r in records}) > 1)
    return {
        "tasks": tasks,
        "solve_rate": solved / tasks if tasks else 0.0,
        "tokens_per_solve": statistics.median(token_costs) if token_costs else None,
        "high_variance_tasks": variance,
    }


def fmt_tokens(n):
    return f"{round(n / 1000)}k" if n else "—"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--week", required=True)
    p.add_argument("--prev", help="previous week, for Δ column")
    args = p.parse_args()

    stats = {skill: summarize(by_task) for skill, by_task in load_week(args.week).items()}
    base = stats.pop("baseline", None)

    prev_rank = {}
    if args.prev:
        prev = {s: summarize(t) for s, t in load_week(args.prev).items() if s != "baseline"}
        ordered = sorted(prev, key=lambda s: -prev[s]["solve_rate"])
        prev_rank = {s: i + 1 for i, s in enumerate(ordered)}

    print(f"| # | Skill / Setup | Solve rate | Δ week | Tokens per solve | vs baseline |")
    print(f"|---|---|---|---|---|---|")
    if base:
        print(f"| — | *baseline · no skill* | *{base['solve_rate']:.0%}* | — "
              f"| *{fmt_tokens(base['tokens_per_solve'])}* | — |")
    ranked = sorted(stats, key=lambda s: -stats[s]["solve_rate"])
    for i, skill in enumerate(ranked, 1):
        s = stats[skill]
        if skill in prev_rank:
            d = prev_rank[skill] - i
            delta = f"▲{d}" if d > 0 else f"▼{-d}" if d < 0 else "—"
        else:
            delta = "new"
        vs = f"{(s['solve_rate'] - base['solve_rate']) * 100:+.0f}pt" if base else "—"
        note = f" ⚠{s['high_variance_tasks']}" if s["high_variance_tasks"] else ""
        print(f"| {i} | {skill.replace('__', '/')} | {s['solve_rate']:.0%}{note} "
              f"| {delta} | {fmt_tokens(s['tokens_per_solve'])} | {vs} |")


if __name__ == "__main__":
    main()
