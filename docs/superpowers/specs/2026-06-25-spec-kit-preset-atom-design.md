# Design: Atom Preset para spec-kit

**Fecha:** 2026-06-25
**Estado:** Aprobado

## Contexto

Atom Developer Skills (ADS) es un plugin de Claude Code que provee dos skills:
- `ads:spec` — convierte FRDs de Confluence en Spec Técnica
- `ads:task` — toma un task de Jira y ejecuta el ciclo completo de implementación

El equipo identificó que spec-kit (115K+ stars, GitHub-backed) provee una base de SDD con creciente ecosistema de extensiones, integraciones, y soporte para 17+ agentes de AI. La oportunidad es usar spec-kit como core y distribuir la lógica de Atom como un **preset**, en lugar de mantener un plugin independiente.

## Problema

El workflow de Atom es time-separated por naturaleza:
- **Hoy (sprint de diseño):** el tech lead crea la Spec Técnica en Confluence a partir del FRD
- **Días después (sprint de desarrollo):** el developer retoma el task en Jira y arranca la implementación

Sin una capa de contexto persistente, el agente de AI tiene que re-fetchear Jira + Confluence + Figma al inicio de cada sesión. Además, las reglas del codebase (Angular, TypeScript strict, CodeGraph, commit format, i18n) hay que explicarlas repetidamente.

## Decisiones de diseño

### spec-kit como core, no como dependencia

Atom ya tiene el workflow correcto. spec-kit resuelve el problema de equipos que no tienen estructura — Atom ya la tiene, y en las herramientas correctas (Jira + Confluence, no archivos markdown locales).

Lo que spec-kit sí aporta: creciente ecosistema de extensiones, registro automático de comandos en 17+ agentes, y un modelo de preset que permite distribuir configuración reutilizable.

### Preset sobre extensión

Un preset puede wrappear comandos core de spec-kit con `strategy: "wrap"`. Esto significa que cuando spec-kit mejora `/speckit-specify` o `/speckit-implement`, las mejoras llegan automáticamente — el wrap solo agrega contexto de Atom antes y después. Una extensión que reemplaza comandos core acumularía deuda de mantenimiento con cada release de spec-kit.

### Wrap, no replace

Los comandos `speckit.specify` y `speckit.implement` se wrappean, no se reemplazan. El contenido del core va en el placeholder `{CORE_TEMPLATE}`. Atom agrega:
- **Antes del specify:** ingesta de Jira + Confluence + Figma → `.specify/memory/atom-context.md`
- **Después del implement:** TypeScript typecheck + verificación de ACs + prompt push/PR

### `ads install` → `specify init --preset atom --integration claude`

La distribución pasa a ser un único comando que inicializa spec-kit con todo el contexto de Atom preconfigurado. El CLI de ADS puede seguir existiendo como wrapper delgado que ejecuta este comando.

## Arquitectura

```
spec-kit-preset-atom/           ← nuevo repo público
  preset.yml                    ← manifest del preset
  commands/
    speckit.specify.md          ← WRAP: contexto Atom antes del specify core
    speckit.implement.md        ← WRAP: verificación Atom después del implement core
    speckit.atom.context.md     ← NEW: ingesta standalone de contexto Jira+Confluence+Figma
  templates/
    spec-template.md            ← APPEND: secciones de Atom al spec-template core
    plan-template.md            ← APPEND: secciones de Atom al plan-template core
  memory/
    constitution.md             ← reglas del codebase de Atom (Angular, TS strict, i18n, etc.)
```

### Flujo resultante

```
specify init --preset atom --integration claude
  └── instala spec-kit base
  └── aplica preset atom:
        constitution.md  → .specify/memory/constitution.md
        spec-template    → append al core
        plan-template    → append al core
        speckit.specify  → wrap + registro en .claude/skills/
        speckit.implement → wrap + registro en .claude/skills/
        speckit.atom.context → nuevo skill en .claude/skills/
```

Workflow del equipo:

```
Sprint de diseño
  /speckit-specify [descripción o Jira ID]
    → wrap: fetch Jira+Confluence+Figma → atom-context.md
    → core: genera SPEC.md con plantilla de Atom
    → (opcionalmente actualiza Confluence Spec Técnica)

Sprint de desarrollo
  /speckit-atom-context CV-599   ← si el contexto no está fresco
  /speckit-plan
  /speckit-tasks
  /speckit-implement
    → core: ejecuta tasks del TASKS.md
    → wrap: typecheck TypeScript + verifica ACs + prompt push/PR con ticket ID
```

