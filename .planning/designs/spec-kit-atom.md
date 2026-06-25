# Design: Atom como harness de spec-kit

**Fecha:** 2026-06-25 (reescrito tras investigar el modelo real de spec-kit)
**Estado:** Aprobado — fase 1 implementada

## Contexto

Atom Developer Skills (ADS) provee dos skills de Claude Code:
- `ads:spec` — convierte FRDs de Confluence en Spec Técnica
- `ads:task` — toma un task de Jira y ejecuta el ciclo de implementación (Jira→Confluence→Figma→CodeGraph→brief)

spec-kit (GitHub-backed, ecosistema creciente de extensiones/presets, soporte 17+ agentes) es una base sólida de SDD. La oportunidad: usar spec-kit como **core que avanza solo**, y montar encima lo propio de Atom — reglas del codebase + ingesta de Jira — sin forkear ni reimplementar el flujo.

## Problema

Dos dolores distintos:
1. **Reglas repetidas:** el agente necesita que le expliquen las reglas del codebase (Angular, sin `any`, i18n, commits, CodeGraph) en cada sesión.
2. **Contexto del task repetido:** el agente re-fetchea Jira + Confluence + Figma al inicio de cada tarea.

## El modelo real de spec-kit (investigado, no asumido)

spec-kit tiene **tres mecanismos distintos**, con capacidades que NO se solapan:

| Mecanismo | Manifest | Puede | NO puede |
|-----------|----------|-------|----------|
| **Preset** | `preset.yml` | Overridear templates/commands core (`replace`/`prepend`/`append`/`wrap`) | Agregar comandos nuevos |
| **Extensión** | `extension.yml` | Agregar comandos nuevos `speckit.<id>.<cmd>`, hooks de ciclo de vida, config | Overridear/wrappear core |
| **Bundle** | `bundle.yml` | Componer extensión + preset en un `specify bundle install` | Comportamiento propio |

Hallazgos clave (fuente: `github/spec-kit` @ main, v0.11.8):
- Un comando con 3+ segmentos (`speckit.atom.context`) es **comando de extensión** y se omite si la extensión no está instalada. **No puede vivir en un preset.**
- No existe tipo `memory`/`constitution`. El constitution se entrega overrideando el template `constitution-template` (`replaces: constitution-template`) — un preset.
- Hooks (`before_specify`, `after_implement`, …) son **feature de extensión**, no de preset. Son el mecanismo correcto para quality gates post-implement.
- `specify init --preset` toma un **ID de catálogo**, no una URL. Instalación por URL/local: `specify preset add` / `specify extension add` con `--from`/`--dev`.
- Ninguna extensión comunitaria hace Jira→spec (las 8 de Jira/ADO van spec→tracker). La ingesta de Atom es net-new; referencias de patrón: `github-issues`/`issue` (inbound) y `cleanup` (quality gate).

## Mapeo dolor → mecanismo

| Dolor | Pieza | Fricción |
|-------|-------|----------|
| Reglas/stack repetidos | **Preset** (`constitution-template` + append a spec/plan) | Mínima — puro override, hereda mejoras de spec-kit gratis |
| Contexto del task repetido | **Extensión** (`speckit.atom.context` + hooks) | Alta — comando net-new, lógica de ingesta |

## Decisión: faseado preset → extensión → bundle

Se construye en fases, empezando por la de menor fricción (la que mejor encarna "harness que dirige sin fricción"):

### Fase 1 — Preset `atom` ✅ (implementada)

```
preset/
  preset.yml
  templates/
    constitution-template.md   (replace)  reglas de Atom: reuso/CodeGraph, sin any,
                                           scope exacto, escepticismo, verificación ACs,
                                           reglas por stack (Angular/CF/RN)
    spec-template.md           (append)   stack · Figma · contratos TS · blast radius
    plan-template.md           (append)   concreción · verificación · commits · CodeGraph
```

Instalación: `specify preset add atom --dev ./preset` (o `--from <zip>` / catálogo).

### Fase 2 — Extensión `atom` ⏳

```
extension/
  extension.yml
  commands/
    speckit.atom.context.md      ingesta Jira+Confluence+Figma (evoluciona ads:task)
    speckit.atom.verify.md       typecheck TS + verificación de ACs
    speckit.atom.pr.md           crear PR con [TICKET-ID]
  hooks:
    before_specify  → prompt para correr speckit.atom.context
    after_implement → [verify (priority 5), pr (priority 20, opcional)]
```

Instalación: `specify extension add atom --dev ./extension`.

### Fase 3 — Bundle `atom` ⏳

```
bundle.yml   → referencia extensión atom + preset atom
```

Instalación única: `specify bundle install atom`.

## Lo que no cambia / stopgap

- `skills/task` (`ads:task`) ya hace la ingesta Jira→Confluence→Figma hoy. Se mantiene como **stopgap** y como **prototipo de referencia** para `speckit.atom.context` (fase 2).
- El source of truth entre sprints sigue siendo la Spec Técnica en Confluence.

## Lo que se deprecó (fase de limpieza)

- `packages/cli/` (installer npm `ads`), `package.json`, `.claude-plugin/plugin.json` → reemplazados por `specify preset add`. **Borrados.**

## Repositorio

Mismo repo, renombrado: `antony-hernandez/spec-kit-atom` (público, instalable vía `specify preset add --from`).

## Criterios de aceptación

### Fase 1 (preset)
- [x] `preset.yml` válido contra el schema real (constitution-template replace + spec/plan append)
- [x] `specify preset add atom --dev ./preset` instala el constitution de Atom y compone los templates — validado e2e con spec-kit v0.11.9: `preset resolve` muestra `constitution-template` reemplazado (contenido Atom) y `spec/plan-template` compuestos `core → atom`
- [x] Los templates de Atom quedan en lugar para `/speckit.constitution`, `/speckit.specify`, `/speckit.plan` (confirmado por la resolución de capas)

### Fase 2 (extensión)
- [x] `extension.yml` válido; `specify extension add ./extension --dev` registra los 3 comandos como skills de Claude (`.claude/skills/speckit-atom-*`) y 2 hooks (`before_specify`, `after_implement`) en `.specify/extensions.yml` — validado e2e con spec-kit v0.11.9
- [ ] `speckit.atom.context CV-599` fetchea Jira+Confluence+Figma y deja contexto utilizable — pendiente: runtime contra un ticket real (requiere MCP Atlassian + ticket)
- [ ] Hook `after_implement` corre typecheck + verifica ACs + ofrece PR — pendiente: runtime en un proyecto con implementación

### Fase 3 (bundle)
- [ ] `specify bundle install atom` instala extensión + preset en un paso
