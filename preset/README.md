# spec-kit-preset-atom

Preset de [spec-kit](https://github.com/github/spec-kit) para proyectos de Atom.

## Qué incluye

- **Constitution** con las reglas del codebase de Atom (Angular, TypeScript strict, CodeGraph, commit format)
- **`/speckit-atom-context <ID>`** — ingesta Jira + Confluence + Figma para un task específico
- **`/speckit-specify`** — wrap que precarga contexto de Jira si recibe un task ID
- **`/speckit-implement`** — wrap que agrega TypeScript check + verificación de ACs + push/PR

## Instalación

```bash
specify init --preset atom --integration claude
```

O si spec-kit ya está inicializado:

```bash
specify preset add https://github.com/atomchat/spec-kit-preset-atom
```

## Reemplaza

```bash
ads install  # ya no necesario
```
