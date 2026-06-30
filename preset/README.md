# Atom preset para spec-kit

Preset de [spec-kit](https://github.com/github/spec-kit) que dirige el flujo SDD con las reglas y el stack de Atom — sin repetir contexto en cada tarea.

Un **preset** solo overridea piezas core de spec-kit (no agrega comandos nuevos). Por eso esta pieza cubre el *steering*; la ingesta de Jira/Confluence/Figma vive en la extensión `atom` (fase 2).

## Qué incluye

| Pieza | Mecanismo | Qué hace |
|-------|-----------|----------|
| `constitution-template` | `replace` | Reemplaza el constitution core con las reglas no negociables de Atom (reuso/CodeGraph, sin `any`, scope exacto, escepticismo, verificación de ACs, reglas por stack) |
| `spec-template` | `append` | Agrega al spec las secciones de Atom: stack, Figma node-id, contratos TypeScript, blast radius |
| `plan-template` | `append` | Agrega al plan los constraints de Atom: regla de concreción, verificación por tarea, formato de commit, gate de CodeGraph |

## Instalación

Desde un proyecto con spec-kit inicializado:

```bash
# Desde el asset del release (manifest en la raíz del zip)
specify preset add atom --from https://github.com/antony-hernandez/spec-kit-atom/releases/latest/download/atom-preset.zip

# En desarrollo, desde una copia local (clon del repo)
specify preset add atom --dev ./preset
```

Verificá con `specify preset list`. Tras instalar, al correr `/speckit.constitution`, `/speckit.specify` y `/speckit.plan` el flujo ya sale con el contexto de Atom.

> No usar `--from <repo>/archive/...zip`: ese archive anida `preset.yml` bajo `preset/` y spec-kit no lo encuentra. Usar el asset del release (`atom-preset.zip`, con el manifest en la raíz) o `--dev`.

## Requisitos

- spec-kit `>=0.6.0`
