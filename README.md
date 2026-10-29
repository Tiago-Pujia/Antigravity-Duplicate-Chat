# Antigravity Duplicate Chat

Herramienta de línea de comandos para ramificar y duplicar conversaciones en **Google Antigravity** en tiempo real, manteniendo el historial completo de análisis sin necesidad de volver a leer ni indexar los contenidos del proyecto.

---

## 📌 Motivación

Al trabajar con asistentes agentic en proyectos medianos o grandes, el inicio de una conversación suele implicar un proceso intensivo de lectura e indexación del espacio de trabajo (código fuente, documentación, dependencias).

Cuando se desea abordar una nueva tarea, investigar una hipótesis alternativa o probar una solución diferente a partir de ese mismo contexto, comenzar un chat nuevo obliga al modelo a escanear nuevamente todo el repositorio. Como la interfaz de usuario de Antigravity no cuenta con una opción visual para duplicar hilos, esta herramienta cubre ese vacío permitiendo realizar un *fork* del hilo en un solo comando.

---

## ✨ Características

* **Ramificación en vivo:** Se conecta directamente con el motor en memoria de Antigravity (`language_server`). La conversación duplicada aparece de inmediato en la barra lateral sin necesidad de recargar la ventana ni reiniciar la aplicación.
* **Preservación total de contexto:** Clona los pasos de ejecución, archivos analizados, artefactos generados y metadatos de la sesión hasta el último punto alcanzado.
* **Búsqueda flexible:** Permite ubicar la conversación por nombre exacto, coincidencia parcial o identificador único.
* **Sin dependencias externas:** Desarrollado utilizando exclusivamente la biblioteca estándar de Python 3.

---

## 🚀 Instalación

1. Clonar el repositorio y acceder a la carpeta:

```bash
git clone https://github.com/usuario/antigravity-duplicate-chat.git
cd antigravity-duplicate-chat
```

2. Otorgar permisos de ejecución y ejecutar el script instalador:

```bash
chmod +x install.sh
./install.sh
```

El script otorgará permisos de ejecución y creará un enlace simbólico en `~/.local/bin/duplicate-chat`, dejando el comando accesible globalmente en cualquier terminal del usuario.

---

## 💻 Ejemplos de Uso

### 1. Duplicación automática
Crea una copia idéntica agregando el sufijo `(Copia)`:

```bash
duplicate-chat "Analisis Inicial de Codigo"
```

> **Nota:** La búsqueda admite coincidencias parciales. Si el chat se titula *"Analisis Inicial de Codigo y Dependencias"*, basta con ingresar `duplicate-chat "Analisis Inicial"`.

---

### 2. Duplicación con nombre personalizado
Permite definir un nuevo título para organizar distintas líneas de trabajo:

```bash
duplicate-chat "Analisis Inicial de Codigo" "Refactor - Modulo de Autenticacion"
```

---

### 3. Listar conversaciones existentes
Para consultar los títulos de los chats registrados actualmente en el entorno:

```bash
duplicate-chat --list
# o de forma abreviada:
duplicate-chat -l
```

---

### 4. Consultar ayuda
```bash
duplicate-chat --help
```

---

## 🔬 Detalles Técnicos

Antigravity opera mediante una arquitectura cliente-servidor local:

```
[ Electron / Frontend ]  <--->  [ language_server (gRPC / Connect) ]  <--->  [ SQLite / Almacenamiento local ]
                                              ▲
                                              │ (Llamada Connect RPC)
                                    [ duplicate-chat ]
```

* **Detección de instancia:** El script examina los procesos locales para identificar la instancia en ejecución de `language_server`, obteniendo dinámicamente su puerto HTTPS activo y el token de seguridad CSRF correspondiente.
* **Llamada a `ForkConversation`:** Envía una solicitud HTTPS al endpoint Connect RPC `/exa.language_server_pb.LanguageServerService/ForkConversation` pasando el identificador de la conversación de origen (`source_cascade_id`) y el índice del último paso alcanzado (`fork_at_step_index`).
* **Sincronización de título:** Mediante `/exa.language_server_pb.LanguageServerService/UpdateConversationAnnotations`, actualiza el nombre del nuevo chat, lo que dispara un evento reactivo que refresca la barra lateral del cliente en tiempo real.

---

## 📋 Requisitos del Sistema

* **Sistema Operativo:** Linux
* **Python:** 3.8 o superior
* **Google Antigravity:** Debe encontrarse en ejecución al momento de invocar el comando para permitir la comunicación con su servicio local.

---

## 🗑️ Desinstalación

Para retirar el comando del sistema:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

Esto elimina el enlace simbólico en `~/.local/bin/duplicate-chat` sin alterar el repositorio ni las conversaciones creadas.
