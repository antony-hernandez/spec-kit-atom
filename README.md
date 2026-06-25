# Atom para spec-kit

**Un harness de [spec-kit](https://github.com/github/spec-kit) que dirige el flujo Spec-Driven Development con las tecnologías, reglas y casos de uso de Atom** — para no repetir el mismo contexto en cada tarea.

spec-kit es el core (avanza rápido, lo seguimos). Atom monta encima sus reglas y, más adelante, su ingesta de Jira/Confluence/Figma. Sin forkear, sin reimplementar el flujo: solo lo que es propio de Atom.

---

## Arquitectura

spec-kit distingue tres mecanismos. Atom usa los tres, en fases:

| Pieza | Mecanismo spec-kit | Qué aporta | Estado |
|-------|--------------------|------------|--------|
| **Preset `atom`** | overridea templates/commands core | Constitution con las reglas de Atom + secciones de Atom en spec/plan | ✅ Fase 1 |
| **Extensión `atom`** | agrega comandos + hooks nuevos | `speckit.atom.context` (ingesta Jira+Confluence+Figma) + quality gates post-implement | ⏳ Fase 2 |
| **Bundle `atom`** | compone extensión + preset | Una sola instalación (`specify bundle install`) | ⏳ Fase 3 |

> Un **preset** solo puede *overridear* lo que ya existe en spec-kit — no agrega comandos nuevos. Los comandos nuevos (la ingesta) son trabajo de una **extensión**. Por eso el faseo.

---

## Preset `atom` (fase 1)

Dirige el flujo SDD con las reglas del codebase de Atom:

| Provide | Estrategia | Qué hace |
|---------|-----------|----------|
| `constitution-template` | `replace` | Reemplaza el constitution core con las reglas no negociables de Atom: reuso/CodeGraph, sin `any`, scope exacto, escepticismo documental, verificación de ACs, y reglas por stack (Angular / Cloud Functions / React Native) |
| `spec-template` | `append` | Agrega al spec: stack, Figma node-id, contratos TypeScript, blast radius |
| `plan-template` | `append` | Agrega al plan: regla de concreción, verificación por tarea, formato de commit, gate de CodeGraph |

### Instalación

Desde un proyecto con spec-kit inicializado:

```bash
# Por catálogo (cuando esté publicado)
specify preset add atom

# Desde una URL (zip de un tag)
specify preset add atom --from https://github.com/antony-hernandez/spec-kit-atom/archive/refs/tags/v1.0.0.zip

# En desarrollo, desde esta copia local
specify preset add atom --dev ./preset
```

Verificá con `specify preset list`. Al correr `/speckit.constitution`, `/speckit.specify` y `/speckit.plan`, el flujo ya sale con el contexto de Atom.

> `specify init --preset` toma un **ID de catálogo**, no una URL. Para URL o ruta local usá `specify preset add`.

---

## Estructura del repo

```
preset/                          ← Fase 1 — preset de spec-kit
  preset.yml                     ← manifest (constitution replace + spec/plan append)
  templates/
    constitution-template.md     ← reglas de Atom
    spec-template.md             ← secciones de Atom para el spec
    plan-template.md             ← constraints de Atom para el plan
  README.md
skills/                          ← Legacy / stopgap — skills ads:task y ads:spec
  task/SKILL.md                  ← ingesta Jira→Confluence→Figma (prototipo de la extensión fase 2)
  spec/SKILL.md                  ← FRD → spec técnica
.planning/                       ← diseño, plan y spikes
```

### `skills/` — stopgap hasta la fase 2

`ads:task` ya hace hoy la ingesta Jira→Confluence→Figma como skill de Claude Code. Se mantiene como stopgap mientras se construye la extensión `speckit.atom.context` (fase 2), que es su evolución dentro de spec-kit.

---

## Requisitos

- spec-kit `>=0.6.0`
- MCPs: Atlassian (Jira+Confluence), Figma, CodeGraph — vía claude.ai/settings → Integrations

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).
