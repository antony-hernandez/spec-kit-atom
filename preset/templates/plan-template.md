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
