<div align="center">

# ⚡ SkillBench

**智能体技能真的有用吗？我们来测量。**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

[English](../README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · 简体中文 · [Español](README.es.md) · [Português](README.pt-BR.md)

</div>

---

数百个技能、`CLAUDE.md` 预设和智能体配置都承诺能带来更强的编码智能体。SkillBench 每周一将最热门的那些放到同一组 **20 个真实编码任务**上运行 — 相同的模型、相同的仓库、相同的评分标准 — 然后公布究竟哪些真正有效。

- **没有赞助商。没有推广链接。** 只用数字说话。
- **所有原始运行日志全部公开。** 不认同某个结果？自己重跑一遍。
- **技能出现退化，我们直说** — 并向上游提 issue。

> 📬 **获取下周一的结果:** Watch → Custom → Releases

## 🏆 排行榜

> **首次基准测试正在进行中。** 第一期周排行榜将于 **2026 年 8 月**发布。

每周，排行榜为每个注册技能报告以下指标:

| 列 | 含义 |
|---|---|
| **Solve rate** | 通过隐藏测试套件的任务比例 |
| **Δ week** | 相比上周的排名变动 |
| **Tokens per solve** | 成功运行的 token 成本中位数 |
| **vs baseline** | 相比**未安装任何技能**的原生智能体的提升 |

**baseline 这一行是整个项目的意义所在。** 大多数技能的 README 不与任何东西对比。我们每周都在所有任务上运行一个不带技能的原生智能体 — 连"什么都不装"都赢不了的技能，不配占用你的上下文窗口。

## 🔬 测量方法

- 覆盖 5 个类别的 **20 个固定任务**: bugfix (6)、feature (5)、refactor (4)、test-writing (3)、docs (2)。全部来自真实开源仓库的真实 issue，每个任务配有隐藏测试套件。规格见 [`tasks/`](../tasks/)。
- **每个技能每个任务运行 3 次**，使用固定的同一模型和版本（当前为 `claude-opus-4-8`）。报告中位数，并标注高方差结果。
- **Solve = 隐藏测试通过。** 头条数字不使用 LLM 评判。
- **一切皆可复现:** 运行器在 [`harness/`](../harness/)，任务规格在 [`tasks/`](../tasks/)，原始运行日志在 [`runs/`](../runs/)。

完整方法论: [`harness/README.md`](../harness/README.md)

## 📥 提交技能

向 [`skills.yaml`](../skills.yaml) 提一个 PR 加一条记录 — 下周一即进入基准测试:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # 该技能声称能帮助的任务类别
```

被测量的技能会获得可放入 README 的实时徽章:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 仓库结构

```
skillbench/
├── README.md            # 本周报告（每周一重新生成）
├── translations/        # 自动同步的语言版本
├── reports/             # 周报归档 + 历史排名记录
├── harness/             # 运行器 — 公开、可复现
├── tasks/               # 20 个任务规格（隐藏测试存放在私有仓库）
├── runs/                # 每周所有运行的原始 JSONL 日志
└── skills.yaml          # 注册表: PR 一行 = 下周一进入测试
```

## ❓ 为什么做这个

本仓库的维护者曾经运营一个面向开发者的书签精选仓库。有一天我们测量了它真实的 star 增长速度 — 数字表明精选列表的时代已经结束。于是我们转向了 GitHub 最热闹的角落里没人做的事: **测量这些东西里到底哪些真正有效。** 测量就是我们的品牌。而这一切，是从测量我们自己开始的。

## 📄 许可证

[MIT](../LICENSE) — 运行器、任务规格及所有公开数据。
