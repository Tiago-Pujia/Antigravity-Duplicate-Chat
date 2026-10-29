# Antigravity Duplicate Chat 🚀

> Herramienta CLI para duplicar y ramificar (*fork*) conversaciones de **Google Antigravity** en vivo sin perder contexto ni tener que solicitarle al asistente que vuelva a leer todos los contenidos del proyecto.

---

## 🎯 ¿Qué problema resuelve?

En **Google Antigravity**, cuando se trabaja con proyectos grandes (código, apuntes, libros o guías de estudio), el primer mensaje suele dedicarse a que el agente lea e indexe carpetas enteras.

La interfaz gráfica de Antigravity **no incluye actualmente un botón nativo para duplicar o clonar un chat**. Si quieres comenzar una consulta nueva sobre otro tema manteniendo todo el material leído, normalmente tendrías que:
1. Seguir en el mismo chat (mezclando temas y alargando excesivamente el historial).
2. Abrir un chat nuevo y pedirle que vuelva a escanear toda la carpeta desde cero (lento y con alto consumo de tokens).

**`duplicate-chat`** soluciona esto permitiéndote clonar cualquier conversación existente al instante. El nuevo chat ramificado aparece en tu barra lateral manteniendo intactos todos los pasos previos, conclusiones y archivos analizados.

---

## ⚙️ ¿Cómo funciona por detrás?

1. **Detección dinámica:** El script localiza el proceso activo del motor de Antigravity (`language_server`) y extrae dinámicamente su puerto HTTPS local y el token de seguridad CSRF (`X-Codeium-Csrf-Token`).
2. **Llamada RPC nativa (`ForkConversation`):** Se comunica con el endpoint gRPC/Connect interno de Antigravity (`/exa.language_server_pb.LanguageServerService/ForkConversation`), el mismo mecanismo que utiliza internamente la plataforma para ramificar agentes y tareas.
3. **Actualización de metadatos (`UpdateConversationAnnotations`):** Le asigna el título deseado de forma limpia en el registro de sesiones.
4. **Reflejo en vivo:** Al interactuar con el servicio en memoria y no solo con los archivos SQLite en disco, el nuevo chat aparece **al instante en la barra lateral**, sin necesidad de reiniciar la app ni recargarla con atajos.

---

## 📦 Instalación

Solo clona o navega a este repositorio y ejecuta el script de instalación:

```bash
cd /home/tiago/Proyectos/Antigravity-Duplicate-Chat
./install.sh
```

El script de instalación:
1. Da permisos de ejecución al script Python.
2. Crea un enlace simbólico en `~/.local/bin/duplicate-chat`.
3. Te asegura disponibilidad global del comando en cualquier terminal de tu sistema.

---

## 💡 Guía de Uso

### 1. Duplicar con nombre automático `(Copia)`
Pasa el nombre o parte del nombre del chat que quieres duplicar:

```bash
duplicate-chat "Leer Contidos De Carpeta"
```

Aparecerá inmediatamente en tu barra lateral:
```text
📁 Estadistica Aplicada
  ├── Leer Contidos De Carpeta (Copia)  <-- (Nuevo chat duplicado)
  └── Leer Contidos De Carpeta
```

### 2. Duplicar asignando un nombre personalizado
Puedes especificar un segundo argumento entre comillas con el nuevo título:

```bash
duplicate-chat "Leer Contidos De Carpeta" "Estudio - Modulo 2 ANOVA"
```

### 3. Listar todos los chats disponibles
Si no recuerdas cómo se llamaba exactamente un chat, puedes listar todos los chats registrados:

```bash
duplicate-chat --list
# o también:
duplicate-chat -l
```

### 4. Ver ayuda en la terminal
```bash
duplicate-chat --help
```

---

## 🛠️ Requisitos

* **Sistema Operativo:** Linux
* **Python:** 3.8 o superior (utiliza solo bibliotecas estándar: `urllib`, `sqlite3`, `ssl`, `json`, `re`)
* **Google Antigravity:** Debe estar abierto y en ejecución al momento de invocar el comando para que pueda conectarse a su API en vivo.

---

## 🗑️ Desinstalación

Si deseas remover el comando del sistema:

```bash
./uninstall.sh
```
*(Esto solo elimina el enlace en `~/.local/bin/duplicate-chat`; tus chats duplicados y el repositorio se mantendrán intactos).*
