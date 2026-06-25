# spec-kit-preset-atom — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear el preset `atom` para spec-kit que preinstala el contexto de Atom (reglas de codebase, integración Jira+Confluence+Figma, wraps de verify) para que el equipo no tenga que repetir contexto en cada tarea.

**Architecture:** Un preset de spec-kit (nuevo repo `spec-kit-preset-atom`) que al instalarse con `specify init --preset atom --integration claude` configura: constitution con las reglas del codebase, un comando `speckit.atom.context` que ingesta Jira+Confluence+Figma, y wraps de `speckit.specify` y `speckit.implement` que inyectan contexto de Atom antes y verificación después. El CLI de ADS pasa a ser un wrapper delgado sobre `specify init`.

**Tech Stack:** spec-kit ≥0.6.0, Claude Code skills (Markdown + YAML frontmatter), Atlassian MCP, Figma MCP, CodeGraph MCP, `gh` CLI, Node.js (install.mjs existente)

## Global Constraints

- spec-kit version requerida: `>=0.6.0`
- IDs de Jira siguen el patrón `/^[A-Z]+-\d+$/` (e.g. CV-123, ATOM-456)
- Atlassian Cloud ID: `atomchat.atlassian.net` — hardcodeado en constitution y commands
- Commit format en proyectos Atom: `<tipo>(<scope>): <descripción> [<TICKET-ID>]`
- Sin `any` en TypeScript — regla en constitution
- Todos los comandos del preset van en `commands/` con extensión `.md`
- El preset vive en `preset/` dentro del repo `atomic` durante desarrollo; luego se mueve a repo propio `spec-kit-preset-atom`

---

### Task 1: Bootstrap — estructura del preset y `preset.yml`

**Files:**
- Create: `preset/preset.yml`
- Create: `preset/commands/` (dir)
- Create: `preset/templates/` (dir)
- Create: `preset/memory/` (dir)
- Create: `preset/README.md`

**Interfaces:**
- Produces: manifest válido que `specify preset add` puede parsear

- [ ] **Step 1: Crear la estructura de directorios**

```bash
mkdir -p preset/commands preset/templates preset/memory
```

- [ ] **Step 2: Verificar que spec-kit está instalado**

```bash
specify --version
```

Si falla: `pip install spec-kit` o `pipx install spec-kit`

- [ ] **Step 3: Escribir `preset/preset.yml`**

```yaml
schema_version: "1.0"

preset:
  id: "atom"
  name: "Atom Developer Skills"
  version: "1.0.0"
  description: "Atom codebase context: Jira+Confluence+Figma ingestion, Angular/TypeScript rules, post-implement verification"
  author: "Atom Team"
  repository: "https://github.com/atomchat/spec-kit-preset-atom"
  license: "MIT"

requires:
  speckit_version: ">=0.6.0"

provides:
  templates:
    - type: "command"
      name: "speckit.atom.context"
      file: "commands/speckit.atom.context.md"
      description: "Fetch Jira+Confluence+Figma context for an Atom task"

    - type: "command"
      name: "speckit.specify"
      file: "commands/speckit.specify.md"
      description: "Atom-aware specify: loads Jira context if task ID is provided"
      strategy: "wrap"
      replaces: "speckit.specify"

    - type: "command"
      name: "speckit.implement"
      file: "commands/speckit.implement.md"
      description: "Atom-aware implement: TypeScript check + AC verify + push/PR after implementation"
      strategy: "wrap"
      replaces: "speckit.implement"

    - type: "template"
      name: "spec-template"
      file: "templates/spec-template.md"
      description: "Atom sections appended to spec template"
      strategy: "append"

    - type: "template"
      name: "plan-template"
      file: "templates/plan-template.md"
      description: "Atom sections appended to plan template"
      strategy: "append"

tags:
  - "atom"
  - "atlassian"
  - "angular"
  - "typescript"
  - "jira"
  - "confluence"
```

- [ ] **Step 4: Verificar que el YAML es válido**

```bash
python3 -c "import yaml; yaml.safe_load(open('preset/preset.yml'))" && echo "✓ YAML válido"
```

Esperado: `✓ YAML válido`

- [ ] **Step 5: Escribir `preset/README.md`**

