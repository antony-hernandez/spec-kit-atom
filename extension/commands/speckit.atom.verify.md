---
description: "Typecheck de TypeScript + verificación de los criterios de aceptación contra la implementación"
---

# Atom Verify

Quality gate post-implement. Corre tras `/speckit.implement` (hook `after_implement`). No modifica código salvo para corregir lo que falla.

## Paso 1 — Typecheck

Buscar script `typecheck`, `build` o `compile` en `package.json` (raíz o `functions/` para Cloud Functions). Si no existe:

```bash
npx tsc --noEmit
```

Errores de tipos → corregir antes de continuar. Sin `any` para silenciar errores.

## Paso 2 — Verificación de ACs

Leer los criterios de aceptación de `.specify/memory/atom-context.md` (sección **Criterios de aceptación**). Si el archivo no existe, usar los ACs de `spec.md`.

Por cada AC, verificar la implementación goal-backward (chequeo de integración, no de tareas):

```
✅ AC-1: <descripción> — implementado en <archivo:línea>
⚠️ AC-2: <descripción> — parcial: falta <qué>
❌ AC-3: <descripción> — no implementado
```

⚠️ o ❌ → implementar lo que falta. No cerrar el gate hasta que todos sean ✅.

## Paso 3 — Reporte

```
Quality gate de Atom:
  Typecheck: ✓ | ✗ (corregido)
  ACs: N/N ✅
```
