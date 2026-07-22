#!/usr/bin/env python3
"""Re-run the sanity gate on ASSEMBLED artifacts (no agent, no cost).

For every season task:
  1. fixture commit  + hidden suite  ->  must FAIL  (bug is live)
  2. fix commit      + hidden suite  ->  must PASS  (suite grades the real fix)

This catches transcription errors between mining and assembly. Fix commits
come from the private candidates.yaml, never from public task specs.

Usage: python3 verify_tasks.py [task-id ...]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from run import all_tasks, grade, load_task, make_env, prepare_fixture

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT.parent / "skillbench-fixtures"


def run_at(task, commit, workdir):
    spec = dict(task, commit=commit)
    fixture = prepare_fixture(spec, workdir)
    py = make_env(spec, workdir, fixture)
    return grade(spec, fixture, py)


def main():
    fix_commits = {c["id"]: c["fix_commit"]
                   for c in yaml.safe_load((FIXTURES / "candidates.yaml").read_text())}
    task_ids = sys.argv[1:] or all_tasks()
    failures = 0
    for task_id in task_ids:
        task = load_task(task_id)
        with tempfile.TemporaryDirectory(prefix="sb-verify-p-") as tmp:
            at_p = run_at(task, task["commit"], Path(tmp))
        with tempfile.TemporaryDirectory(prefix="sb-verify-f-") as tmp:
            at_f = run_at(task, fix_commits[task_id], Path(tmp))
        ok = (not at_p["solved"]) and at_f["solved"]
        if not ok:
            failures += 1
        print(f"{'OK  ' if ok else 'FAIL'} {task_id}: "
              f"fixture={'fails (good)' if not at_p['solved'] else 'PASSES (bad!)'} "
              f"fix={'passes (good)' if at_f['solved'] else 'FAILS (bad!)'}")
        if not ok:
            print("  --- fixture tail ---")
            print("  " + at_p["output_tail"][-500:].replace("\n", "\n  "))
            print("  --- fix tail ---")
            print("  " + at_f["output_tail"][-500:].replace("\n", "\n  "))
    print(f"\n{len(task_ids) - failures}/{len(task_ids)} tasks verified")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
