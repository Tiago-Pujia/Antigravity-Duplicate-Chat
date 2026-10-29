#!/usr/bin/env python3
"""
Antigravity Duplicate Chat
Herramienta de línea de comandos para ramificar y duplicar conversaciones
en Google Antigravity en tiempo real sin perder el contexto.
"""

import sys
import os
import re
import ssl
import json
import sqlite3
import urllib.request

BASE_DIR = os.path.expanduser("~/.gemini/antigravity")
SUMMARIES_DB = os.path.join(BASE_DIR, "conversation_summaries.db")
LS_LOG = os.path.expanduser("~/.config/Antigravity/logs/language_server.log")


def get_live_ls_info():
    """Detecta si language_server está corriendo y obtiene su puerto HTTPS y CSRF token."""
    csrf_token = None
    try:
        for pid in os.listdir("/proc"):
            if not pid.isdigit():
                continue
            cmdline_path = os.path.join("/proc", pid, "cmdline")
            if os.path.exists(cmdline_path):
                with open(cmdline_path, "rb") as f:
                    cmdline = f.read().decode("utf-8", errors="ignore")
                if "language_server" in cmdline and "--csrf_token" in cmdline:
                    m = re.search(
                        r"--csrf_token\x00([a-f0-9-]+)", cmdline
                    ) or re.search(r"--csrf_token\s+([a-f0-9-]+)", cmdline)
                    if m:
                        csrf_token = m.group(1)
                    break
    except Exception:
        pass

    if not csrf_token:
        return None, None

    port = None
    if os.path.exists(LS_LOG):
        with open(LS_LOG, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for line in reversed(lines):
            m = re.search(r"listening on random port at (\d+) for HTTPS", line)
            if m:
                port = int(m.group(1))
                break

    return port, csrf_token


def fork_via_api(source_id, new_title, port, csrf_token, step_count=71):
    """Invoca los endpoints Connect/gRPC en vivo de Antigravity."""
    ctx = ssl._create_unverified_context()
    headers = {
        "Content-Type": "application/json",
        "X-Codeium-Csrf-Token": csrf_token,
    }

    # 1. Fork conversation (clona historial y contexto)
    fork_url = f"https://127.0.0.1:{port}/exa.language_server_pb.LanguageServerService/ForkConversation"
    fork_data = json.dumps(
        {
            "source_cascade_id": source_id,
            "fork_at_step_index": max(0, step_count - 1),
        }
    ).encode("utf-8")

    req = urllib.request.Request(fork_url, data=fork_data, headers=headers)
    res = urllib.request.urlopen(req, timeout=10, context=ctx)
    res_json = json.loads(res.read().decode("utf-8"))
    new_cascade_id = res_json.get("newCascadeId")

    if not new_cascade_id:
        raise Exception(f"No se recibió newCascadeId en la respuesta: {res_json}")

    # 2. Update conversation title (asigna el nombre personalizado)
    annot_url = f"https://127.0.0.1:{port}/exa.language_server_pb.LanguageServerService/UpdateConversationAnnotations"
    annot_data = json.dumps(
        {
            "cascade_id": new_cascade_id,
            "cascade_ids": [new_cascade_id],
            "annotations": {"title": new_title},
            "merge_annotations": True,
        }
    ).encode("utf-8")

    req_annot = urllib.request.Request(annot_url, data=annot_data, headers=headers)
    urllib.request.urlopen(req_annot, timeout=10, context=ctx)

    return new_cascade_id


def list_conversations():
    """Muestra la lista de chats registrados en la base de datos de Antigravity."""
    if not os.path.exists(SUMMARIES_DB):
        print("❌ No se encontró la base de datos de chats de Antigravity.")
        return
    con = sqlite3.connect(SUMMARIES_DB)
    rows = con.execute(
        "SELECT title, conversation_id FROM conversation_summaries ORDER BY last_modified_time DESC"
    ).fetchall()
    con.close()

    print("\n📋 Chats disponibles para duplicar:")
    for title, _ in rows:
        display_title = title if title.strip() else "(Sin título)"
        print(f"  • \"{display_title}\"")
    print()


def print_help():
    print("""
Antigravity Duplicate Chat
==========================
Herramienta CLI para ramificar y clonar chats de Google Antigravity en vivo.

Uso:
  duplicate-chat [OPCIONES] "<Nombre del Chat>" ["<Nombre de la Copia>"]

Opciones:
  -l, --list    Muestra todos los chats disponibles en Antigravity.
  -h, --help    Muestra esta ayuda.

Ejemplos:
  1) Duplicar con sufijo '(Copia)':
     duplicate-chat "Leer Contidos De Carpeta"

  2) Duplicar asignando un título nuevo:
     duplicate-chat "Leer Contidos De Carpeta" "Estudio - Modulo 2"

  3) Listar chats disponibles:
     duplicate-chat --list
""")


def duplicate_conversation(source_id_or_title, custom_new_title=None):
    if not os.path.exists(SUMMARIES_DB):
        print("❌ Error: No se encontró la base de datos de Antigravity.")
        return None

    con = sqlite3.connect(SUMMARIES_DB, timeout=30.0)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    row = cur.execute(
        "SELECT * FROM conversation_summaries WHERE conversation_id = ? OR title LIKE ? ORDER BY last_modified_time DESC LIMIT 1",
        (source_id_or_title, f"%{source_id_or_title}%"),
    ).fetchone()

    if not row:
        print(
            f"\n❌ Error: No se encontró ningún chat que coincida con '{source_id_or_title}'."
        )
        con.close()
        list_conversations()
        return None

    source_id = row["conversation_id"]
    source_title = row["title"]
    step_count = row["step_count"]
    con.close()

    new_title = custom_new_title or f"{source_title} (Copia)"

    print(f"\n🚀 Duplicando chat en Antigravity:")
    print(f"   • Original: \"{source_title}\"")
    print(f"   • Nueva:    \"{new_title}\"")

    port, csrf_token = get_live_ls_info()
    if not (port and csrf_token):
        print("\n❌ Error: Antigravity no parece estar en ejecución.")
        print("   Abre la aplicación Antigravity antes de ejecutar el comando.\n")
        return None

    try:
        new_id = fork_via_api(source_id, new_title, port, csrf_token, step_count)
        print(f"\n✅ ¡Listo! El chat ha sido duplicado con éxito.")
        print(f"   Ya aparece visible en tu barra lateral como \"{new_title}\".\n")
        return new_id
    except Exception as e:
        print(f"\n❌ Error al duplicar en vivo: {e}\n")
        return None


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print_help()
        sys.exit(0)
    if args[0] in ("-l", "--list"):
        list_conversations()
        sys.exit(0)

    target = args[0]
    custom_title = args[1] if len(args) > 1 else None
    duplicate_conversation(target, custom_title)
