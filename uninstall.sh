#!/usr/bin/env bash
set -e

BIN_DIR="$HOME/.local/bin"
SYMLINK_PATH="$BIN_DIR/duplicate-chat"

echo "=== Desinstalando Antigravity Duplicate Chat ==="

if [ -L "$SYMLINK_PATH" ] || [ -f "$SYMLINK_PATH" ]; then
    rm -f "$SYMLINK_PATH"
    echo "✅ Comando eliminado de $SYMLINK_PATH"
else
    echo "ℹ️  No se encontró el comando en $SYMLINK_PATH"
fi

echo "Desinstalación completa."
