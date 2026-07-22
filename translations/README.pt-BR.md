<div align="center">

# ⚡ SkillBench

**Skills de agentes realmente funcionam? Nós medimos.**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

[English](../README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · Português

</div>

---

Centenas de skills, presets de `CLAUDE.md` e configurações de agentes prometem um agente de programação melhor. Toda segunda-feira, o SkillBench executa as mais populares contra as mesmas **20 tarefas reais de programação** — mesmo modelo, mesmos repositórios, mesma rubrica — e publica o que realmente faz diferença.

- **Sem patrocinadores. Sem links de afiliados.** Apenas números.
- **Todos os logs brutos de execução são públicos.** Discorda de um resultado? Execute novamente você mesmo.
- **Se uma skill regredir, nós dizemos** — e abrimos a issue upstream.

> 📬 **Receba os resultados da próxima segunda:** Watch → Custom → Releases

## 🏆 Placar

> **A primeira execução do benchmark está em andamento.** O primeiro placar semanal sai em **agosto de 2026**.

Toda semana, para cada skill registrada, o placar reporta:

| Coluna | Significado |
|---|---|
| **Solve rate** | % de tarefas em que a suíte de testes oculta passa |
| **Δ week** | mudança de posição em relação à semana anterior |
| **Tokens per solve** | custo mediano em tokens de uma execução bem-sucedida |
| **vs baseline** | melhoria sobre um agente **sem nenhuma skill instalada** |

**A linha baseline é o coração do projeto.** A maioria dos READMEs de skills não se compara com nada. Nós executamos um agente sem skills em todas as tarefas, toda semana — uma skill que não consegue vencer o "nada" não deveria ocupar a sua janela de contexto.

## 🔬 Como medimos

- **20 tarefas fixas** em 5 categorias: bugfix (6), feature (5), refactor (4), test-writing (3), docs (2). Issues reais de repositórios OSS reais, cada uma com uma suíte de testes oculta. As especificações estão em [`tasks/`](../tasks/).
- **3 execuções por skill por tarefa**, mesmo modelo e versão fixados (atualmente `claude-opus-4-8`). Reportamos medianas e sinalizamos resultados de alta variância.
- **Solve = testes ocultos passam.** Sem LLM como juiz para o número principal.
- **Tudo é reproduzível:** o harness em [`harness/`](../harness/), as especificações em [`tasks/`](../tasks/), cada log bruto em [`runs/`](../runs/).

Metodologia completa: [`harness/README.md`](../harness/README.md)

## 📥 Registre sua skill

Adicione uma entrada ao [`skills.yaml`](../skills.yaml) via PR — ela entra no bench da próxima segunda:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # categorias de tarefas que a skill afirma melhorar
```

Skills medidas recebem um badge ao vivo para o README:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 Estrutura do repositório

```
skillbench/
├── README.md            # o relatório desta semana (regenerado toda segunda)
├── translations/        # edições de idioma sincronizadas automaticamente
├── reports/             # arquivo de relatórios semanais + histórico de posições
├── harness/             # o runner — aberto, reproduzível
├── tasks/               # 20 especificações de tarefas (testes ocultos em repo privado)
├── runs/                # logs JSONL brutos de cada execução, toda semana
└── skills.yaml          # o registro: uma linha de PR = bench da próxima segunda
```

## ❓ Por que isso existe?

O autor deste repositório mantinha antes uma lista curada de favoritos para desenvolvedores. Um dia medimos a velocidade real de estrelas dela — e os números disseram que a era da curadoria tinha acabado. Então pivotamos para o que ninguém fazia no canto mais barulhento do GitHub: **medir se algo disso realmente funciona.** Medição é a marca. E começou em casa.

## 📄 Licença

[MIT](../LICENSE) — harness, especificações de tarefas e todos os dados publicados.
