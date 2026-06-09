#!/usr/bin/env node
/**
 * Atomic installer — copia skills, CLAUDE.md y configura MCPs
 * Uso: curl -fsSL https://raw.githubusercontent.com/antony-hernandez/atomic/main/packages/cli/src/install.mjs | node
 * o:  npx github:antony-hernandez/atomic
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve, dirname, join } from "path";
import { fileURLToPath } from "url";

const ROOT = process.cwd();
const RAW_BASE = "https://raw.githubusercontent.com/antony-hernandez/atomic/main/packages/cli/templates";

const green = (s) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s) => `\x1b[33m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;

console.log(bold("\n⚡ Atomic — Asistente de desarrollo de Atom\n"));

// Detectar si corremos desde stdin (curl | node) o desde un archivo real (npx)
let TEMPLATES = null;
try {
  const __dir = dirname(fileURLToPath(import.meta.url));
  const candidate = resolve(__dir, "../templates");
  if (existsSync(join(candidate, "skills/task/SKILL.md"))) {
    TEMPLATES = candidate;
  }
} catch {
  // import.meta.url no resuelve desde stdin — modo remoto
}

if (!TEMPLATES) {
  console.log("  (descargando templates desde GitHub)\n");
}

async function readTemplate(relativePath) {
  if (TEMPLATES) {
    return readFileSync(join(TEMPLATES, relativePath), "utf8");
  }
  const url = `${RAW_BASE}/${relativePath}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Error al descargar ${url}: HTTP ${res.status}`);
  return res.text();
}

async function install() {
  // 1. Crear directorios necesarios
  mkdirSync(join(ROOT, ".claude/skills/task"), { recursive: true });

  // 2. Copiar skills
  const skills = [
    ["skills/task/SKILL.md", ".claude/skills/task/SKILL.md"],
    ["skills/task/brief-template.md", ".claude/skills/task/brief-template.md"],
  ];
  for (const [src, dest] of skills) {
    const content = await readTemplate(src);
    writeFileSync(join(ROOT, dest), content);
    console.log(green(`  ✓ skill /task`), `→ ${dest}`);
  }

  // 3. Crear o actualizar CLAUDE.md
  const claudeMdPath = join(ROOT, "CLAUDE.md");
  const claudeMdContent = await readTemplate("CLAUDE.md");
  if (!existsSync(claudeMdPath)) {
    writeFileSync(claudeMdPath, claudeMdContent);
    console.log(green("  ✓ CLAUDE.md creado"));
  } else {
    console.log(yellow("  ~ CLAUDE.md ya existe — no sobreescrito"));
    console.log(`    Revisa el repo de Atomic para ver qué agregar manualmente.`);
  }

  // 4. Configurar MCPs en .claude/settings.json
  const settingsPath = join(ROOT, ".claude/settings.json");
  let settings = {};
  if (existsSync(settingsPath)) {
    try {
      settings = JSON.parse(readFileSync(settingsPath, "utf8"));
    } catch {
      // malformado — empezar limpio
    }
  }

  settings.mcpServers = settings.mcpServers ?? {};

  if (!settings.mcpServers.codegraph) {
    settings.mcpServers.codegraph = {
      command: "npx",
      args: ["-y", "@colbymchenry/codegraph@latest", "serve"],
      env: {}
    };
    console.log(green("  ✓ MCP CodeGraph configurado"));
  } else {
    console.log(yellow("  ~ MCP CodeGraph ya configurado"));
  }

  if (!settings.mcpServers["plugin:atlassian:atlassian"]) {
    console.log(yellow("  ! MCP Atlassian no detectado"));
    console.log("    Instálalo desde: claude.ai/settings → Integrations → Atlassian");
  }

  if (!settings.mcpServers["plugin:figma:figma"]) {
    console.log(yellow("  ! MCP Figma no detectado"));
    console.log("    Instálalo desde: claude.ai/settings → Integrations → Figma");
  }

  writeFileSync(settingsPath, JSON.stringify(settings, null, 2));

  console.log(bold("\n¡Listo! Atomic instalado.\n"));
  console.log("  Uso:");
  console.log("    /task CV-123    ← carga el brief completo de una tarea\n");
  console.log("  MCPs requeridos:");
  console.log("    ✓ CodeGraph (configurado)");
  console.log("    → Atlassian: claude.ai/settings → Integrations");
  console.log("    → Figma:     claude.ai/settings → Integrations\n");
}

install().catch((err) => {
  console.error(`\n  ✗ Error durante la instalación: ${err.message}\n`);
  process.exit(1);
});
