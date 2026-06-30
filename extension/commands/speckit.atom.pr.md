---
description: "Crear el PR del feature con título [TICKET-ID] y checklist de ACs (GitHub o Bitbucket)"
---

# Atom PR

Crea el PR del feature. Corre tras la verificación (hook `after_implement`, opcional). Confirmar antes de acciones outward-facing.

## Paso 1 — Estado git y rama

```bash
git status && git branch --show-current
```

- Cambios sin commitear → preguntar si commitear primero (formato `<tipo>(<scope>): <descripción> [<TICKET-ID>]`).
- En rama principal → **STOP**: la rama del ticket suele existir ya en remote. `git fetch` y buscar `git branch -r | grep <TICKET-ID>`; usar esa (convención Atom: `feature/<TICKET-ID>-<descripción>`). No inventar nombre/base.

## Paso 2 — Push

```bash
git push -u origin <rama>
```

## Paso 3 — Detectar el host del remote

```bash
git remote get-url origin
```

- `github.com` → GitHub (Paso 4a).
- `bitbucket.org` → Bitbucket (Paso 4b). **Atom usa Bitbucket.**

El título y body salen de `.specify/memory/atom-context.md` (TICKET-ID + ACs). Body sugerido: Contexto · Qué se hizo · Fuera de alcance · checklist de ACs (honesto: marcar solo los verificados) · Cómo probar · Notas.

### Paso 4a — GitHub

```bash
gh pr create --title "[<TICKET-ID>] <resumen>" --body "<body>"
```

### Paso 4b — Bitbucket

`gh` **no** aplica. SSH autentica git, no la API REST — la PR necesita un **app password** (scope *Pull requests: Write*, en bitbucket.org/account/settings/app-passwords).

Si hay `BB_USER` + `BB_APP_PASSWORD` en el entorno → crear vía API (POST a `…/repositories/<ws>/<repo>/pullrequests` con `source`, `destination: master`, `description`; si ya existe PR abierta para la rama → PUT para actualizar la descripción).

Si no hay credenciales → **no bloquear**: escribir el body a un archivo y dar al usuario el link de creación que devuelve el `git push` (`…/pull-requests/new?source=<rama>&dest=master`) para pegarlo. No asumir que se pudo crear.

Reportar la URL del PR (o el link de creación si quedó manual).