```markdown
# spec-kit-preset-atom

Preset de [spec-kit](https://github.com/github/spec-kit) para proyectos de Atom.

## Qué incluye

- **Constitution** con las reglas del codebase de Atom (Angular, TypeScript strict, CodeGraph, commit format)
- **`/speckit-atom-context <ID>`** — ingesta Jira + Confluence + Figma para un task específico
- **`/speckit-specify`** — wrap que precarga contexto de Jira si recibe un task ID
- **`/speckit-implement`** — wrap que agrega TypeScript check + verificación de ACs + push/PR

## Instalación

\`\`\`bash
specify init --preset atom --integration claude
\`\`\`

O si spec-kit ya está inicializado:

\`\`\`bash
specify preset add https://github.com/atomchat/spec-kit-preset-atom
\`\`\`

## Reemplaza

\`\`\`bash
ads install  # ya no necesario
\`\`\`
```

- [ ] **Step 6: Commit**

```bash
git add preset/
git commit -m "feat(preset): bootstrap spec-kit-preset-atom structure"
```

---

### Task 2: `memory/constitution.md` — reglas del codebase de Atom

**Files:**
- Create: `preset/memory/constitution.md`

**Interfaces:**
- Produces: archivo que spec-kit copia a `.specify/memory/constitution.md` al instalar el preset; el agente lo lee en cada sesión

- [ ] **Step 1: Escribir `preset/memory/constitution.md`**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add preset/memory/constitution.md
git commit -m "feat(preset): add Atom constitution with codebase rules"
```

---

### Task 3: `commands/speckit.atom.context.md` — ingesta de contexto Jira+Confluence+Figma

**Files:**
- Create: `preset/commands/speckit.atom.context.md`

**Interfaces:**
- Consumes: `$ARGUMENTS` = Jira task ID (e.g. `CV-599`)
- Produces: `.specify/memory/atom-context.md` con contexto compilado del task

- [ ] **Step 1: Escribir `preset/commands/speckit.atom.context.md`**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add preset/commands/speckit.atom.context.md
git commit -m "feat(preset): add speckit.atom.context command"
```

---

### Task 4: `commands/speckit.specify.md` — wrap con contexto Atom

**Files:**
- Create: `preset/commands/speckit.specify.md`

**Interfaces:**
- Consumes: `$ARGUMENTS` = Jira task ID o descripción libre
- Produces: wrappea `speckit.specify` nativo inyectando contexto de Atom antes

- [ ] **Step 1: Escribir `preset/commands/speckit.specify.md`**

```markdown
---
description: "Atom-aware specify: loads Jira+Confluence context if a task ID is provided, then runs the core specify workflow"
argument-hint: "Jira task ID (e.g. CV-599) or feature description"
---

# Specify — Atom

## Pre-carga de contexto

Si `$ARGUMENTS` coincide con el patrón de un task ID de Jira (`[A-Z]+-\d+`, e.g. `CV-123`, `ATOM-456`):

1. Ejecutar `/speckit-atom-context $ARGUMENTS`
2. Esperar confirmación: `✓ Contexto de $ARGUMENTS cargado`
3. Leer `.specify/memory/atom-context.md` — el contexto ya está disponible para los pasos siguientes

Si `$ARGUMENTS` es una descripción libre (no un task ID):
- Continuar directamente al workflow de specify

---

{CORE_TEMPLATE}

---

## Secciones adicionales de Atom

Al generar el spec, asegurarse de incluir estas secciones además de las del template core:

**Stack afectado:** Frontend / Backend / Mobile (solo los que aplican, según atom-context.md)

**Figma:** node-id del frame específico de la HU (de atom-context.md), o `⚠️ ausente — confirmar con diseño`

**Contratos TypeScript:** interfaces completas — no esqueletos. Incluir campos existentes sin cambios + nuevos marcados.

**Blast radius:** para cada componente tocado, indicar cuántos lugares lo usan (de CodeGraph) y cómo aislarlo si es > 3.
```

- [ ] **Step 2: Commit**

```bash
git add preset/commands/speckit.specify.md
git commit -m "feat(preset): add speckit.specify wrap with Atom context pre-loading"
```

---

### Task 5: `commands/speckit.implement.md` — wrap con verificación post-implement

**Files:**
- Create: `preset/commands/speckit.implement.md`

**Interfaces:**
- Consumes: resultado del implement core + `.specify/memory/atom-context.md` (ACs originales)
- Produces: wrappea `speckit.implement` nativo agregando verificación al final

