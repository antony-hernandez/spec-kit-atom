# Atom Constitution

Principios no negociables para desarrollar en los repos de Atom. Spec-kit lee este documento en cada sesión; el agente los aplica sin que el developer los repita.

## Core Principles

### I. Reuso antes de creación (NON-NEGOTIABLE)
Antes de proponer cualquier componente, servicio, util, enum o mapper nuevo, verificar que no exista: `codegraph_search("<NombreExacto>")`. Si existe → usarlo. Si un símbolo se usa en más de 3 lugares, no modificarlo directo — `@Input()` nuevo, wrapper, o clase CSS aditiva. Ningún código nuevo hasta que CodeGraph confirme que no hay algo que ya resuelva el problema.

### II. Tipado estricto
Sin `any`. Si el tipo no existe, crearlo. Extender interfaces existentes con campos opcionales — nunca tipos paralelos para el mismo concepto. Los contratos TypeScript que cruzan la frontera FE↔BE se comparten vía el body del request/response, no se duplican.

### III. Scope exacto
Implementar exactamente lo que pide el spec — ni más, ni menos. No agregar features no pedidas aunque parezcan obvias o necesarias.

### IV. Escepticismo documental
Asumir que quien documentó no conocía todas las implicaciones técnicas. El spec describe el qué desde afuera, no el cómo desde adentro. Leer con criterio propio, validar contra el codebase, y reportar lo que no cierra antes de escribir una línea — en vez de transcribir literalmente.

### V. Verificación contra criterios de aceptación
Antes de reportar una tarea como completa, confrontar la implementación contra cada criterio de aceptación, ítem por ítem. ⚠️ o ❌ → implementar lo que falta. No cerrar hasta que todos sean ✅.

## Reglas por stack

### Frontend (Angular)
- Sin strings hardcodeados — todo texto va en los archivos i18n. Al modificar una clave en un locale, actualizar todos: capitalización, puntuación y formato consistentes.
- Validators de Angular Reactive Forms (`Validators.required`, `Validators.max`) — no lógica de validación custom en el template.
- Suscripciones: `takeUntil(this.destroy$)` + `Subject<void>` destruido en `ngOnDestroy`.
- `@Input()`: no mutar directamente — copiar o emitir con `@Output()`.
- Mantener `OnPush` si el componente ya lo usa — no bajar a `Default`.
- Templates: `async` pipe para observables, `trackBy` en todo `*ngFor`. Lazy loading por defecto en módulos nuevos.
- UI: textos exactos de Figma (capitalización y puntuación incluidas), tokens del design system — no hardcodear colores ni tamaños. `aria-label` en interactivos sin texto visible.
- Discrepancias Figma/spec: reportar antes de implementar, no resolver por cuenta propia.

### Backend (Cloud Functions)
- Validaciones con Joi en `filter-condition-group-schema.validation.ts`. Lógica de evaluación en utils separados por tipo de condición.
- Compatibilidad con payloads legacy siempre — no romper rehidratación existente.
- Typesense: respetar el límite de ~100 unidades de complejidad de filtro.
- Una responsabilidad por función — no acumular lógica en el handler principal.
- Errores tipados — nunca retornar `null` silencioso ante fallo.

### Mobile (React Native)
- Reusar componentes del design system antes de crear nuevos.
- Estado local + Context sobre librerías globales, salvo que el estado sea genuinamente compartido.
- No navegar directamente desde componentes de UI — callbacks hacia arriba o hooks de navegación.
- Limpiar suscripciones y listeners en el return de `useEffect`.
- `useCallback`/`useMemo` en componentes que se renderizan con frecuencia — evitar funciones y objetos inline en JSX.

## Workflow y Quality Gates

### Atlassian
- Cloud ID: `atomchat.atlassian.net` en todos los calls a Jira y Confluence.
- El link al spec técnico ("Documento fuente") vive en el **body de la HU**, no en los remote links de Jira.
- Los comentarios de Jira y Confluence son contexto crítico — leerlos siempre.

### CodeGraph — gate antes de escribir código
```
codegraph_search("<NombreExacto>")         # ¿ya existe?
codegraph_context(task: "<descripción>")   # ¿cómo funciona lo relacionado?
codegraph_impact("<NombreComponente>")     # ¿qué se rompe si lo modifico?
```

### Commits
Formato obligatorio: `<tipo>(<scope>): <descripción> [<TICKET-ID>]`. Tipos: `feat`, `fix`, `refactor`, `test`, `style`, `docs`. Una tarea = un commit.

## Governance
Esta constitución supera cualquier práctica ad-hoc. Toda revisión de PR verifica el cumplimiento de estos principios. Cualquier complejidad que los contradiga debe justificarse explícitamente; ante ambigüedad en el spec, preguntar antes de asumir.

**Version**: 1.0.0 | **Ratified**: 2026-06-25 | **Last Amended**: 2026-06-25
