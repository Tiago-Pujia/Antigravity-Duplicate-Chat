#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SCRIPT="$SCRIPT_DIR/duplicate_chat.py"
BIN_DIR="$HOME/.local/bin"
COMMAND_NAME="duplicate-chat-antigravity"
SYMLINK_PATH="$BIN_DIR/$COMMAND_NAME"

echo "=== Instalando Antigravity Duplicate Chat ==="

# 1. Asegurar permisos de ejecución en los scripts
chmod +x "$TARGET_SCRIPT" "$SCRIPT_DIR/uninstall.sh"

# 2. Crear ~/.local/bin si no existe
mkdir -p "$BIN_DIR"

# 3. Limpiar enlace anterior si existía
rm -f "$BIN_DIR/duplicate-chat"

# 4. Crear enlace simbólico
ln -sf "$TARGET_SCRIPT" "$SYMLINK_PATH"

echo "✅ Enlace creado exitosamente en: $SYMLINK_PATH -> $TARGET_SCRIPT"

# 5. Verificar PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  Aviso: $BIN_DIR no parece estar en tu variable PATH actual."
    echo "   Para usar el comando '$COMMAND_NAME' directamente, añade esto a tu ~/.bashrc o ~/.zshrc:"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
else
    echo "✅ El directorio $BIN_DIR está en tu PATH."
fi

echo ""
echo "🎉 ¡Instalación completa!"
echo "Prueba ejecutar:"
echo "   $COMMAND_NAME --help"
