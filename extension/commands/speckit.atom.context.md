---
description: "Fetch Jira+Confluence+Figma para un task de Atom y escribir el contexto en .specify/memory/atom-context.md"
---

# Atom Context

Dado un task ID de Jira, compila el contexto de implementación y lo escribe en `.specify/memory/atom-context.md` para que `/speckit.specify` y `/speckit.plan` lo consuman.

## User Input

```text
$ARGUMENTS
```

`$ARGUMENTS` es el task ID de Jira (e.g. `CV-599`). Si está vacío → pedirlo y detener.

## Pre-flight

Llamar `atlassianUserInfo()`. Si falla, mostrar y **detener**:

```
❌ Atlassian MCP no conectado.
1. Abrí claude.ai/settings → Integrations
2. Conectá "Atlassian" con tu cuenta de Atom
3. Reiniciá esta sesión
```

## Paso 1 — Task de Jira

```
getJiraIssue(
  cloudId: "atomchat.atlassian.net",
  issueIdOrKey: "$ARGUMENTS",
  responseContentFormat: "markdown",
  fields: ["summary","description","parent","comment","issuetype"]
)
```

- `[FRONTEND]` en summary → `TASK_TYPE = FE`; `[BACKEND]` → `BE`; sin prefijo → preguntar.
- Sin criterios de aceptación → **STOP**: "Este task no tiene ACs. Agregarlos en Jira antes de continuar."
- Leer **todos** los comentarios — son contexto crítico.

## Paso 2 — HU padre y Documento fuente

Si es subtask (`hierarchyLevel === -1`), fetch del `parent.key`. En el **body de la HU** (no en remote links) buscar "Documento fuente":
- `wiki/x/<tinyId>` → usar tinyId como pageId
- `wiki/spaces/.../pages/<id>` → usar el número como pageId

## Paso 3 — Spec Técnica (Confluence)

```
getConfluencePage(cloudId: "atomchat.atlassian.net", pageId: <id>)
getConfluencePageFooterComments(cloudId: "atomchat.atlassian.net", pageId: <id>)
getConfluencePageInlineComments(cloudId: "atomchat.atlassian.net", pageId: <id>)
```

Extraer archivos a modificar, contratos TypeScript y criterios técnicos. Buscar link al FRD en el body.

## Paso 4 — Figma (solo si TASK_TYPE = FE)

En el FRD, ubicar la sección `### HU-XX` de la HU padre y extraer el **node-id específico de esa sección** (no el genérico del header). Si no hay node-id → anotar `⚠️ Figma ausente`.

## Paso 5 — Escribir `.specify/memory/atom-context.md`

Crear o sobreescribir con este formato:

```markdown
# Atom Context — $ARGUMENTS

**Task type:** FE | BE
**Rama sugerida:** $ARGUMENTS/<descripción-corta>

## Task
**Summary:** <summary>
**Criterios de aceptación:**
- [ ] <AC 1>
- [ ] <AC 2>

## Spec Técnica
**Archivos a modificar:** <lista de la spec>
**Contratos TypeScript:** <interfaces de la spec>
**Criterios técnicos:** <de la spec>

## Figma
<node-id con link, o "⚠️ ausente">

## Decisiones de comentarios
<decisiones relevantes de comentarios de Jira/Confluence que no están en el body>
```

Reportar: `✓ Contexto de $ARGUMENTS cargado en .specify/memory/atom-context.md`. No implementar — eso es trabajo de `/speckit.specify` → `/speckit.plan` → `/speckit.implement`.
