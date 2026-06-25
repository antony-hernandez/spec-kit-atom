---
description: "Atom-aware implement: runs core implementation, then TypeScript check, AC verification, and push/PR"
argument-hint: "Optional task filter or implementation guidance"
---

# Implement — Atom

{CORE_TEMPLATE}

---

## Verificación post-implementación de Atom

Ejecutar estos pasos **después** de que el implement core haya completado todas las tareas.

### 1. TypeScript check

```bash
npx tsc --noEmit
```

- Si hay errores de tipos → corregirlos antes de continuar. No omitir.
- Si no existe `tsconfig.json` en el proyecto → saltar este paso y anotarlo.

### 2. Verificación de criterios de aceptación

Leer los ACs de `.specify/memory/atom-context.md`. Para cada uno, verificar que la implementación lo cumple:

```
✅ AC-1: <descripción> — implementado en <archivo>:<línea>
⚠️ AC-2: <descripción> — parcial: falta <X>
❌ AC-3: <descripción> — no implementado
```

Cualquier ⚠️ o ❌ → implementar lo que falta antes de continuar.

### 3. Push

Preguntar: `"¿Hacemos push de '<rama-actual>'?"`

Si sí:
```bash
git push -u origin <rama-actual>
```

### 4. Pull Request

Preguntar: `"¿Abrimos un PR?"`

Si sí, crear PR con el ticket ID de `atom-context.md`:
```bash
gh pr create \
  --title "[<TICKET-ID>] <resumen del task>" \
  --body "$(cat <<'EOF'
## Cambios

<lista de cambios implementados>

## Criterios de aceptación

<checklist de ACs del task>

## Ticket

<link a Jira: https://atomchat.atlassian.net/browse/TICKET-ID>
EOF
)"
```