- [ ] **Step 1: Escribir `preset/commands/speckit.implement.md`**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add preset/commands/speckit.implement.md
git commit -m "feat(preset): add speckit.implement wrap with TypeScript check and AC verification"
```

---

### Task 6: `templates/spec-template.md` — secciones adicionales de Atom

**Files:**
- Create: `preset/templates/spec-template.md`

**Interfaces:**
- Produces: contenido que se **append** al final del spec-template core de spec-kit

- [ ] **Step 1: Escribir `preset/templates/spec-template.md`**

```markdown
---

## Contexto de Atom

> Esta sección es completada por el agente al correr `/speckit-atom-context` o `/speckit-specify <TICKET-ID>`.

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
```

- [ ] **Step 2: Commit**

```bash
git add preset/templates/spec-template.md
git commit -m "feat(preset): add Atom sections append to spec-template"
```

---

### Task 7: `templates/plan-template.md` — constraints de Atom para el plan

**Files:**
- Create: `preset/templates/plan-template.md`

**Interfaces:**
- Produces: contenido que se **append** al final del plan-template core de spec-kit

- [ ] **Step 1: Escribir `preset/templates/plan-template.md`**

```markdown
---

## Constraints de implementación de Atom

### Regla de concreción

Cada tarea nombra exactamente qué función, campo, o valor cambia. Nunca "actualizar el servicio" o "ajustar la lógica" — si no incluye un identificador concreto, no es suficiente.

✅ Correcto: `Agregar control 'dateRange' al FormGroup con Validators.required`
❌ Incorrecto: `Actualizar el formulario para soportar el nuevo campo`

### Verificación por tarea

Cada tarea incluye un criterio de verificación observable:
- Grep: `grep -r "dateRange" src/` → debe aparecer en los archivos modificados
- Test: `ng test --include=path/componente.spec.ts` → suite pasa
- Network: campo aparece en el payload del request (verificar en DevTools)

### Formato de commit

```
<tipo>(<scope>): <descripción> [<TICKET-ID>]
```

Tipos válidos: `feat`, `fix`, `refactor`, `test`, `style`, `docs`

Ejemplos:
- `feat(audience): add date-range condition [CV-599]`
- `fix(campaign): correct filter serialization [CV-612]`

Una tarea = un commit. Hacer commit antes de avanzar a la siguiente tarea.

### Gate de CodeGraph

Antes de cualquier archivo nuevo:
```
codegraph_search("<NombreExacto>")
```
Si existe → usar el existente. Si el resultado es > 3 usages → proponer `@Input()` nuevo o wrapper.
```

- [ ] **Step 2: Commit**

```bash
git add preset/templates/plan-template.md
git commit -m "feat(preset): add Atom constraints append to plan-template"
```

---

### Task 8: Smoke test local del preset

**Files:**
- No modifica archivos del preset — solo verifica la instalación

**Interfaces:**
- Consumes: preset completo de Tasks 1-7
- Produces: verificación de que `specify init --preset atom --integration claude` funciona

- [ ] **Step 1: Crear directorio de test**

```bash
mkdir /tmp/atom-preset-test && cd /tmp/atom-preset-test && git init && git commit --allow-empty -m "init"
```

- [ ] **Step 2: Inicializar spec-kit con el preset local**

```bash
specify init --here --preset /ruta/absoluta/al/preset --integration claude
```

Donde `/ruta/absoluta/al/preset` es el path completo a `preset/` en el repo `atomic`.

- [ ] **Step 3: Verificar archivos instalados**

```bash
# Constitution copiada
ls .specify/memory/constitution.md

# Commands registrados en Claude
ls .claude/skills/
# Esperado: speckit-atom-context/ speckit-specify/ speckit-implement/

# Templates actualizados
ls .specify/templates/
```

Todos deben existir. Si alguno falta, revisar el `preset.yml` de Task 1.

- [ ] **Step 4: Verificar contenido del skill atom-context**

```bash
head -5 .claude/skills/speckit-atom-context/SKILL.md
```

Esperado: frontmatter con `description: "Fetch Jira+Confluence+Figma context..."`

- [ ] **Step 5: Verificar que el wrap de specify incluye {CORE_TEMPLATE} resuelto**

```bash
grep -c "CORE_TEMPLATE" .claude/skills/speckit-specify/SKILL.md
```

Esperado: `0` — spec-kit reemplaza `{CORE_TEMPLATE}` con el contenido core al instalar

- [ ] **Step 6: Limpiar**

```bash
cd - && rm -rf /tmp/atom-preset-test
```

---

### Task 9: Actualizar `ads install` como wrapper del preset

**Files:**
- Modify: `packages/cli/src/install.mjs`

**Interfaces:**
- Consumes: `specify` CLI disponible en el sistema
- Produces: `ads install` ejecuta `specify init --preset atom --integration claude`

- [ ] **Step 1: Leer el estado actual de install.mjs**

```bash
wc -l packages/cli/src/install.mjs
head -20 packages/cli/src/install.mjs
```

- [ ] **Step 2: Reemplazar la lógica principal por el wrapper**

Al inicio de `install.mjs`, después de los imports y antes de la lógica actual, agregar:

```javascript
// Verificar si specify está disponible
import { execSync, spawnSync } from "child_process";

function specifyAvailable() {
  try {
    execSync("specify --version", { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

if (specifyAvailable()) {
  console.log(bold("⚡ Atom Developer Skills — usando spec-kit como base\n"));
  console.log("  Ejecutando: specify init --preset atom --integration claude\n");

  const result = spawnSync(
    "specify",
    ["init", "--here", "--preset", "atom", "--integration", "claude"],
    { stdio: "inherit" }
  );

  if (result.status !== 0) {
    console.error("\n❌ Error al inicializar el preset. Verificar que spec-kit está instalado:");
    console.error("   pip install spec-kit\n");
    process.exit(1);
  }

  console.log(green("\n✓ Atom Developer Skills instalado vía spec-kit\n"));
  process.exit(0);
}

// Fallback: flujo legacy si specify no está disponible
console.log(yellow("⚠️  spec-kit no encontrado — usando instalación legacy\n"));
console.log("   Para usar la versión completa: pip install spec-kit\n");
// ... resto del código existente continúa aquí sin cambios
```

- [ ] **Step 3: Verificar sintaxis**

```bash
node --input-type=module < packages/cli/src/install.mjs 2>&1 | head -5
```

Esperado: el script corre sin errores de sintaxis (va a fallar en runtime si no hay preset, eso es OK)

- [ ] **Step 4: Commit**

```bash
git add packages/cli/src/install.mjs
git commit -m "feat(cli): ads install now wraps specify init --preset atom with legacy fallback"
```

---

### Task 10: Mover el preset a su propio repo

**Files:**
- No modifica archivos — operación de git

**Interfaces:**
- Consumes: `preset/` completo y testeado de Tasks 1-7
- Produces: repo `atomchat/spec-kit-preset-atom` público con el preset listo para instalar

- [ ] **Step 1: Crear el repo en GitHub**

```bash
gh repo create atomchat/spec-kit-preset-atom --public --description "spec-kit preset for Atom projects"
```

- [ ] **Step 2: Inicializar el preset como repo independiente**

```bash
cd preset/
git init
git add .
git commit -m "feat: initial Atom preset for spec-kit"
git remote add origin https://github.com/atomchat/spec-kit-preset-atom.git
git push -u origin main
```

- [ ] **Step 3: Actualizar la URL del preset en README y preset.yml**

En `preset/preset.yml` y `preset/README.md` ya está `https://github.com/atomchat/spec-kit-preset-atom` — verificar que es la URL correcta del repo creado.

- [ ] **Step 4: Verificar instalación desde URL pública**

```bash
mkdir /tmp/verify-preset && cd /tmp/verify-preset && git init && git commit --allow-empty -m "init"
specify init --here --preset https://github.com/atomchat/spec-kit-preset-atom --integration claude
ls .claude/skills/
cd - && rm -rf /tmp/verify-preset
```

Esperado: mismos skills que en Task 8 Step 3.

- [ ] **Step 5: Actualizar `install.mjs` con URL del preset publicado**

En el bloque del Step 2 de Task 9, cambiar:
```javascript
["init", "--here", "--preset", "atom", "--integration", "claude"]
```
por (si spec-kit no detecta el preset por nombre automáticamente):
```javascript
["init", "--here", "--preset", "https://github.com/atomchat/spec-kit-preset-atom", "--integration", "claude"]
```

- [ ] **Step 6: Commit final en atomic**

```bash
git add packages/cli/src/install.mjs
git commit -m "feat(cli): point ads install to published spec-kit-preset-atom repo"
```
