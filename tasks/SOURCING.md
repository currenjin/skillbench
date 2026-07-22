# How season tasks are sourced

SWE-bench-style, from real history — a task is only admitted when reality
already graded it once:

1. **Find a merged bug-fix PR that added tests** in a candidate repo.
2. **Fixture** = the parent commit of that fix (the bug is live, tests are green).
3. **Prompt** = the linked issue's symptom, rewritten to name behavior, never files.
4. **Hidden suite** = the tests the real fix added (adapted), kept in the private
   fixtures repo until the task retires.
5. **Sanity gate** (mechanical, must pass before admission):
   - hidden suite **fails** at the fixture commit
   - hidden suite **passes** at the fix commit
   - public suite passes at both
   - fixture installs + tests run in under 60s on a laptop, no network

## Candidate repo pool

Pure Python, light dependencies, fast test suites, active issue tracker:

| Repo | Domain | Why it benches well |
|---|---|---|
| tqdm/tqdm | progress bars | tiny API surface, behavioral bugs |
| pallets/click | CLI framework | rich edge cases, excellent tests |
| pallets/jinja2 | templating | parsing/precedence bugs |
| more-itertools/more-itertools | iteration utils | pure functions, crisp specs |
| dateutil/dateutil | dates | timezone/parsing bugs, hidden-test friendly |
| marshmallow-code/marshmallow | serialization | schema edge cases |
| jd/tenacity | retries | async/timing logic bugs |
| seperman/deepdiff | diffing | recursive edge cases |
| john-kurkowski/tldextract | URL parsing | clean symptom→fix mapping |
| py-pdf/pypdf | PDF | plenty of real-world bugfix PRs |

Selection target: 20 tasks — bugfix 6 · feature 5 · refactor 4 · test-writing 3 · docs 2,
no repo contributing more than 3 tasks.

## Disqualifiers

- Fix visible in the repo's git log at the fixture commit (agents read history) →
  fixture ships **without `.git`** (the harness already strips it), and the task is
  still rejected if the issue thread spells out the patch.
- Flaky/timing-sensitive tests, network access, compiled dependencies.
- Symptom can't be stated without pointing at the file.

## Task admission log

Every admitted task gets a `notes.md` recording: source PR/issue links, why it
discriminates, sanity-gate output. Published one season after the task retires.
