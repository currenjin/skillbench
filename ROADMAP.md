# SkillBench — 작업 로드맵 (내부용)

> 이어서 진행할 때 이 파일부터 읽으세요. 완료된 것은 체크, 남은 것은 순서대로.
> 마지막 갱신: 2026-07-22

## 배경 한 줄

site-for-developers(한국어 북마크, 1,173★, 정체) → **SkillBench**로 피봇.
"AI 코딩 에이전트 스킬이 실제로 효과 있는지 매주 실측하는 벤치마크 리더보드."
목표 5k★. 영어 우선 + 다국어 배포. **운영비 0원** (구독 CLI만, metered API 금지).

## 인프라 상태 (완료)

- [x] `currenjin/skillbench` 스캐폴드 (README, skills.yaml, CONTRIBUTING, LICENSE)
- [x] `currenjin/skillbench-fixtures` (프라이빗) — 히든 채점 스위트 + candidates.yaml
- [x] 하네스: `run.py`(실행·채점·JSONL), `aggregate.py`(리더보드), `assemble.py`(태스크 생성), `verify_tasks.py`(양방향 게이트), `translate.py`(언어판 동기화)
- [x] 시즌 1 태스크 19개(bugfix) — 10개 OSS 레포에서 마이닝, 전원 게이트 검증
- [x] 다국어 5종(ko/ja/zh-CN/es/pt-BR) 첫 판 커밋
- [x] `--resume` 플래그 (중단 지점부터 재개)

## 벤치 실행 상태 (2026-W32, n=1)

파일럿 및 배치 결과 — `runs/2026-W32/`, `runs/pilot/`:

- [x] baseline × 19 (pilot 폴더, 16/19 solve) + W32에 bugfix-18 재실행분
- [x] superpowers:test-driven-development × 19 (17/19)
- [x] superpowers:systematic-debugging × 19
- [x] caveman × 19 (16/19, 실패 04·06·12)
- [x] karpathy CLAUDE.md × 19
- [ ] **mattpocock:triage × 19** ← 다음 실행할 것. `--resume`으로 시작:
      ```
      cd ~/Documents/personal/repositories/skillbench
      ./.venv/bin/python -u harness/run.py --skill mattpocock/skills:triage \
        --runs 1 --week 2026-W32 --resume 2>&1 | grep -vE "notice|pip install"
      ```
      예상: ~19런, ~$25 명목(회사 쿼터), ~1~1.5h. bugfix-04는 20분 타임아웃 정상.

## 남은 작업 — 순서대로

1. **triage 배치 실행** (위 명령). 완료 후 `git add runs && commit && push`.

2. **baseline을 W32로 통합.** baseline 전체는 `runs/pilot/baseline/`에 19개 있고
   W32엔 bugfix-18만 있음. aggregate가 W32만 보므로, pilot의 baseline 18개를
   `runs/2026-W32/baseline/`로 복사(bugfix-18은 W32 재실행분 유지):
   ```
   for f in runs/pilot/baseline/*.jsonl; do
     t=$(basename $f); [ -f runs/2026-W32/baseline/$t ] || cp $f runs/2026-W32/baseline/
   done
   ```
   ※ 엄밀히는 baseline도 W32에서 새로 돌리는 게 정석이나, n=1 첫 리더보드에선
     pilot 재활용 허용. 정식 주간부터는 baseline도 매주 새로 실행.

3. **첫 리더보드 생성 + README 갱신.**
   ```
   ./.venv/bin/python harness/aggregate.py --week 2026-W32
   ```
   출력 마크다운을 README.md의 `## 🏆 Leaderboard` 섹션에 삽입,
   "first bench in progress" 배지 → 실제 수치로 교체.
   ⚠️ n=1이므로 리더보드에 "n=1, medians from W33" 명시할 것.
   ⚠️ solve rate가 baseline과 큰 차이 없을 가능성 → 정렬을 **tokens-per-solve
      (효율)** 기준으로 두고, 헤드라인은 "대부분의 스킬은 순정보다 더 풀게
      해주지 못한다; 차이는 효율에서 난다"로.

4. **reports/2026-W32.md 작성** — 주간 상세 분석: 스킬별 표, 회귀(어떤 스킬이
   어떤 태스크를 baseline 대비 못 풀었나), 이번 주 스토리, bugfix-18/19
   오염 플래그 주석.

5. **언어판 동기화** — `./.venv/bin/python harness/translate.py` (README 갱신 후).

6. **첫 릴리스** — `git tag 2026-W32 && git push --tags`, GitHub Release 작성
   (Watch=구독 유도). 태그가 곧 주간 발행 이벤트.

7. **site-for-developers 마무리** — README 최상단에 "→ SkillBench로 이어집니다"
   배너 커밋 후 `gh repo archive`(개인 계정 토큰 필요:
   `GH_TOKEN=$(gh auth token -u currenjin) gh repo archive currenjin/site-for-developers`).

8. **커뮤니티 공개** — Show HN, r/ClaudeAI, X (영); GeekNews (한); Zenn/Qiita (일);
   掘金/V2EX (중); dev.to (남미). 언어판별로 각각.

## 그다음 (정식 주간 체제)

- [ ] 매주 월요일: 6스킬 × 19태스크 × **3런**(중앙값) — ⚠️ ~$450 명목/주.
      회사 쿼터로는 과함 → **개인 Claude 계정 전환** 또는 런 수 조정 먼저 논의.
- [ ] 카테고리 확장: feature(5)/refactor(4)/test-writing(3)/docs(2) 태스크 소싱
      (마이닝 에이전트 재활용). 대기 스킬(ui-ux-pro-max, anthropics/frontend-design,
      spec-kit) 매칭 카테고리 생기면 등재.
- [ ] skills.yaml 외부 PR 접수 시작 + 등재 배지 발급.
- [ ] 반기 결산 "State of Agent Skills 2026-H2" (12월).

## 알아둘 것 (함정)

- 벤치 중단 = 대부분 구독 쿼터 순간 고갈. `--resume`으로 그 지점부터 재개(유실 없음).
- Python 3.11 고정 (venv `.venv`). 3.14에선 dateutil 등 죽음.
- 회사(Wemeetmobility Team) 쿼터로 실행 중 — 개인 프로젝트 대량 실행 시 계정 재확인.
- 커밋에 co-author 라인 넣지 않기.
