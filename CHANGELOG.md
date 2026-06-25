# Changelog

Cambios de **spec-kit-atom**, el harness de spec-kit para Atom.
Formato: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versionado: [SemVer](https://semver.org/).

## Versioning conventions

### Repo (este CHANGELOG)
- **MAJOR** — cambio de arquitectura o breaking en cómo se instala/usa
- **MINOR** — fase/pieza nueva (preset, extensión, bundle), comando o template nuevo
- **PATCH** — fix o ajuste de wording en un manifest/template

### Componentes (`version` en `preset.yml` / `extension.yml`)
Cada pieza versiona su propio `version` con el mismo criterio semver.

---

## [1.0.0] — 2026-06-25

Primera versión. Atom como harness de spec-kit: dirige el flujo SDD con las reglas y la ingesta de contexto de Atom, montándose encima de spec-kit.

### Added
- **Preset `atom`** — `constitution-template` (replace) con las reglas no negociables del codebase de Atom (reuso/CodeGraph, sin `any`, scope exacto, escepticismo, verificación de ACs, reglas por stack Angular/Cloud Functions/React Native) + `spec-template`/`plan-template` (append) con las secciones de Atom (stack, Figma, contratos TypeScript, blast radius). Validado e2e con spec-kit v0.11.9.
- **Extensión `atom`** — comandos `speckit.atom.context` (ingesta Jira+Confluence+Figma → `.specify/memory/atom-context.md`), `speckit.atom.verify` (typecheck + verificación de ACs) y `speckit.atom.pr` (PR con `[TICKET-ID]`), enganchados con hooks `before_specify` y `after_implement`.
