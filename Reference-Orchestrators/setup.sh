#!/usr/bin/env bash
# FITPAC Reference-Orchestrators setup script.
# Run from your project root. Copies the correct rule/orchestrator files for your IDE.
# Usage: ./setup.sh [path-to-Reference-Orchestrators]
#   If no path is given, uses the directory containing this script as the source.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE="${1:-$SCRIPT_DIR}"
TARGET="$(pwd)"
FORCE=""
if [[ "${1:-}" == "--force" ]]; then
  FORCE="y"
  SOURCE="${2:-$SCRIPT_DIR}"
fi
if [[ "${1:-}" == "--force" && -z "${2:-}" ]]; then
  SOURCE="$SCRIPT_DIR"
fi

if [[ ! -d "$SOURCE" ]]; then
  echo "Error: Source directory not found: $SOURCE"
  echo "Usage: $0 [--force] [path-to-Reference-Orchestrators]"
  exit 1
fi

confirm_overwrite() {
  if [[ -n "$FORCE" ]]; then
    return 0
  fi
  if [[ -e "$1" ]]; then
    echo -n "Overwrite $1? [y/N] "
    read -r ans
    [[ "$ans" == "y" || "$ans" == "Y" ]]
  else
    return 0
  fi
}

copy_safe() {
  local src="$1"
  local dst="$2"
  if [[ ! -e "$src" ]]; then
    echo "Error: Missing source $src"
    return 1
  fi
  mkdir -p "$(dirname "$dst")"
  if confirm_overwrite "$dst"; then
    cp -r "$src" "$dst"
    echo "  Copied: $dst"
  fi
}

echo "FITPAC orchestrator setup"
echo "  Source: $SOURCE"
echo "  Target (project root): $TARGET"
echo ""

if [[ "$SOURCE" == "$TARGET" ]]; then
  echo "Warning: Source and target are the same. Run this script from your project root with the path to Reference-Orchestrators, or run it from inside Reference-Orchestrators with target as parent."
  echo ""
fi

echo "Which IDE are you using?"
echo "  1) Cursor"
echo "  2) Windsurf"
echo "  3) VS Code (Continue / Claude)"
echo "  4) GitHub Copilot"
echo "  5) Roo Code"
echo "  6) Universal (show instructions only; no copy)"
echo -n "Choice [1-6]: "
read -r choice

case "$choice" in
  1)
    echo "Installing Cursor orchestrator..."
    copy_safe "$SOURCE/Cursor/.cursorrules" "$TARGET/.cursorrules"
    copy_safe "$SOURCE/Cursor/orchestrator" "$TARGET/orchestrator"
    if [[ -z "$FORCE" ]]; then
      echo -n "Install Cursor skill (optional)? [y/N] "
      read -r skill
      if [[ "$skill" == "y" || "$skill" == "Y" ]]; then
        mkdir -p "$TARGET/.cursor/skills"
        if [[ -d "$SOURCE/Cursor/.cursor/skills" ]]; then
          cp -r "$SOURCE/Cursor/.cursor/skills/"* "$TARGET/.cursor/skills/"
          echo "  Copied: .cursor/skills/"
        fi
      fi
    fi
    echo "Done. Open the project in Cursor."
    ;;
  2)
    echo "Installing Windsurf orchestrator..."
    copy_safe "$SOURCE/Windsurf/.windsurfrules" "$TARGET/.windsurfrules"
    copy_safe "$SOURCE/Windsurf/orchestrator" "$TARGET/orchestrator"
    echo "Done. Open the project in Windsurf."
    ;;
  3)
    echo "Installing VS Code orchestrator (Continue + Claude)..."
    copy_safe "$SOURCE/VSCode/.continue" "$TARGET/.continue"
    copy_safe "$SOURCE/VSCode/claude/CLAUDE.md" "$TARGET/CLAUDE.md"
    copy_safe "$SOURCE/VSCode/orchestrator" "$TARGET/orchestrator"
    echo "Done. Open the project in VS Code with Continue and/or Claude Code."
    ;;
  4)
    echo "Installing GitHub Copilot orchestrator..."
    mkdir -p "$TARGET/.github"
    copy_safe "$SOURCE/GitHub-Copilot/github/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"
    copy_safe "$SOURCE/GitHub-Copilot/orchestrator" "$TARGET/orchestrator"
    echo "Done. Use the project in a Copilot-enabled environment."
    ;;
  5)
    echo "Installing Roo Code orchestrator..."
    copy_safe "$SOURCE/Roo-Code/.clinerules" "$TARGET/.clinerules"
    copy_safe "$SOURCE/Roo-Code/orchestrator" "$TARGET/orchestrator"
    echo "Done. Open the project in VS Code with Roo Code."
    ;;
  6)
    echo ""
    echo "Universal: no files are copied. Copy the contents of this file into your AI's System Prompt or Custom Instructions:"
    echo "  $SOURCE/Universal/FITPAC_INSTRUCTIONS.md"
    echo ""
    if [[ -f "$SOURCE/Universal/FITPAC_INSTRUCTIONS.md" ]]; then
      echo "Path (absolute): $(cd "$SOURCE" && pwd)/Universal/FITPAC_INSTRUCTIONS.md"
    fi
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac
