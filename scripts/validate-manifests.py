#!/usr/bin/env python3
"""Valida los manifests del preset y la extensión contra el modelo de spec-kit.

Chequea, sin instalar spec-kit:
  - YAML válido y campos requeridos
  - los `file:` referenciados existen
  - estrategias de preset válidas (replace/prepend/append/wrap)
  - nombres de comandos de extensión: ^speckit\\.<id>\\.<cmd>$ con <id> == extension.id
  - los hooks referencian comandos declarados por la extensión

Uso: python3 scripts/validate-manifests.py
Sale con código != 0 si algo no cierra.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("✗ falta PyYAML (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def require(cond: bool, msg: str) -> None:
    if not cond:
        err(msg)


def validate_preset(path: Path) -> None:
    if not path.exists():
        err(f"{path} no existe")
        return
    d = yaml.safe_load(path.read_text())
    base = path.parent
    require(d.get("schema_version") == "1.0", "preset: schema_version debe ser '1.0'")
    p = d.get("preset", {})
    for f in ("id", "name", "version", "description"):
        require(bool(p.get(f)), f"preset.{f} requerido")
    require(bool(d.get("requires", {}).get("speckit_version")), "preset.requires.speckit_version requerido")

    templates = d.get("provides", {}).get("templates", [])
    require(len(templates) > 0, "preset.provides.templates vacío")
    valid_strategies = {"replace", "prepend", "append", "wrap"}
    for t in templates:
        name = t.get("name", "<sin name>")
        require(t.get("type") in ("template", "command", "script"), f"preset: type inválido en {name}")
        f = t.get("file")
        require(bool(f), f"preset: falta file en {name}")
        if f:
            require((base / f).exists(), f"preset: file no existe → {f} (en {name})")
        strat = t.get("strategy", "replace")
        require(strat in valid_strategies, f"preset: strategy inválida '{strat}' en {name}")
        if strat == "wrap" and f and (base / f).exists():
            require("{CORE_TEMPLATE}" in (base / f).read_text(),
                    f"preset: wrap sin {{CORE_TEMPLATE}} en {f}")
    print(f"✓ preset.yml — {len(templates)} templates, files OK")


def validate_extension(path: Path) -> None:
    if not path.exists():
        err(f"{path} no existe")
        return
    d = yaml.safe_load(path.read_text())
    base = path.parent
    require(d.get("schema_version") == "1.0", "extension: schema_version debe ser '1.0'")
    e = d.get("extension", {})
    for f in ("id", "name", "version", "description", "author", "repository", "license"):
        require(bool(e.get(f)), f"extension.{f} requerido")
    ext_id = e.get("id", "")
    require(bool(d.get("requires", {}).get("speckit_version")), "extension.requires.speckit_version requerido")

    commands = d.get("provides", {}).get("commands", [])
    require(len(commands) >= 1, "extension.provides.commands necesita ≥1 comando")
    name_re = re.compile(r"^speckit\.[a-z0-9-]+\.[a-z0-9-]+$")
    declared = set()
    for c in commands:
        name = c.get("name", "<sin name>")
        declared.add(name)
        require(bool(name_re.match(name)), f"extension: nombre inválido '{name}' (regex)")
        parts = name.split(".")
        if len(parts) == 3:
            require(parts[1] == ext_id, f"extension: '{name}' — el segmento medio debe ser '{ext_id}'")
        f = c.get("file")
        require(bool(f), f"extension: falta file en {name}")
        if f:
            require((base / f).exists(), f"extension: file no existe → {f} (en {name})")

    # hooks → comandos declarados
    hooks = d.get("hooks", {}) or {}
    valid_events = {
        "before_specify", "after_specify", "before_plan", "after_plan",
        "before_tasks", "after_tasks", "before_implement", "after_implement",
        "before_analyze", "after_analyze", "before_checklist", "after_checklist",
        "before_clarify", "after_clarify", "before_constitution", "after_constitution",
        "before_taskstoissues", "after_taskstoissues",
    }
    for event, spec in hooks.items():
        require(event in valid_events, f"extension: hook event desconocido '{event}'")
        entries = spec if isinstance(spec, list) else [spec]
        for entry in entries:
            cmd = entry.get("command")
            require(cmd in declared, f"extension: hook '{event}' apunta a comando no declarado '{cmd}'")
    print(f"✓ extension.yml — {len(commands)} comandos, {len(hooks)} hooks, files OK")


def main() -> int:
    validate_preset(ROOT / "preset" / "preset.yml")
    validate_extension(ROOT / "extension" / "extension.yml")
    if errors:
        print("\n✗ Validación falló:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("\n✓ Todos los manifests válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
