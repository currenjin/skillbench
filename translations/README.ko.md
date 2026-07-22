<div align="center">

# ⚡ SkillBench

**에이전트 스킬, 진짜 효과 있을까? 우리는 측정합니다.**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

[English](../README.md) · 한국어 · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md)

</div>

---

수백 개의 스킬, `CLAUDE.md` 프리셋, 에이전트 셋업이 "더 나은 코딩 에이전트"를 약속합니다. SkillBench는 매주 월요일, 가장 인기 있는 것들을 동일한 **실전 코딩 태스크 20개**에 돌립니다 — 같은 모델, 같은 저장소, 같은 채점 기준으로. 그리고 실제로 차이를 만드는 것이 무엇인지 공개합니다.

- **스폰서 없음. 제휴 링크 없음.** 숫자로만 말합니다.
- **모든 원본 실행 로그 공개.** 결과에 동의할 수 없다면 직접 재실행해 보세요.
- **스킬이 퇴보하면 그대로 말합니다** — 그리고 업스트림에 이슈를 올립니다.

> 📬 **다음 주 월요일 결과 받아보기:** Watch → Custom → Releases

## 🏆 리더보드

> **첫 벤치마크가 진행 중입니다.** 첫 주간 리더보드는 **2026년 8월**에 공개됩니다.

매주, 등록된 모든 스킬에 대해 리더보드는 다음을 보고합니다:

| 컬럼 | 의미 |
|---|---|
| **Solve rate** | 히든 테스트 스위트를 통과한 태스크 비율 |
| **Δ week** | 지난주 대비 순위 변동 |
| **Tokens per solve** | 성공한 실행의 중앙값 토큰 비용 |
| **vs baseline** | **스킬 없이** 돌린 순정 에이전트 대비 개선폭 |

**baseline 행이 이 프로젝트의 핵심입니다.** 대부분의 스킬 README는 아무것과도 비교하지 않습니다. 우리는 스킬 없는 순정 에이전트를 매주 모든 태스크에 돌립니다 — "아무것도 없음"을 이기지 못하는 스킬이 여러분의 컨텍스트 윈도우를 차지할 이유가 없으니까요.

## 🔬 측정 방법

- 5개 카테고리에 걸친 **고정 태스크 20개**: bugfix (6), feature (5), refactor (4), test-writing (3), docs (2). 실제 OSS 저장소의 실제 이슈이며, 각각 히든 테스트 스위트가 있습니다. 스펙은 [`tasks/`](../tasks/)에 있습니다.
- **스킬당 태스크당 3회 실행**, 고정된 동일 모델·버전 (현재 `claude-opus-4-8`). 중앙값을 보고하며 분산이 큰 결과는 표시합니다.
- **Solve = 히든 테스트 통과.** 대표 수치에 LLM 심판을 쓰지 않습니다.
- **모든 것이 재현 가능합니다:** 하네스는 [`harness/`](../harness/), 태스크 스펙은 [`tasks/`](../tasks/), 원본 실행 로그는 [`runs/`](../runs/)에.

전체 방법론: [`harness/README.md`](../harness/README.md)

## 📥 스킬 등록하기

[`skills.yaml`](../skills.yaml)에 PR로 한 항목만 추가하세요 — 다음 월요일 벤치에 들어갑니다:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # 이 스킬이 돕는다고 주장하는 태스크 카테고리
```

측정된 스킬은 README에 달 수 있는 라이브 배지를 받습니다:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 저장소 구조

```
skillbench/
├── README.md            # 이번 주 리포트 (매주 월요일 재생성)
├── translations/        # 자동 동기화되는 언어판
├── reports/             # 주간 리포트 아카이브 + 역대 순위 히스토리
├── harness/             # 러너 — 공개, 재현 가능
├── tasks/               # 태스크 스펙 20개 (히든 테스트는 프라이빗 저장소에)
├── runs/                # 매주 모든 실행의 원본 JSONL 로그
└── skills.yaml          # 레지스트리: PR 한 줄 = 다음 월요일 벤치
```

## ❓ 왜 만들었나

이 저장소의 관리자는 예전에 개발자용 북마크 큐레이션을 운영했습니다. 어느 날 그 저장소의 실제 star 증가 속도를 측정해 봤고 — 숫자는 큐레이션의 시대가 끝났다고 말했습니다. 그래서 GitHub에서 가장 시끄러운 동네에서 아무도 하지 않는 일로 피봇했습니다: **그중에 진짜 효과 있는 게 뭔지 측정하는 일.** 측정이 곧 브랜드입니다. 시작은 우리 자신이었습니다.

## 📄 라이선스

[MIT](../LICENSE) — 하네스, 태스크 스펙, 공개된 모든 데이터.