### `speckit.atom.context`

Comando standalone que el developer puede invocar al inicio de una sesión para refrescar el contexto de un task específico:

```
/speckit-atom-context CV-599
```

Hace:
1. `getJiraIssue` → extrae summary, ACs, HU padre
2. `getConfluencePage` → lee Spec Técnica (busca "Documento fuente" en la HU)
3. Figma node-id (si es `[FRONTEND]`) → metadata del frame
4. Escribe `.specify/memory/atom-context.md` con el contexto compilado
5. Reporta: `✓ Contexto de CV-599 cargado`

### Constitution (`memory/constitution.md`)

Pre-cargada con las reglas no negociables del codebase de Atom:

- **General:** reusar antes de crear, sin `any`, scope exacto, verificar al terminar
- **Frontend (Angular):** `OnPush`, `takeUntil(destroy$)`, `async` pipe, `trackBy`, sin strings hardcodeados, i18n consistente entre locales, no mutar `@Input()`, lazy loading
- **Backend (Cloud Functions):** Joi validations, una responsabilidad por función, errores tipados, compatibilidad con payloads legacy, límite Typesense ~100 unidades
- **Mobile (React Native):** limpiar `useEffect`, `useCallback`/`useMemo` donde aplique, no navegar desde UI components
- **CodeGraph:** correr `codegraph_search` + `codegraph_context` antes de escribir código nuevo; `codegraph_impact` antes de modificar un símbolo existente; no modificar directamente si blast radius > 3 lugares
- **Atlassian:** Cloud ID `atomchat.atlassian.net`; "Documento fuente" vive en el body de la HU, no en remote links

### Templates (append)

`spec-template.md` recibe secciones adicionales de Atom:
- Stack afectado (FE / BE / Mobile)
- Figma node-id por HU
- Contratos TypeScript (interfaces completas, no esqueletos)
- Blast radius de componentes tocados

`plan-template.md` recibe:
- Regla de concreción (la descripción nombra función/campo/valor — no "actualizar el servicio")
- Constraint de verificación por tarea (grep, test command, o aserción observable)
- Commit format: `<tipo>(<scope>): <descripción> [<TICKET-ID>]`

## Lo que no cambia

- La lógica de negocio de `ads:spec` y `ads:task` se preserva — pasa a vivir en los wraps del preset
- El flujo Jira-first (`ads:task CV-599`) sigue siendo el entry point principal, ahora como `/speckit-atom-context CV-599` + `/speckit-specify`
- El artefacto persistido entre sprints sigue siendo la Spec Técnica en Confluence — los archivos locales (SPEC.md, PLAN.md) son contexto adicional para el agente, no el source of truth

## Lo que se depreca

- `packages/cli/` como distribuidor de skills → reemplazado por `specify init --preset atom`
- `.claude-plugin/plugin.json` → el preset registra los skills directamente en `.claude/skills/`
- `skills/task/SKILL.md` y `skills/spec/SKILL.md` como skills standalone → su lógica vive en los wraps del preset

El CLI de ADS (`ads`) puede mantenerse como wrapper delgado:
```bash
ads install   →   specify init --preset atom --integration claude
ads update    →   specify preset update atom
```

## Repositorio

Nuevo repo: `atomchat/spec-kit-preset-atom` (público, para poder ser instalado via `specify preset add`)

```bash
specify preset add https://github.com/atomchat/spec-kit-preset-atom
```

## Criterios de aceptación

- [ ] `specify init --preset atom --integration claude` en un repo nuevo genera los skills en `.claude/skills/`
- [ ] `/speckit-atom-context CV-599` fetchea Jira + Confluence + Figma y escribe `atom-context.md`
- [ ] `/speckit-specify` incluye el contexto de Atom antes de ejecutar el core
- [ ] `/speckit-implement` corre typecheck TypeScript y verifica ACs al terminar
- [ ] La constitution aparece en `.specify/memory/constitution.md` con las reglas de Atom
- [ ] Los templates de spec y plan incluyen las secciones adicionales de Atom
- [ ] Un developer puede usar `/speckit-plan` y `/speckit-tasks` de spec-kit nativo sin fricción
- [ ] `ads install` sigue funcionando como alias del nuevo comando
