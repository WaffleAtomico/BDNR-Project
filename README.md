# Proyecto BDNR - Sistema de Gestión

Este proyecto utiliza una infraestructura basada en **Docker Compose** para gestionar múltiples bases de datos y servicios de backend/frontend.

## 🚀 Cómo correr el proyecto en local

Para levantar todo el entorno de desarrollo, asegúrate de tener Docker y Docker Compose instalados en tu máquina.

1. Navega a la raíz del proyecto:
   ```bash
   cd /BDNR-Project
   ```
2. Levanta todos los servicios:
   ```bash
   docker compose up -d
   ```
3. Verifica que los servicios estén corriendo:
   ```bash
   docker compose ps
   ```

## 🛠️ Cómo modificar los archivos (Modo Desarrollo)

**Nota importante:** No es necesario entrar al contenedor por SSH para modificar el código.

Este proyecto utiliza **Bind Mounts** (volúmenes de mapeo). Esto significa que las carpetas locales (`backend/` y `frontend/`) están "conectadas" en tiempo real con las carpetas dentro de los contenedores.

- **Flujo de trabajo:**
  1. Abre tu editor favorito (VS Code, PyCharm, etc.) en la carpeta local `BDNR-Project`.
  2. Realiza tus cambios en el código localmente.
  3. El contenedor detectará los cambios automáticamente y reiniciará el servidor (si tienes habilitado *Hot Reload*).

- **¿Cuándo usar el contenedor?**
  Solo debes entrar al contenedor por terminal (ej. `docker exec -it backend_api bash`) si necesitas ejecutar comandos específicos de la base de datos o herramientas instaladas dentro del sistema operativo del contenedor que no estén disponibles en tu máquina local.

## 📋 Tecnologías utilizadas
- **Bases de Datos:** Cassandra, MongoDB 8.0.4, Dgraph.
- **Backend:** Python (API).
- **Frontend:** Node.js (React).
- **UI:** Ratel (para Dgraph).
