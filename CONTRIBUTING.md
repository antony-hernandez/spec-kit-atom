# Contributing

Este repo es un harness de [spec-kit](https://github.com/github/spec-kit) para Atom: un **preset** (fase 1) y, más adelante, una **extensión** y un **bundle**. Lo que aportamos vive encima de spec-kit — no forkeamos el core.

## Setup de desarrollo

```bash
git clone https://github.com/antony-hernandez/spec-kit-atom
cd spec-kit-atom
pipx install spec-kit          # el CLI `specify`
specify preset add atom --dev ./preset   # instala el preset desde la copia local
```

## Estructura

```
preset/
  preset.yml                   ← manifest del preset
  templates/
    constitution-template.md   ← reglas de Atom (override de constitution core)
    spec-template.md           ← secciones de Atom (append)
    plan-template.md           ← constraints de Atom (append)
extension/
  extension.yml                ← manifest (comandos + hooks)
  commands/                    ← speckit.atom.context / verify / pr
.planning/                     ← diseño, roadmap, spikes
CHANGELOG.md
```

## Reglas del modelo de spec-kit (no negociables al editar `preset.yml`)

- Un **preset solo overridea** templates/commands que ya existen en el core. **No agrega comandos nuevos** — eso es una extensión.
- Estrategias válidas: `replace` (default), `prepend`, `append`, `wrap` (`{CORE_TEMPLATE}` marca dónde va el contenido core).
- Templates core overrideables: `constitution-template`, `spec-template`, `plan-template`, `tasks-template`, `checklist-template`, `agent-file-template`.
- Las rutas `file:` son relativas a `preset.yml`.

## Modificar el preset

1. Editar el `template` correspondiente en `preset/templates/`.
2. Bump de `preset.version` en `preset.yml` (semver).
3. Entrada en `CHANGELOG.md`.
4. Probar: `specify preset add atom --dev ./preset` en un proyecto de prueba y verificar que el constitution / spec / plan salen con el contexto de Atom.

## Roadmap

- **Fase 1 — Preset** (actual): constitution + secciones en spec/plan.
- **Fase 2 — Extensión**: `speckit.atom.context` (ingesta Jira+Confluence+Figma) + hooks `after_implement` (typecheck, verificación de ACs, PR).
- **Fase 3 — Bundle**: `bundle.yml` que compone extensión + preset en un `specify bundle install`.

## Convención de commits

```
feat(scope):     nueva funcionalidad
fix(scope):      corrección de bug
docs(scope):     solo documentación
chore(scope):    mantenimiento
refactor(scope): refactor sin cambio de comportamiento
```

## Pull requests

- Un PR por cambio lógico.
- El título sigue la convención de commits.
- Incluir qué cambia y por qué.
