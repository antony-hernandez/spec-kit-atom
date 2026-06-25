---
description: "Atom-aware specify: loads Jira+Confluence context if a task ID is provided, then runs the core specify workflow"
argument-hint: "Jira task ID (e.g. CV-599) or feature description"
---

# Specify — Atom

## Pre-carga de contexto

Si `$ARGUMENTS` coincide con el patrón de un task ID de Jira (`[A-Z]+-\d+`, e.g. `CV-123`, `ATOM-456`):

1. Ejecutar `/speckit-atom-context $ARGUMENTS`
2. Esperar confirmación: `✓ Contexto de $ARGUMENTS cargado`
3. Leer `.specify/memory/atom-context.md` — el contexto ya está disponible para los pasos siguientes

Si `$ARGUMENTS` es una descripción libre (no un task ID):
- Continuar directamente al workflow de specify

---

{CORE_TEMPLATE}

---

## Secciones adicionales de Atom

Al generar el spec, asegurarse de incluir estas secciones además de las del template core:

**Stack afectado:** Frontend / Backend / Mobile (solo los que aplican, según atom-context.md)

**Figma:** node-id del frame específico de la HU (de atom-context.md), o `⚠️ ausente — confirmar con diseño`

**Contratos TypeScript:** interfaces completas — no esqueletos. Incluir campos existentes sin cambios + nuevos marcados.

**Blast radius:** para cada componente tocado, indicar cuántos lugares lo usan (de CodeGraph) y cómo aislarlo si es > 3.
