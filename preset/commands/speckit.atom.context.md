---
description: "Fetch Jira+Confluence+Figma context for an Atom task and write to .specify/memory/atom-context.md"
argument-hint: "Jira task ID (e.g. CV-599)"
---

# Atom Context

Dado el task ID `$ARGUMENTS`, compila el contexto completo de implementación y lo escribe en `.specify/memory/atom-context.md`.

## Pre-flight

Llamar `atlassianUserInfo()`. Si falla, mostrar:

```
❌ Atlassian MCP no conectado.
1. Abrí claude.ai/settings → Integrations
2. Conectá "Atlassian" con tu cuenta de Atom
3. Reiniciá esta sesión
```

Y detener.

## Paso 1 — Fetch del task

```
getJiraIssue(
  cloudId: "atomchat.atlassian.net",
  issueIdOrKey: "$ARGUMENTS",
  responseContentFormat: "markdown",
  fields: ["summary","description","parent","comment","issuetype"]
)
```

- `[FRONTEND]` en summary → `TASK_TYPE = FE`
- `[BACKEND]` en summary → `TASK_TYPE = BE`
- Sin prefijo → preguntar al usuario antes de continuar
- Sin criterios de aceptación → **STOP**: "Este task no tiene ACs. Agregarlos en Jira antes de continuar."

## Paso 2 — Fetch de la HU padre

Si `hierarchyLevel === -1` (es subtask), fetch del `parent.key`:

```
getJiraIssue(cloudId: "atomchat.atlassian.net", issueIdOrKey: parent.key, ...)
```

Buscar "Documento fuente" en el body de la HU. Patrones:
- `Documento fuente: <url>`
- `## Confluence\n<url>`
- `wiki/x/<tinyId>` → usar tinyId como pageId
- `wiki/spaces/.../pages/<id>` → usar el número como pageId

## Paso 3 — Fetch de la Spec Técnica

```
getConfluencePage(cloudId: "atomchat.atlassian.net", pageId: <id>)
getConfluencePageFooterComments(cloudId: "atomchat.atlassian.net", pageId: <id>)
getConfluencePageInlineComments(cloudId: "atomchat.atlassian.net", pageId: <id>)
```

Extraer: archivos a modificar, contratos TypeScript, criterios técnicos.

## Paso 4 — Figma (solo si TASK_TYPE = FE)

Buscar en el FRD (si existe link en la Spec Técnica) la sección `### HU-XX` correspondiente a la HU padre. Extraer el node-id de Figma de esa sección específica.

Si no hay node-id → anotar `⚠️ Figma ausente`.

## Paso 5 — Escribir `.specify/memory/atom-context.md`

Crear o sobreescribir el archivo con este formato:

```markdown
# Atom Context — $ARGUMENTS

**Generado:** <fecha>
**Task type:** FE | BE
**Rama sugerida:** $ARGUMENTS/descripcion-corta

## Task

**Summary:** <summary del task>
**ACs:**
- [ ] <AC 1>
- [ ] <AC 2>

## HU padre

**Key:** <HU key>
**Summary:** <summary>

## Spec Técnica

<contenido relevante de la Spec Técnica — archivos a modificar, contratos TypeScript, criterios técnicos>

## Figma

**Node-id:** <node-id> | ⚠️ ausente

## Gaps detectados

<❓ Bloqueantes y ⚠️ Asumidos encontrados durante la lectura>
```

## Resultado

Reportar:
```
✓ Contexto de $ARGUMENTS cargado en .specify/memory/atom-context.md
  Task type: FE | BE
  ACs: N criterios
  Spec Técnica: ✓ | ⚠️ ausente
  Figma: ✓ <node-id> | ⚠️ ausente
```
