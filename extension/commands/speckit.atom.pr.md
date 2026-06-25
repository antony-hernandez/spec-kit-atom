---
description: "Crear el PR del feature con título [TICKET-ID] y checklist de ACs"
---

# Atom PR

Crea el PR del feature. Corre tras la verificación (hook `after_implement`, opcional). Confirmar antes de acciones outward-facing.

## Paso 1 — Estado git

```bash
git status && git branch --show-current
```

- Cambios sin commitear → preguntar si commitear primero (formato `<tipo>(<scope>): <descripción> [<TICKET-ID>]`).
- En rama principal → **STOP**: proponer crear `<TICKET-ID>/<descripción>` antes de seguir.

## Paso 2 — Push

```bash
git push -u origin <rama>
```

## Paso 3 — PR

Tomar el `TICKET-ID` y los ACs de `.specify/memory/atom-context.md`. Crear:

```bash
gh pr create \
  --title "[<TICKET-ID>] <resumen>" \
  --body "<cambios del feature>

## Criterios de aceptación
- [x] <AC 1>
- [x] <AC 2>

Ticket: https://atomchat.atlassian.net/browse/<TICKET-ID>"
```

Reportar la URL del PR.
