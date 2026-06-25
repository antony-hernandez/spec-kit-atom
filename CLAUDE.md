# spec-kit-atom — guía del repo

Este repo es un **harness de [spec-kit](https://github.com/github/spec-kit) para Atom**: dirige el flujo Spec-Driven Development con las reglas y el stack de Atom, montándose encima de spec-kit sin forkearlo. spec-kit es el core; acá solo vive lo propio de Atom.

> Las reglas del codebase de Atom (Angular, sin `any`, i18n, CodeGraph, commits) **no son reglas para trabajar en este repo** — son el *contenido* que el preset entrega, y viven en `preset/templates/constitution-template.md`. Este repo es YAML + Markdown, no tiene código Angular.

## Modelo de spec-kit — no negociable al editar manifests

Tres mecanismos con capacidades que NO se solapan. Confundirlos fue el error original (un preset no agrega comandos):

- **Preset** (`preset.yml`): SOLO overridea templates/commands core. Estrategias: `replace`, `prepend`, `append`, `wrap` (`{CORE_TEMPLATE}`). Constitution = override de `constitution-template`. NO agrega comandos.
- **Extensión** (`extension.yml`): agrega comandos nuevos `speckit.<id>.<cmd>` (segmento medio = `extension.id`), hooks de ciclo de vida (`before_specify`, `after_implement`…), config. NO overridea core.
- **Bundle** (`bundle.yml`): compone extensión + preset.
- Instalación: `specify preset add <id> --dev <path> | --from <zip>`; `specify extension add` ídem. `specify init --preset` toma ID de catálogo, no URL.

Antes de tocar `preset.yml`, verificar contra el repo real de spec-kit si hay dudas del schema — no asumir.

## Faseado

| Fase | Pieza | Estado |
|------|-------|--------|
| 1 | Preset `atom` — `constitution-template` (replace) + `spec`/`plan-template` (append) | ✅ en `preset/`, validado e2e |
| 2 | Extensión `atom` — `speckit.atom.context` (ingesta Jira+Confluence+Figma) + hooks de quality gate | ⏳ |
| 3 | Bundle `atom` — une extensión + preset | ⏳ |

Diseño completo: `.planning/designs/spec-kit-atom.md`.

## Estructura

```
preset/                          fase 1 (manifest + templates)
skills/                          legacy/stopgap: ads:task, ads:spec — prototipo de la ingesta fase 2
.planning/designs/               diseño corregido al modelo real de spec-kit
```

`skills/` se mantiene como stopgap de ingesta Jira y referencia para construir la extensión; no es código a integrar en el harness.

## Convenciones

- Atlassian Cloud ID: `atomchat.atlassian.net`. El link al spec ("Documento fuente") vive en el body de la HU, no en remote links.
- Commits: `<tipo>(<scope>): <descripción>`. Un cambio lógico por commit.
- Editar el preset → bump `preset.version` + entrada en `CHANGELOG.md`.
- No reintroducir el CLI npm (`packages/cli`, `package.json`): la instalación es vía `specify`.
