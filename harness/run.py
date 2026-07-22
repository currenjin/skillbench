#!/usr/bin/env python3
"""SkillBench harness runner.

Runs one (skill, task) pair N times through Claude Code headless,
grades each run with the task's test suite, and appends one JSONL
record per run to runs/<week>/<skill>/<task>-r<n>.jsonl.

Usage:
  python3 run.py --baseline --task smoke-01 --runs 1 --week dev
  python3 run.py --skill obra/superpowers:tdd --task bugfix-01 --runs 3 --week 2026-W32
  python3 run.py --all --week 2026-W32          # baseline + every skill x every task

Agent permissions: runs use `--permission-mode acceptEdits` by default.
Tasks that need broader autonomy should grant it per-fixture via a
`.claude/settings.json` allow-list committed to the fixture, so every
skill gets exactly the same sandbox.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "harness" / ".cache"
DEFAULT_MODEL = "claude-opus-4-8"
DEFAULT_RUNS = 3
BASELINE = {"repo": None, "skill": None, "kind": "baseline"}


def slug(entry):
    if entry["kind"] == "baseline":
        return "baseline"
    name = entry["repo"].replace("/", "__")
    return f"{name}__{entry['skill']}" if entry.get("skill") else name


def load_skills():
    with open(ROOT / "skills.yaml") as f:
        return yaml.safe_load(f)


def find_skill_entry(spec):
    """Resolve 'owner/repo[:skill]' against skills.yaml."""
    repo, _, skill = spec.partition(":")
    for entry in load_skills():
        if entry["repo"] == repo and (not skill or entry.get("skill") == skill):
            return entry
    sys.exit(f"error: {spec!r} not found in skills.yaml")


def load_task(task_id):
    for d in sorted((ROOT / "tasks").iterdir()):
        spec = d / "task.yaml"
        if d.is_dir() and spec.exists():
            task = yaml.safe_load(spec.read_text())
            if task["id"] == task_id:
                task["_dir"] = d
                return task
    sys.exit(f"error: task {task_id!r} not found under tasks/")


def all_tasks():
    ids = []
    for d in sorted((ROOT / "tasks").iterdir()):
        spec = d / "task.yaml"
        if d.is_dir() and spec.exists():
            task_id = yaml.safe_load(spec.read_text())["id"]
            if not task_id.startswith("smoke"):
                ids.append(task_id)
    return ids


def prepare_fixture(task, workdir):
    """Materialize the task's fixture repo into workdir/fixture."""
    dest = workdir / "fixture"
    if task["fixture"] == "local":
        shutil.copytree(task["_dir"] / task["fixture_path"], dest)
    else:
        subprocess.run(["git", "clone", "--quiet",
                        f"https://github.com/{task['fixture']}", str(dest)], check=True)
        subprocess.run(["git", "checkout", "--quiet", task["commit"]], cwd=dest, check=True)
        shutil.rmtree(dest / ".git")
    return dest


def clone_cached(repo):
    dest = CACHE / repo.replace("/", "__")
    if not dest.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        f"https://github.com/{repo}", str(dest)], check=True)
    return dest


def install_skill(entry, fixture):
    """Install the skill/preset into the fixture the way a user would."""
    if entry["kind"] == "baseline":
        return
    src = clone_cached(entry["repo"])
    if entry["kind"] == "claude-md":
        shutil.copy(src / "CLAUDE.md", fixture / "CLAUDE.md")
        return
    name = entry.get("skill")
    # locate the skill dir — layouts verified across the ecosystem:
    #   skills/<name>/          (superpowers, anthropics/skills, caveman)
    #   skills/<bucket>/<name>/ (mattpocock/skills)
    #   .claude/skills/<name>/  (ui-ux-pro-max)
    #   <name>/ or repo root with SKILL.md
    patterns = [f"skills/{name}/SKILL.md", f"skills/*/{name}/SKILL.md",
                f".claude/skills/{name}/SKILL.md", f"{name}/SKILL.md", "SKILL.md"] \
        if name else ["SKILL.md"]
    skill_dir = next((m.parent for pat in patterns for m in sorted(src.glob(pat))), None)
    if skill_dir is None:
        raise RuntimeError(f"cannot locate SKILL.md for {entry['repo']}:{name}")
    dest = fixture / ".claude" / "skills" / (name or Path(entry["repo"]).name)
    shutil.copytree(skill_dir, dest)


def make_env(task, workdir, fixture):
    """Per-run venv: pytest + (optionally) the fixture installed editable."""
    venv_dir = workdir / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    py = venv_dir / "bin" / "python"
    subprocess.run([py, "-m", "pip", "install", "-q", "pytest",
                    *task.get("extra_deps", [])], check=True)
    if task.get("install") == "editable":
        # fixtures ship without .git, so scm-based version plugins
        # (setuptools-scm, hatch-vcs) need a pretend version
        env = {**os.environ, "SETUPTOOLS_SCM_PRETEND_VERSION": "0.0.0"}
        subprocess.run([py, "-m", "pip", "install", "-q", "-e", str(fixture)],
                       check=True, timeout=120, env=env)
    return py


