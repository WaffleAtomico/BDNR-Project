# Proyecto BDNR - Pinterest Clone

## Miembros
- Hania Fernanda Chavez Camberos
- Luis Oswaldo Beltran Aranda
- Oscar Alejandro Penilla Skakievich


## Descripción del proyecto
Este proyecto es un clon de Pinterest que permite a los usuarios subir imágenes, crear tableros y explorar contenido visual. Los usuarios pueden registrarse, iniciar sesión, subir imágenes, crear tableros, seguir a otros usuarios y explorar imágenes subidas por la comunidad.
Este proyecto está diseñado para poder tener conciencia de la arquitectura en una aplicacion real y como se puede integrar diferentes tecnologías para lograr un sistema robusto y escalable.

Implementamos el backend utilizando **FastAPI** y el frontend con **React**. Mientras tanto para el almacenamiento de datos, utilizamos una combinación de **Cassandra**, **MongoDB** y **Dgraph** para aprovechar las fortalezas de cada base de datos en diferentes aspectos del proyecto.

### Como se van a correr las consultas?
Por medio de un API REST, el cual se encuentra en el backend, se van a poder hacer las consultas a las bases de datos. El API REST va a tener diferentes endpoints para cada una de las funcionalidades del proyecto, como subir imágenes, crear tableros, seguir usuarios, etc.
Se espera recibir objetos JSON en las solicitudes y devolver respuestas JSON con los resultados de las consultas.
Para las imagenes se va a utilizar R2 de Cloudflare y se va a enviar la imagen en base64 para que el backend la pueda procesar y subir a R2.
Muchas consultas van a utilizar multiples agregaciones a distintas bases de datos para que cada una de estas pueda hacer lo que mejor sabe hacer


### Arquitectura del proyecto
- **FastAPI:** Servidor backend que maneja las solicitudes HTTP, la lógica de negocio y la interacción con las bases de datos.  
- **React:** Interfaz de usuario que permite a los usuarios interactuar con la aplicación de manera intuitiva y dinámica.
- **Cassandra:** Guardar el flujo de eventos como las interacciones del usuario con las imágenes, clicks, búsquedas, para usarlos en la recomendación del sistema.  
- **MongoDB:** Almacenar tags de las imágenes, descripciones de estas, urls, información de los tableros.  
- **Dgraph:** Modela las relaciones entre gustos del usuario y las imágenes y las relaciones entre estas mismas imágenes. 


Este proyecto utiliza una infraestructura basada en **Docker Compose** para gestionar múltiples bases de datos y servicios de backend/frontend.

## Cómo correr el proyecto en local

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
4. Acceder al backend API, a veces se traba, recomiendo hacer un cambio o poner y quitar un comentario en el archivo `backend/app/main.py` para que se reinicie el servidor de uvicorn y el backend quede disponible:
   ```bash
   docker logs -f backend_api
   ```
5. Acceder al backend de swagger en tu navegador:
   ```
   http://localhost:8001/docs#/
   ```


## Cómo modificar los archivos (Modo Desarrollo)

**Nota importante:** No es necesario entrar al contenedor por SSH para modificar el código.

Este proyecto utiliza **Bind Mounts** (volúmenes de mapeo). Esto significa que las carpetas locales (`backend/` y `frontend/`) están "conectadas" en tiempo real con las carpetas dentro de los contenedores.

- **Flujo de trabajo:**
  1. Abre tu editor favorito (VS Code, PyCharm, etc.) en la carpeta local `BDNR-Project`.
  2. Realiza tus cambios en el código localmente.
  3. El contenedor detectará los cambios automáticamente y reiniciará el servidor (si tienes habilitado *Hot Reload*).

- **¿Cuándo usar el contenedor?**
  Solo debes entrar al contenedor por terminal (ej. `docker exec -it backend_api bash`) si necesitas ejecutar comandos específicos de la base de datos o herramientas instaladas dentro del sistema operativo del contenedor que no estén disponibles en tu máquina local.

## Tecnologías utilizadas
- **Bases de Datos:** Cassandra, MongoDB 8.0.4, Dgraph.
- **Backend:** Python (FastAPI).
- **Frontend:** Node.js (React).
- **Interfaz de dgraph:** Ratel (para Dgraph).
