# Atom — Reglas del codebase

Este documento define los principios no negociables para desarrollar en los repos de Atom. El agente los aplica en cada tarea sin que el developer los repita.

## General

- **Reusar antes de crear** — antes de proponer cualquier componente, servicio, util, o enum nuevo, correr `codegraph_search("<NombreExacto>")`. Si existe → usarlo.
- **Sin `any`** — tipado estricto siempre. Si el tipo no existe, crearlo.
- **Scope exacto** — implementar exactamente lo que dice el spec, ni más.
- **Verificar al terminar** — confrontar la implementación contra los criterios de aceptación ítem por ítem antes de reportar como completo.
- **Escepticismo por defecto** — quien documentó no conocía todas las implicaciones técnicas. Leer el spec con criterio propio, validar contra el codebase, reportar lo que no cierra.

## Atlassian

- Cloud ID: `atomchat.atlassian.net` — usar en todos los calls a Jira y Confluence
- El link al spec técnico ("Documento fuente") está en el **body de la HU**, no en remote links de Jira
- Los comentarios de Jira y Confluence son contexto crítico — siempre leerlos

## Frontend (Angular)

- Reusar componentes existentes — CodeGraph confirma qué hay antes de crear
- Sin strings hardcodeados — todo texto va en los archivos i18n correspondientes
- **i18n consistencia**: al modificar una clave en un locale, actualizar todos los locales
- Validators de Angular Reactive Forms (`Validators.max`, `Validators.required`) — no lógica custom en el template
- **Suscripciones**: siempre `takeUntil(this.destroy$)` + `Subject<void>` destruido en `ngOnDestroy`
- **@Inputs**: no mutar directamente — crear copia o emitir con `@Output()`
- **Change detection**: si el componente ya usa `OnPush`, mantenerlo — no bajar a `Default`
- **Tipos**: extender interfaces existentes con campos opcionales — no crear tipos paralelos
- **Templates**: `async` pipe para observables, `trackBy` en todo `*ngFor`
- **Módulos**: lazy loading por defecto en módulos nuevos
- **Accesibilidad**: `aria-label` en elementos interactivos sin texto visible
- **UI**: textos exactos de Figma (capitalización, puntuación incluida), reusar tokens del design system, no hardcodear colores ni tamaños

## Backend (Cloud Functions)

- Validaciones con Joi en `filter-condition-group-schema.validation.ts`
- Lógica de evaluación de condiciones en utils separados por tipo de condición
- Compatibilidad con payloads legacy siempre — no romper rehidratación existente
- Typesense: respetar límite de ~100 unidades de complejidad de filtro
- **Funciones**: una responsabilidad por función — no acumular lógica en el handler principal
- **Errores**: lanzar errores tipados, nunca retornar `null` silencioso ante fallo
- **Tipos**: compartir contratos TypeScript con el frontend via tipos en el body del request/response — no duplicar definiciones

## Mobile (React Native)

- Reusar componentes del design system antes de crear nuevos
- **Estado**: preferir estado local + Context sobre librerías globales salvo que el estado sea genuinamente compartido
- **Navegación**: no navegar directamente desde componentes de UI — usar callbacks o hooks de navegación
- **Suscripciones y listeners**: limpiar siempre en el return de `useEffect`
- **Performance**: `useCallback`/`useMemo` en componentes que se renderizan frecuentemente

## CodeGraph — gate obligatorio antes de escribir código

Para cada componente, servicio, enum, o mapper en el brief:

```
codegraph_search("<NombreExacto>")         # ¿ya existe?
codegraph_context(task: "<descripción>")   # ¿cómo funciona lo relacionado?
codegraph_impact("<NombreComponente>")     # ¿qué se rompe si lo modifico?
```

- Ningún código nuevo hasta que CodeGraph confirme que no existe
- Si el símbolo se usa en más de 3 lugares → no modificar directamente. Alternativas: `@Input()` nuevo, componente wrapper, clase CSS aditiva

## Commits

Formato obligatorio: `<tipo>(<scope>): <descripción> [<TICKET-ID>]`

Ejemplos:
- `feat(audience): add date-range condition type [CV-599]`
- `fix(campaign): correct Typesense filter limit [CV-612]`
- `refactor(condition-row): extract validation to util [CV-601]`

Una tarea = un commit. No acumular cambios de múltiples tareas.
