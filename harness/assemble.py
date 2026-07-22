#!/usr/bin/env python3
"""Assemble season tasks from the private candidates file.

Reads  ../skillbench-fixtures/candidates.yaml  (the single source of truth)
and generates:
  tasks/<id>/task.yaml                          (public — this repo)
  ../skillbench-fixtures/tasks/<id>/test_hidden.py   (private)
  ../skillbench-fixtures/tasks/<id>/notes.md         (private until retirement)

Idempotent: re-running regenerates everything from candidates.yaml.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT.parent / "skillbench-fixtures"

PROMPT_SUFFIX = (
    "\n\nFind the root cause and fix it. "
    "Do not modify any existing tests."
)


def main():
    candidates = yaml.safe_load((FIXTURES / "candidates.yaml").read_text())
    for c in candidates:
        task_dir = ROOT / "tasks" / c["id"]
        task_dir.mkdir(parents=True, exist_ok=True)
        task = {
            "id": c["id"],
            "category": c["category"],
            "fixture": c["repo"],
            "commit": c["fixture_commit"],
            "prompt": c["symptom"].strip() + PROMPT_SUFFIX,
            "timeout_minutes": 20,
            "install": "editable",
            "grading": {
                "type": "private",
                "path": f"tasks/{c['id']}",
                "command": "python3 -m pytest grading_tests -q",
            },
        }
        if c.get("extra_deps"):
            task["extra_deps"] = c["extra_deps"]
        (task_dir / "task.yaml").write_text(
            yaml.safe_dump(task, sort_keys=False, allow_unicode=True, width=88))

        hidden_dir = FIXTURES / "tasks" / c["id"]
        hidden_dir.mkdir(parents=True, exist_ok=True)
        (hidden_dir / "test_hidden.py").write_text(c["extracted_tests"])
        (hidden_dir / "notes.md").write_text(
            f"# {c['id']} — {c['repo']}\n\n"
            f"- source PR: {c['pr_url']}\n"
            f"- issue: {c.get('issue_url') or '—'}\n"
            f"- fix commit: `{c['fix_commit']}`\n"
            f"- fixture commit: `{c['fixture_commit']}`\n\n"
            f"## Sanity gate (mining agent)\n\n```\n{c['gate_output'].strip()}\n```\n\n"
            f"## Caveats\n\n{(c.get('caveats') or 'none').strip()}\n")
        print(f"assembled {c['id']:10s} <- {c['repo']} #{c['pr']}")


if __name__ == "__main__":
    main()
