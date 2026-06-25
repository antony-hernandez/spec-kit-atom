---

## Contexto de Atom

> Completá esta sección con el contexto del task (Jira / Confluence / Figma) antes de implementar.

**Task ID:** <!-- e.g. CV-599 -->
**Task type:** <!-- Frontend | Backend | Mobile -->
**Rama:** <!-- e.g. CV-599/add-date-condition -->

**Stack afectado:** <!-- Frontend / Backend / Mobile — marcar los que aplican -->

**Figma:** <!-- node-id del frame específico de la HU, o "⚠️ ausente" -->

## Contratos TypeScript

<!-- Interfaces completas. Incluir campos existentes sin cambios + nuevos marcados como "NUEVO". -->

```typescript
// Extender — no crear tipos paralelos
export interface ExistingModel {
  existingField: string;   // sin cambios
  newField: string;        // NUEVO
}
```

## Blast radius

<!-- Para cada componente tocado, indicar uso y estrategia de aislamiento. -->

| Componente | Usado en N lugares | Estrategia |
|---|---|---|
| `ComponentName` | 2 | Modificar directo |
| `SharedComponent` | 5 | Nuevo `@Input()` |
