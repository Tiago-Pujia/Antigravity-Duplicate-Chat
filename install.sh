#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SCRIPT="$SCRIPT_DIR/duplicate_chat.py"
BIN_DIR="$HOME/.local/bin"
SYMLINK_PATH="$BIN_DIR/duplicate-chat"

echo "=== Instalando Antigravity Duplicate Chat ==="

# 1. Asegurar permisos de ejecución en el script
chmod +x "$TARGET_SCRIPT"

# 2. Crear ~/.local/bin si no existe
mkdir -p "$BIN_DIR"

# 3. Crear enlace simbólico
ln -sf "$TARGET_SCRIPT" "$SYMLINK_PATH"

echo "✅ Enlace creado exitosamente en: $SYMLINK_PATH -> $TARGET_SCRIPT"

# 4. Verificar PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  Aviso: $BIN_DIR no parece estar en tu variable PATH actual."
    echo "   Para usar el comando 'duplicate-chat' directamente, añade esto a tu ~/.bashrc o ~/.zshrc:"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
else
    echo "✅ El directorio $BIN_DIR está en tu PATH."
fi

echo ""
echo "🎉 ¡Instalación completa!"
echo "Prueba ejecutar:"
echo "   duplicate-chat --help"
