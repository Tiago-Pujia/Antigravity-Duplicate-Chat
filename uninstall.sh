#!/usr/bin/env bash
set -e

BIN_DIR="$HOME/.local/bin"
COMMAND_NAME="duplicate-chat-antigravity"
SYMLINK_PATH="$BIN_DIR/$COMMAND_NAME"

echo "=== Desinstalando Antigravity Duplicate Chat ==="

# Limpiar comando actual y legado si existe
rm -f "$BIN_DIR/duplicate-chat"

if [ -L "$SYMLINK_PATH" ] || [ -f "$SYMLINK_PATH" ]; then
    rm -f "$SYMLINK_PATH"
    echo "✅ Comando eliminado de $SYMLINK_PATH"
else
    echo "ℹ️  No se encontró el comando en $SYMLINK_PATH"
fi

echo "Desinstalación completa."