def run_agent(task, fixture, model, permission_mode):
    # web tools are blocked: season fixtures come from real OSS history, and the
    # published fix must not be one WebSearch away
    cmd = ["claude", "-p", task["prompt"], "--output-format", "json",
           "--model", model, "--permission-mode", permission_mode,
           "--disallowedTools", "WebFetch,WebSearch"]
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=fixture, capture_output=True, text=True,
                              timeout=task.get("timeout_minutes", 30) * 60)
        out = json.loads(proc.stdout) if proc.stdout.strip() else {}
        timed_out = False
    except subprocess.TimeoutExpired:
        out, timed_out = {}, True
    usage = out.get("usage", {})
    return {
        "timed_out": timed_out,
        "is_error": out.get("is_error", timed_out),
        "cost_usd": out.get("total_cost_usd"),
        "tokens_in": usage.get("input_tokens"),
        "tokens_out": usage.get("output_tokens"),
        "cache_read": usage.get("cache_read_input_tokens"),
        "num_turns": out.get("num_turns"),
        "duration_s": round(time.monotonic() - start, 1),
        "session_id": out.get("session_id"),
    }


FIXTURES_REPO = "currenjin/skillbench-fixtures"


def grade(task, fixture, py=None):
    g = task["grading"]
    if g["type"] == "local":
        src = task["_dir"] / g["path"]
    elif g["type"] == "private":
        # hidden suites live in the private fixtures repo (maintainer creds);
        # refresh the cache so weekly suite updates are picked up
        repo_dir = clone_cached(g.get("repo", FIXTURES_REPO))
        subprocess.run(["git", "pull", "--quiet"], cwd=repo_dir, check=False)
        src = repo_dir / g["path"]
    else:
        raise ValueError(f"unknown grading type: {g['type']!r}")
    shutil.copytree(src, fixture / "grading_tests")
    cmd = g["command"].split()
    if cmd[0] in ("python", "python3"):
        # grade with the per-run venv (fixture installed), else the harness venv
        cmd[0] = str(py) if py else sys.executable
    if "pytest" in cmd:
        # neutral config: never inherit the fixture's addopts/plugins
        # (e.g. tqdm requires --asyncio-mode, pypdf requires --disable-socket)
        ini = fixture / "grading_tests" / "_neutral.ini"
        ini.write_text("[pytest]\n")
        cmd += ["-c", str(ini)]
    proc = subprocess.run(cmd, cwd=fixture, capture_output=True,
                          text=True, timeout=600)
    return {"solved": proc.returncode == 0,
            "returncode": proc.returncode,
            "output_tail": (proc.stdout + proc.stderr)[-2000:]}


def bench(entry, task, runs, week, model, permission_mode):
    out_dir = ROOT / "runs" / week / slug(entry)
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in range(1, runs + 1):
        with tempfile.TemporaryDirectory(prefix="skillbench-") as tmp:
            workdir = Path(tmp)
            fixture = prepare_fixture(task, workdir)
            py = make_env(task, workdir, fixture)
            install_skill(entry, fixture)
            agent = run_agent(task, fixture, model, permission_mode)
            result = grade(task, fixture, py) if not agent["timed_out"] else \
                {"solved": False, "returncode": None, "output_tail": "agent timed out"}
        record = {
            "week": week, "model": model,
            "skill": slug(entry), "task": task["id"], "run": n,
            "solved": result["solved"], "agent": agent, "grade": result,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        path = out_dir / f"{task['id']}-r{n}.jsonl"
        with open(path, "a") as f:
            f.write(json.dumps(record) + "\n")
        print(f"[{slug(entry)} / {task['id']} / run {n}] "
              f"{'SOLVED' if result['solved'] else 'failed'} "
              f"(tokens {agent['tokens_in']}/{agent['tokens_out']}, "
              f"{agent['duration_s']}s) -> {path.relative_to(ROOT)}")


def main():
    p = argparse.ArgumentParser()
    who = p.add_mutually_exclusive_group(required=True)
    who.add_argument("--skill", help="owner/repo[:skill] from skills.yaml")
    who.add_argument("--baseline", action="store_true")
    who.add_argument("--all", action="store_true", help="baseline + every skill")
    p.add_argument("--task", help="task id (default: all season tasks)")
    p.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    p.add_argument("--week", required=True, help="e.g. 2026-W32, or 'dev'")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--permission-mode", default="acceptEdits",
                   help="claude --permission-mode value (default: acceptEdits)")
    args = p.parse_args()

    entries = ([BASELINE] + load_skills()) if args.all else \
              [BASELINE] if args.baseline else [find_skill_entry(args.skill)]
    task_ids = [args.task] if args.task else all_tasks()
    if not task_ids:
        sys.exit("error: no season tasks yet — pass --task smoke-01 to validate the pipeline")

    for entry in entries:
        for task_id in task_ids:
            bench(entry, load_task(task_id), args.runs, args.week, args.model,
                  args.permission_mode)


if __name__ == "__main__":
    main()
