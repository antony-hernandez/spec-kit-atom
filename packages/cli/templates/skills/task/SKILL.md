---
name: task
description: Use when starting work on any Jira task — before reading code, writing code, or asking the user for context.
---

# Task Discovery

Dado un ID de Jira (task o HU), arma el contexto completo antes de implementar. Sigue las fases en orden. No leer código ni preguntar al usuario hasta terminar el discovery.

## Fase 1 — Discovery (en paralelo donde sea posible)

**1. Task** — `getJiraIssue(cloudId: "atomchat.atlassian.net", issueIdOrKey, responseContentFormat: "markdown", fields: ["summary","description","parent","comment","issuetype"])`
- `[FRONTEND]` en summary → `TASK_TYPE = FE` / `[BACKEND]` → BE / ninguno → preguntar
- Sin criterios de aceptación → detenerse y exigirlos antes de continuar

**2. HU padre** — si `hierarchyLevel === -1`, fetch del `parent.key`. Buscar "Documento fuente" en body: `wiki/x/<tinyId>` o `wiki/spaces/.../pages/<id>`.

**3. Spec técnica** — `getConfluencePage` + footer comments + inline comments (en paralelo). Extraer cambios técnicos y criterios filtrados por `TASK_TYPE`. Buscar link a FRD en el body.

**4. FRD** (si existe) — `getConfluencePage` + comentarios. Identificar sección `### HU-XX` correspondiente. Extraer Figma node-id específico de esa sección (FE) y criterios funcionales.

## Fase 2 — Análisis

**5. Cross-check** — comparar criterios del FRD vs task/HU. Si hay mismatches → presentar al usuario y resolver antes de continuar. Si no → silencioso.

**6. Gate de reuso** — aplicar las reglas de `## Implementación` en CLAUDE.md. Resultados van en la sección REUSO del brief.

## Fase 3 — Brief e implementación

**7.** Compilar brief usando `brief-template.md`. Incluir sección REUSO.

**8.** STOP — presentar el brief completo y preguntar explícitamente: _"¿Algo que ajustar antes de empezar?"_ No continuar hasta recibir respuesta.

**9.** Implementar siguiendo estrictamente el brief y las reglas de CLAUDE.md.

## Errores comunes

| Error | Corrección |
|-------|------------|
| Tomar el Figma genérico del header del FRD | Buscar la sección `### HU-XX` y extraer el node-id de ahí |
| Mezclar cambios FE y BE en el mismo brief | Filtrar estrictamente por `TASK_TYPE` desde la Spec Técnica |
| Buscar "Documento fuente" en remote links de Jira | Está en el body de la HU — parsear el texto de `description` |
| Saltear el paso 8 si el brief quedó completo | El STOP es obligatorio siempre, independientemente de la calidad del brief |
| Subir directo a la Spec sin pasar por la HU | El link al spec vive en la HU, no en el task |

## Cuándo NO usar

- Si el brief de esta tarea ya está cargado en la sesión actual → no re-correr el skill, usarlo directamente.
