#!/usr/bin/env python3
"""Sync translations/ from the root README — part of the weekly release.

Runs locally through the maintainer's `claude` CLI (subscription, zero cash);
never a metered API key, never CI. One call per language.

Usage:
  python3 translate.py            # all languages
  python3 translate.py ko ja     # specific languages
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LANGS = {
    "ko": "Korean",
    "ja": "Japanese",
    "zh-CN": "Simplified Chinese",
    "es": "Spanish (Latin American)",
    "pt-BR": "Brazilian Portuguese",
}

LINKS = " · ".join(
    f"[English](../README.md)" if code == "en" else f"[{label}](README.{code}.md)"
    for code, label in [("en", "English"), ("ko", "한국어"), ("ja", "日本語"),
                        ("zh-CN", "简体中文"), ("es", "Español"), ("pt-BR", "Português")])

PROMPT = """Translate the following GitHub README from English to {language}.

Rules:
- Keep ALL markdown structure, badges, code blocks, YAML snippets, file paths,
  CLI commands, and shields.io URLs exactly as-is. Translate prose only.
- Keep the project name "SkillBench" and column names (Solve rate, Δ week,
  Tokens per solve, vs baseline) in English; translate their descriptions.
- Relative links must point one directory up (../README.md, ../tasks/ etc.).
- Replace the language-switcher line with exactly:
  {links}
  but change the current language ({language}) from a link to plain text.
- Output ONLY the translated markdown, no commentary.

README:
---
{readme}"""


def main():
    readme = (ROOT / "README.md").read_text()
    targets = sys.argv[1:] or list(LANGS)
    for code in targets:
        prompt = PROMPT.format(language=LANGS[code], links=LINKS, readme=readme)
        out = subprocess.run(["claude", "-p", prompt, "--model", "claude-opus-4-8"],
                             capture_output=True, text=True, timeout=600)
        text = out.stdout.strip()
        if out.returncode != 0 or not text.startswith("<div"):
            print(f"FAIL {code}: {out.stderr[:200] or 'unexpected output'}")
            continue
        (ROOT / "translations" / f"README.{code}.md").write_text(text + "\n")
        print(f"synced translations/README.{code}.md")


if __name__ == "__main__":
    main()
