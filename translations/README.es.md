<div align="center">

# ⚡ SkillBench

**¿Las skills de agentes realmente funcionan? Nosotros lo medimos.**

<p>
  <img src="https://img.shields.io/badge/status-first_bench_in_progress-e3a008" alt="Status">
  <img src="https://img.shields.io/badge/tasks-20_fixed-blue" alt="Tasks">
  <img src="https://img.shields.io/badge/raw_logs-100%25_public-2f7d4f" alt="Raw logs public">
  <img src="https://img.shields.io/github/license/currenjin/skillbench" alt="License">
</p>

[English](../README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · Español · [Português](README.pt-BR.md)

</div>

---

Cientos de skills, presets de `CLAUDE.md` y configuraciones de agentes prometen un mejor agente de programación. Cada lunes, SkillBench ejecuta las más populares contra las mismas **20 tareas de programación del mundo real** — mismo modelo, mismos repositorios, misma rúbrica — y publica qué es lo que realmente marca la diferencia.

- **Sin patrocinadores. Sin enlaces de afiliados.** Solo números.
- **Todos los logs de ejecución en bruto son públicos.** ¿No estás de acuerdo con un resultado? Vuelve a ejecutarlo tú mismo.
- **Si una skill empeora, lo decimos** — y abrimos el issue upstream.

> 📬 **Recibe los resultados del próximo lunes:** Watch → Custom → Releases

## 🏆 Tabla de clasificación

> **La primera ejecución del benchmark está en curso.** La primera tabla semanal se publica en **agosto de 2026**.

Cada semana, para cada skill registrada, la tabla reporta:

| Columna | Significado |
|---|---|
| **Solve rate** | % de tareas donde la suite de tests oculta pasa |
| **Δ week** | cambio de posición respecto a la semana anterior |
| **Tokens per solve** | costo mediano en tokens de una ejecución exitosa |
| **vs baseline** | mejora sobre un agente sin **ninguna skill instalada** |

**La fila baseline es el corazón del proyecto.** La mayoría de los README de skills no se comparan con nada. Nosotros ejecutamos un agente sin skills en cada tarea, cada semana — una skill que no puede superar a "nada" no debería ocupar tu ventana de contexto.

## 🔬 Cómo medimos

- **20 tareas fijas** en 5 categorías: bugfix (6), feature (5), refactor (4), test-writing (3), docs (2). Issues reales de repositorios OSS reales, cada uno con una suite de tests oculta. Las especificaciones viven en [`tasks/`](../tasks/).
- **3 ejecuciones por skill por tarea**, mismo modelo y versión fijados (actualmente `claude-opus-4-8`). Reportamos medianas y marcamos resultados de alta varianza.
- **Solve = los tests ocultos pasan.** Sin LLM como juez para la cifra principal.
- **Todo es reproducible:** el harness en [`harness/`](../harness/), las especificaciones en [`tasks/`](../tasks/), cada log en bruto en [`runs/`](../runs/).

Metodología completa: [`harness/README.md`](../harness/README.md)

## 📥 Registra tu skill

Agrega una entrada a [`skills.yaml`](../skills.yaml) vía PR — entra al bench del próximo lunes:

```yaml
- repo: your-name/your-skill
  skill: skill-name
  categories: [bugfix, feature]   # categorías de tareas que la skill dice mejorar
```

Las skills medidas reciben un badge en vivo para su README:

&nbsp;&nbsp;`⚡ SkillBench · #3 · 85% solve` &nbsp;·&nbsp; `⚡ SkillBench · measured 2026-W32`

## 🗂 Estructura del repositorio

```
skillbench/
├── README.md            # el reporte de esta semana (regenerado cada lunes)
├── translations/        # ediciones de idioma sincronizadas automáticamente
├── reports/             # archivo de reportes semanales + historial de posiciones
├── harness/             # el runner — abierto, reproducible
├── tasks/               # 20 especificaciones de tareas (tests ocultos en repo privado)
├── runs/                # logs JSONL en bruto de cada ejecución, cada semana
└── skills.yaml          # el registro: una línea de PR = bench del próximo lunes
```

## ❓ ¿Por qué existe esto?

El autor de este repositorio mantenía antes una lista curada de marcadores para desarrolladores. Un día medimos su velocidad real de estrellas — y los números dijeron que la era de la curación había terminado. Así que pivotamos hacia lo que nadie hacía en el rincón más ruidoso de GitHub: **medir si algo de esto realmente funciona.** La medición es la marca. Y empezó en casa.

## 📄 Licencia

[MIT](../LICENSE) — harness, especificaciones de tareas y todos los datos publicados.
