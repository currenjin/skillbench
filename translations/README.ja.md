<div align="center">

# ⚡ SkillBench

**エージェントスキルは本当に効くのか？私たちは測定します。**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

[English](../README.md) · [한국어](README.ko.md) · 日本語 · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md)

</div>

---

何百ものスキル、`CLAUDE.md` プリセット、エージェント設定が「より良いコーディングエージェント」を約束しています。SkillBench は毎週月曜日、最も人気のあるものを同一の**実世界コーディングタスク 20 個**に対して実行します — 同じモデル、同じリポジトリ、同じ採点基準で。そして実際に効果があるものを公開します。

- **スポンサーなし。アフィリエイトリンクなし。** 数字だけで語ります。
- **すべての生実行ログを公開。** 結果に納得できなければ、自分で再実行してください。
- **スキルが劣化したら、そのまま報告します** — そして上流に issue を立てます。

> 📬 **来週月曜日の結果を受け取る:** Watch → Custom → Releases

## 🏆 リーダーボード

> **最初のベンチマークを実行中です。** 最初の週間リーダーボードは **2026 年 8 月**に公開されます。

毎週、登録されたすべてのスキルについて、リーダーボードは以下を報告します:

| 列 | 意味 |
|---|---|
| **Solve rate** | 隠しテストスイートに合格したタスクの割合 |
| **Δ week** | 先週からの順位変動 |
| **Tokens per solve** | 成功した実行のトークンコスト中央値 |
| **vs baseline** | **スキルなし**の素のエージェントに対する改善幅 |

**baseline の行こそがこのプロジェクトの核心です。** ほとんどのスキルの README は何とも比較していません。私たちはスキルなしの素のエージェントを毎週すべてのタスクで実行します — 「何もなし」に勝てないスキルが、あなたのコンテキストウィンドウを占有すべきではありません。

## 🔬 測定方法

- 5 カテゴリにわたる**固定タスク 20 個**: bugfix (6)、feature (5)、refactor (4)、test-writing (3)、docs (2)。実際の OSS リポジトリの実際の issue で、それぞれに隠しテストスイートがあります。仕様は [`tasks/`](../tasks/) にあります。
- **スキルごと・タスクごとに 3 回実行**、固定された同一モデル・バージョン（現在 `claude-opus-4-8`）。中央値を報告し、分散の大きい結果には印を付けます。
- **Solve = 隠しテスト合格。** 見出しの数字に LLM 審判は使いません。
- **すべて再現可能:** ハーネスは [`harness/`](../harness/)、タスク仕様は [`tasks/`](../tasks/)、生実行ログは [`runs/`](../runs/) に。

完全な方法論: [`harness/README.md`](../harness/README.md)

## 📥 スキルを登録する

[`skills.yaml`](../skills.yaml) に PR で 1 エントリ追加するだけ — 次の月曜日のベンチに入ります:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # このスキルが役立つと主張するタスクカテゴリ
```

測定されたスキルは README に貼れるライブバッジを受け取ります:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 リポジトリ構成

```
skillbench/
├── README.md            # 今週のレポート（毎週月曜日に再生成）
├── translations/        # 自動同期される言語版
├── reports/             # 週間レポートのアーカイブ + 歴代順位履歴
├── harness/             # ランナー — 公開、再現可能
├── tasks/               # タスク仕様 20 個（隠しテストはプライベートリポジトリに）
├── runs/                # 毎週すべての実行の生 JSONL ログ
└── skills.yaml          # レジストリ: PR 1 行 = 次の月曜日のベンチ
```

## ❓ なぜ作ったのか

このリポジトリの管理者は、かつて開発者向けブックマークのキュレーションを運営していました。ある日、そのリポジトリの実際の star 増加速度を測定してみたところ — 数字はキュレーションの時代の終わりを告げていました。そこで、GitHub で最も騒がしい界隈で誰もやっていないことにピボットしました: **その中で本当に効果があるものを測定すること。** 測定こそがブランドです。始まりは私たち自身でした。

## 📄 ライセンス

[MIT](../LICENSE) — ハーネス、タスク仕様、公開されたすべてのデータ。
