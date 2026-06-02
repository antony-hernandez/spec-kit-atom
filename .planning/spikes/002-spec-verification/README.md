---
spike: "002"
name: spec-verification
type: standard
validates: "Dado un task de Jira y su spec técnica en Confluence, cuando el agente los compara durante el context gathering, entonces detecta mismatches confiablemente (criterios que el task omite, pasos faltantes, contradicciones entre fuentes)"
verdict: VALIDATED
related: ["001"]
tags: [verification, jira, confluence, cross-check, drift]
---

# Spike 002: spec-verification

## What This Validates

Dado un task real (`CV-452`) y su spec técnica en Confluence, cuando el agente lee ambas fuentes y las compara, entonces detecta discrepancias reales antes de implementar — sin falsos negativos en ítems críticos.

## Redefinición del problema

El spike originalmente apuntaba a "verificar implementación vs spec". Durante la sesión, el usuario aclaró el problema real:

> "la idea es no llamar a un skill para saber, si te dan una tarea para desarrollar vos haces eso automático… lo que sí debemos validar son mismatches de FRD vs las tareas, a veces pasa que se actualiza el FRD pero la tarea o la HU no"

El spike se reorientó a: **¿puede el agente detectar, dentro del flujo `/task`, que el task/HU está desincronizado con la spec?**

La verificación no es un comando separado — es una fase automática del context gathering, entre leer el último documento y compilar el brief.

## Approach

No se construyó código separado. El spike se ejecutó corriendo el pipeline completo de `/task` sobre `CV-452` con el Paso 4.5 (cross-check) recién agregado al skill.

## How to Run

```
/task CV-452
```

El Paso 4.5 del skill corre automáticamente y reporta mismatches antes de entregar el brief.

## Investigation Trail

### CV-452 — `[BACKEND] Agregar ConditionType SERVICE_STAGE`

Pipeline ejecutado:
- CV-452 (subtask) → CV-451 (HU padre) → Confluence `4291002451` (Spec Técnica)
- Sin FRD separado en esta HU
- Sin comentarios en ningún nivel

### Mismatches encontrados

**MISMATCH 1 — Trigger `onUpdateConversation`: paso faltante en el task**

| Fuente | Qué dice |
|--------|----------|
| Spec (`on-update.ts`) | 3 cambios: (1) declarar variable, (2) agregar al bloque Typesense L326-333, (3) agregar a `VerifyComplianceWithListConditionsUseCase` L358-370 |
| Task CV-452 | Solo 2 cambios: (1) declarar variable, (3) agregar a `VerifyComplianceWithListConditionsUseCase`. **El paso (2) no aparece.** |

Impacto real: si el dev sigue solo el task, `lastServiceStage` nunca actualiza el índice Typesense cuando cambia. Las estimaciones y búsquedas de esa condición quedan desactualizadas.

**MISMATCH 2 — Cambio Typesense schema: criterio sin tarea técnica**

La spec lista explícitamente el cambio en `conversations-search.service.ts` L203-226 con archivo y líneas. El task lo tiene como criterio de aceptación pero no como checkbox de tarea técnica. Un dev que trabaja por checkboxes puede asumir que alguien más lo cubre.

### Validación del Paso 4.5

El cross-check detectó ambos mismatches correctamente. No hubo falsos positivos (las 9 áreas restantes del task son consistentes con la spec). La interrupción antes del brief es el momento correcto — el dev necesita saber esto antes de arrancar.

## Results

**Veredicto: VALIDATED ✅**

### Qué funciona

- El agente detecta pasos faltantes en el task comparado con la spec (mismatch 1 — crítico)
- El agente detecta criterios sin tarea técnica asociada (mismatch 2 — menor)
- El cross-check no genera ruido cuando las fuentes son consistentes
- El momento de interrupción (después de leer todo, antes del brief) es correcto

### Lecciones para el skill `/task`

1. **El task puede estar desactualizado respecto a la spec** — especialmente en pasos técnicos dentro de un mismo ítem (el trigger tenía 3 sub-pasos, el task listaba 2)
2. **Criterios de aceptación sin tarea técnica son un riesgo** — pueden quedar sin implementar si el dev trabaja por checkboxes
3. **La spec técnica de Confluence es la fuente de verdad técnica** — el task es una copia resumida que puede derivar
4. **Sin FRD en esta HU** — el pipeline funciona igualmente; el cross-check opera sobre lo que hay (Spec vs task/HU)
