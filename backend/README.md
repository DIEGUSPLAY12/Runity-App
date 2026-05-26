# 🏃 API de Runity - Backend

Backend de la aplicación **Runity**, una plataforma completa de gestión deportiva construida con **Python** y **FastAPI**. 

### 📋 Contenido
- Gestión de usuarios y perfiles
- Creación y participación en desafíos deportivos
- Registro de sesiones de entrenamiento
- Sistema de análisis estadístico
- Feed de actividad social
- Sistema de presencia en tiempo real

---

## ⚡ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

| Requisito | Versión | Instalación |
|-----------|---------|------------|
| **Python** | 3.10 o superior | [python.org](https://www.python.org/downloads/) |
| **Git** | Última | `brew install git` (macOS) o [git-scm.com](https://git-scm.com/) |
| **Docker** (Opcional) | Última | Para Supabase local |
| **Node.js** (Frontend) | 16+ | Para tu compañero del frontend |

### Verificar instalaciones
```bash
python --version
git --version
```

---

## 📦 Instalación Local - Paso a Paso

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/Runity-Diego.git
cd Runity-Diego/Runity_Diego
```

> **Nota**: Si aún no tienes acceso al repositorio, pídele al administrador que te agregue como colaborador.

### 2️⃣ Crear y activar entorno virtual

El entorno virtual aísla las dependencias del proyecto de tu sistema.

**macOS y Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

✅ Tu terminal debería mostrar `(.venv)` al inicio de la línea.

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instala todas las librerías necesarias (FastAPI, SQLAlchemy, Alembic, etc.)

### 4️⃣ Configurar Supabase

#### Opción A: Usar Supabase Local (Recomendado para desarrollo)

Si tienes Docker instalado:

```bash
# Instalar Supabase CLI (una sola vez)
brew install supabase/tap/supabase  # macOS
# O descárgalo de: https://supabase.com/docs/guides/cli/getting-started

# En la carpeta del proyecto, iniciar Supabase local
supabase start
```

Esto creará una instancia PostgreSQL local en el puerto `54322`.

#### Opción B: Usar Supabase Online (Producción)

1. Ve a [supabase.com](https://supabase.com/) y crea una cuenta
2. Crea un nuevo proyecto
3. Ve a **Settings > Database** y copia la connection string
4. Actualiza tu archivo `.env` con esa URL

### 5️⃣ Configurar variables de entorno

Crea o edita el archivo `.env` en la raíz del proyecto con lo siguiente:

```env
# Base de Datos (Local - Supabase)
DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:54322/postgres"

# Base de Datos (Producción - Reemplaza con tu URL real)
# DATABASE_URL="postgresql://user:password@host:port/database"

# Configuración de Supabase Auth (Local)
SUPABASE_URL="http://127.0.0.1:54321"
SUPABASE_ANON_KEY="sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"
SUPABASE_JWT_SECRET="super-secret-jwt-token-with-at-least-32-characters-long"

# Configuración de Supabase Auth (Producción)
# Cambiar con tus valores reales de Supabase
# SUPABASE_URL="https://tu-proyecto.supabase.co"
# SUPABASE_ANON_KEY="tu-anon-key-aqui"
# SUPABASE_JWT_SECRET="tu-jwt-secret-aqui"
```

> **⚠️ Importante**: Nunca hagas commit del archivo `.env` (ya está en `.gitignore`)

### 6️⃣ Ejecutar migraciones de base de datos

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head
```

Esto crea las tablas (profiles, sessions, challenges, etc.)

### 7️⃣ Ejecutar el servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

📍 El servidor estará disponible en: **http://localhost:8000**

El `--reload` significa que el servidor se reinicia automáticamente cuando cambias código.

---

## 🌐 Acceder a la API

### 📚 Documentación Interactiva (Swagger UI)

Una vez el servidor esté ejecutándose, la documentación interactiva estará en:

🔗 **http://localhost:8000/docs**

#### Qué puedes hacer con Swagger:

1. **Ver todos los endpoints** - Organizados por categoría (Perfiles, Session, Desafíos, etc.)
2. **Probar endpoints en vivo** - Haz clic en "Try it out" y envía peticiones
3. **Ver esquemas** - Estructura exacta de datos que envía/recibe
4. **Autenticarse** - Usa el botón "Authorize" para agregar tu token

### 📖 Documentación Alternativa (ReDoc)

Versión de solo lectura más bonita:

🔗 **http://localhost:8000/redoc**

### 🧪 Health Check

Para verificar que el servidor esté funcionando:

```bash
curl http://localhost:8000/health
```

---

## 🔐 Autenticación

La mayoría de endpoints requieren un **token JWT** válido.

### Obtener un token

1. Regístrate o inicia sesión a través del endpoint `/auth/login` o `/auth/register`
2. Recibirás un token en la respuesta
3. Úsalo en todas las peticiones posteriores

### Enviar el token

En cada petición, incluye el header:

```http
Authorization: Bearer TU_TOKEN_AQUI
```

### En Swagger UI:

1. Haz clic en el botón **Authorize** (parte superior derecha)
2. Pega tu token
3. Swagger añadirá automáticamente el header a todas tus pruebas

### Generar tokens para testing

```bash
python generar_token.py
```

Esto genera un token de prueba listo para usar.

---

## 📁 Estructura del Proyecto

```
Runity_Diego/
├── app/                           # Código principal de la aplicación
│   ├── main.py                    # Punto de entrada de FastAPI
│   ├── api/
│   │   └── v1/                    # API v1
│   │       ├── auth.py            # Endpoints de autenticación
│   │       ├── profiles.py        # Perfiles de usuario
│   │       ├── sessions.py        # Sesiones de entrenamiento
│   │       ├── challenges.py      # Desafíos deportivos
│   │       ├── feed.py            # Feed de actividad
│   │       ├── friends.py         # Gestión de amigos
│   │       ├── presence.py        # Presencia en tiempo real
│   │       ├── notifications.py   # Notificaciones
│   │       ├── stats.py           # Estadísticas
│   │       └── users.py           # Búsqueda y sugerencias de usuarios
│   ├── core/
│   │   ├── config.py              # Configuración de BD
│   │   └── db.py                  # Sesiones de BD
│   ├── models/
│   │   └── domain.py              # Modelos ORM de SQLAlchemy
│   ├── schemas/                   # Esquemas de validación (Pydantic)
│   └── services/
│       └── challenge_service.py   # Lógica de negocio
├── alembic/                       # Migraciones de base de datos
│   └── versions/                  # Historial de cambios
├── tests/                         # Suite de pruebas
├── supabase/                      # Configuración de Supabase
├── requirements.txt               # Dependencias del proyecto
├── .env                           # Variables de entorno (⚠️ NO subir a Git)
└── README.md                      # Este archivo
```

---

## 🧪 Ejecutar Pruebas

Para asegurar que todo funciona correctamente:

```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar pruebas de un módulo específico
pytest tests/test_auth.py

# Mostrar más detalles
pytest tests/ -v

# Mostrar cobertura de código
pytest tests/ --cov=app
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución**: Asegúrate de estar en la carpeta `Runity_Diego` y que el entorno virtual esté activado.

```bash
cd Runity-Diego/Runity_Diego
source .venv/bin/activate  # o tu comando de activación
```

### Error: "Could not connect to database"

**Solución**: Verifica que:
1. Supabase esté corriendo: `supabase status`
2. La `DATABASE_URL` en `.env` sea correcta
3. PostgreSQL esté escuchando en el puerto correcto

```bash
# Ver el status
supabase status

# Ver logs
supabase db pull
```

### Error: "SUPABASE_URL or SUPABASE_ANON_KEY not found"

**Solución**: Verifica que el archivo `.env` exista en la raíz del proyecto con las variables correctas.

### El servidor inicia pero no puedo conectar

**Solución**: Verifica que el puerto 8000 esté libre:

```bash
# macOS/Linux
lsof -i :8000

# Si algo está en el puerto, termina el proceso o usa otro puerto
uvicorn app.main:app --reload --port 8001
```

### Las migraciones fallan

**Solución**: Reset la BD y aplica migraciones de nuevo:

```bash
# Down a versión anterior (o head para todas)
alembic downgrade -1

# Vuelve a aplicar
alembic upgrade head
```

---

## 👥 Información para Tu Compañero del Frontend

### Lo que necesita saber:

1. **Base URL de la API**: `http://localhost:8000` (desarrollo)
2. **Documentación de endpoints**: `http://localhost:8000/docs`
3. **Todos los endpoints requieren token** en el header `Authorization: Bearer <token>`
4. **La autenticación** devuelve un token JWT que debe guardarse (localStorage, sessionStorage, etc.)
5. **CORS** está configurado para aceptar peticiones locales

### Endpoints principales para el frontend:

- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/profiles/me` - Obtener perfil actual
- `GET /api/v1/users/suggested` - Obtener usuarios sugeridos
- `GET /api/v1/feed` - Obtener feed de actividad
- Más en `/docs` cuando el servidor esté corriendo

---

## 📚 Documentación adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

---

## 💡 Tips para desarrollar

### Modo hot-reload automático
El servidor ya está en `--reload`, así que los cambios se aplican automáticamente.

### Debugging
Usa `print()` o importa `pdb`:
```python
import pdb; pdb.set_trace()
```

### Ver logs de BD
Agrega `echo=True` en `config.py`:
```python
engine = create_engine(DATABASE_URL, echo=True)
```

---

## 🚀 Despliegue a Producción

> ⚠️ **Importante**: Antes de desplegar, cambia todas las variables de `.env` a producción.

```bash
# Desactivar modo reload en producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Se recomienda usar:
- **Gunicorn** como servidor ASGI
- **Nginx** como reverse proxy
- **Docker** para containerización

---

## ❓ Preguntas Frecuentes

**¿Cuál es la frecuencia de actualización de la API?**
El servidor recarga automáticamente con los cambios. Recarga la página de documentación (`/docs`) en el navegador.

**¿Dónde veo los errores?**
En la terminal donde ejecutaste `uvicorn`. También en las respuestas de la API.

**¿Cómo reinicio la base de datos?**
```bash
supabase db reset
alembic upgrade head
```

**¿Necesito instalar algo más aparte de Python?**
Solo Docker si quieres Supabase local. De lo contrario, todo es Python.

---

## 📞 Soporte

Si tienes problemas:

1. Revisa la [documentación de FastAPI](https://fastapi.tiangolo.com/)
2. Revisa el archivo de logs
3. Consulta el endpoint `/docs` para ver detalles de errores
4. Pregunta en el grupo de desarrollo

---

**Última actualización**: Abril 2026
