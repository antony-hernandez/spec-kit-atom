# Atom para spec-kit

[![ci](https://github.com/antony-hernandez/spec-kit-atom/actions/workflows/ci.yml/badge.svg)](https://github.com/antony-hernandez/spec-kit-atom/actions/workflows/ci.yml)

**Un harness de [spec-kit](https://github.com/github/spec-kit) que dirige el flujo Spec-Driven Development con las tecnologías, reglas y casos de uso de Atom** — para no repetir el mismo contexto en cada tarea.

spec-kit es el core (avanza rápido, lo seguimos). Atom monta encima sus reglas y su ingesta de Jira/Confluence/Figma. Sin forkear, sin reimplementar el flujo: solo lo que es propio de Atom.

---

## Arquitectura

spec-kit distingue tres mecanismos. Atom usa los tres, en fases:

| Pieza | Mecanismo spec-kit | Qué aporta | Estado |
|-------|--------------------|------------|--------|
| **Preset `atom`** | overridea templates/commands core | Constitution con las reglas de Atom + secciones de Atom en spec/plan | ✅ Fase 1 |
| **Extensión `atom`** | agrega comandos + hooks nuevos | `speckit.atom.context` (ingesta Jira+Confluence+Figma) + quality gates post-implement | ✅ Fase 2 |
| **Bundle `atom`** | compone extensión + preset | Una sola instalación (`specify bundle install`) | ⏳ Fase 3 |

> Un **preset** solo puede *overridear* lo que ya existe en spec-kit — no agrega comandos nuevos. Los comandos nuevos (la ingesta) son trabajo de una **extensión**. Por eso el faseo: el preset (steering, fricción mínima) primero, la extensión (ingesta + gates) después, y el bundle los une en un solo install.

---

## Instalación

Requiere [spec-kit](https://github.com/github/spec-kit) instalado (`uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`) y un proyecto inicializado (`specify init . --integration claude`).

Por defecto se instala la **última versión** (rama `main`):

```bash
# Preset (reglas + templates de Atom)
specify preset add atom --from https://github.com/antony-hernandez/spec-kit-atom/archive/refs/heads/main.zip

# Extensión (ingesta + quality gates)
specify extension add atom --from https://github.com/antony-hernandez/spec-kit-atom/archive/refs/heads/main.zip
```

Para fijar una versión, apuntá a un tag en vez de `heads/main`: `.../archive/refs/tags/v1.0.0.zip`.

En desarrollo, desde un clon local del repo:

```bash
specify preset add atom --dev ./preset
specify extension add ./extension --dev
```

Verificá con `specify preset list` y `specify extension list`.

> `specify init --preset` toma un **ID de catálogo**, no una URL. Para URL o ruta local usá `specify preset add` / `specify extension add`.

---

## Flujo de trabajo

Con el preset y la extensión instalados, una tarea de Atom corre así:

```
speckit.atom.context CV-599   ← ingesta Jira+HU+Spec Técnica+Figma → .specify/memory/atom-context.md
/speckit.specify              ← spec-kit genera el spec, ya con las secciones de Atom (preset)
/speckit.plan                 ← plan con la regla de concreción + gate de CodeGraph (preset)
/speckit.tasks
/speckit.implement            ← al terminar dispara el hook after_implement:
                                  → speckit.atom.verify  (typecheck + verificación de ACs)
                                  → speckit.atom.pr       (PR con [CV-599], opcional)
```

El hook `before_specify` ofrece correr `speckit.atom.context` automáticamente antes de especificar. La constitution de Atom (reglas del codebase) la lee spec-kit en cada sesión vía `/speckit.constitution`.

---

## Preset `atom` (fase 1)

Dirige el flujo SDD con las reglas del codebase de Atom:

| Provide | Estrategia | Qué hace |
|---------|-----------|----------|
| `constitution-template` | `replace` | Reemplaza el constitution core con las reglas no negociables de Atom: reuso/CodeGraph, sin `any`, scope exacto, escepticismo documental, verificación de ACs, y reglas por stack (Angular / Cloud Functions / React Native) |
| `spec-template` | `append` | Agrega al spec: stack, Figma node-id, contratos TypeScript, blast radius |
| `plan-template` | `append` | Agrega al plan: regla de concreción, verificación por tarea, formato de commit, gate de CodeGraph |

## Extensión `atom` (fase 2)

Agrega lo que spec-kit no tiene — la ingesta de contexto de Atom y los quality gates:

| Comando | Qué hace |
|---------|----------|
| `speckit.atom.context <CV-599>` | Fetch Jira + HU + Spec Técnica (Confluence) + Figma → escribe `.specify/memory/atom-context.md` que `/speckit.specify` consume |
| `speckit.atom.verify` | Typecheck de TypeScript + verificación de los ACs contra la implementación |
| `speckit.atom.pr` | Crea el PR con título `[TICKET-ID]` y checklist de ACs |

Enganchados con hooks: `before_specify` → `context` (opcional, pregunta), `after_implement` → `verify` (priority 5) + `pr` (priority 20, opcional).

---

## Estructura del repo

```
preset/                          ← Fase 1 — preset de spec-kit
  preset.yml                     ← manifest (constitution replace + spec/plan append)
  templates/
    constitution-template.md     ← reglas de Atom
    spec-template.md             ← secciones de Atom para el spec
    plan-template.md             ← constraints de Atom para el plan
extension/                       ← Fase 2 — extensión de spec-kit
  extension.yml                  ← manifest (3 comandos + hooks)
  commands/
    speckit.atom.context.md      ← ingesta Jira→Confluence→Figma
    speckit.atom.verify.md       ← typecheck + verificación de ACs
    speckit.atom.pr.md           ← creación de PR
.planning/                       ← diseño y spikes
```

---

## Requisitos

- spec-kit `>=0.9.0` (la extensión usa hooks de ciclo de vida)
- MCPs: Atlassian (Jira+Confluence), Figma, CodeGraph — vía claude.ai/settings → Integrations

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Roadmap y diseño en [`.planning/designs/spec-kit-atom.md`](.planning/designs/spec-kit-atom.md).
