# 🏃 Runity

¡Bienvenido a **Runity**! Este repositorio consolida en un único espacio (*monorepo*) tanto el **Frontend** (Aplicación Móvil en React Native) como el **Backend** (API en FastAPI conectada a Supabase). 

Esta guía te ayudará a clonar, configurar y ejecutar ambos proyectos de manera local.

---

## 🏗 Estructura del Proyecto

```text
Runity/
├── backend/       # API construida con Python (FastAPI), SQLAlchemy y Supabase
├── mobile/        # App móvil construida con TypeScript, React Native (Expo) y NativeWind
└── package.json   # Orquestador del monorepo (gestiona scripts concurrentes)
```

## 📋 Requisitos Previos

Asegúrate de tener instaladas las siguientes herramientas de desarrollo en tu sistema:

- **[Node.js](https://nodejs.org/es/)** (v18 o superior).
- **[pnpm](https://pnpm.io/es/)**: Gestor de paquetes más rápido y eficiente. Se puede instalar con `npm install -g pnpm`.
- **[Python](https://www.python.org/)** (v3.10 o superior).
- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: **OBLIGATORIO** para ejecutar la base de datos local de Supabase. Debe estar abierto y en ejecución.
- **[Supabase CLI](https://supabase.com/docs/guides/cli)**: Para levantar el entorno local (`brew install supabase/tap/supabase` en macOS).
- **Simuladores (Opcional pero recomendado)**: 
  - [Android Studio](https://developer.android.com/studio) configurado para emular dispositivos Android.
  - Xcode para emular dispositivos iOS (solo en macOS).
  - Alternativamente, puedes usar "Expo Go" instalado en tu teléfono físico.

---

## 🚀 Configuración Inicial

### 1. Levantar Supabase (Base de Datos Local)
El backend depende de un entorno local de Supabase proporcionando autenticación de usuarios y base de datos relacional.
1. Abre **Docker Desktop** y asegúrate de que esté funcionando.
2. Inicia los servicios internos de Supabase:
   ```bash
   cd backend
   supabase start
   ```
Al terminar de encender los contenedores, la terminal imprimirá todas tus credenciales de desarrollo local (API URL, `anon key`, `service_role key`, Studio URL, etc.).

### 2. Instalar Módulos y Dependencias
Desde **la raíz** del repositorio, instala todo lo necesario (los modulos de Node y el entorno virtual (`venv`) de Python):
```bash
# 1. Instala los paquetes compartidos y registra el workspace
pnpm install

# 2. Instala internamente las dependencias de React Native (mobile) y Python (backend)
pnpm run install:all
```
> **Nota**: Este comando de `install:all` ya se encargará de utilizar pip para auto-configurar el entorno `venv` en la carpeta correcta del backend para que no tengas que instalar python globalmente.

### 3. Configurar Variables de Entorno (.env)

**Backend:**
Crea o modifica el archivo `.env` en la carpeta `/backend` y añade los accesos a tu Supabase local (tomados del paso 1).
> ⚠️ **IMPORTANTE**: La librería de `supabase-py` requiere que el string de la `SUPABASE_ANON_KEY` tenga formalmente el formato válido de un **JSON Web Token (JWT)** (es decir, caracteres divididos por puntos `x.y.z`). Si alguna vez tu registro local falla indicando `Invalid API Key`, es porque requiere que uses tu `SUPABASE_JWT_SECRET` para firmar un Token válido asignando los roles 'anon', en base a este [issue conocido](https://github.com/supabase-community/supabase-py/issues). Actualmente el archivo `.env` ya se encuentra parcheado con un Token válido para usar en el desarrollo de Runity.

```env
SUPABASE_URL="http://127.0.0.1:54321"
SUPABASE_ANON_KEY="tu_jwt_anon_key_valida_o_token_generado"
```

**Mobile:**
Duplica el archivo `mobile/env-example` renombrándolo a `mobile/.env`. Ajusta la IP dependiendo del dispositivo que uses para ver la app:
- Para el **Simulador de iOS**: `http://localhost:8000` o `http://127.0.0.1:8000`
- Para el **Emulador de Android**: `http://10.0.2.2:8000` (el emulador de android usa esta ip para comunicarse con el localhost de tu PC).
- Para un **Teléfono físico (Expo Go)**: Obtén tu IP local de WiFi  (ej. `http://192.168.1.50:8000`).

```env
EXPO_PUBLIC_API_URL="http://ip_segun_tu_dispositivo:8000"
```

---

## 💻 Cómo Ejecutar el Entorno de Desarrollo Simultáneo

Hemos configurado un comando general con el que correrás el servidor de Python y la app móvil de React Native **al mismo tiempo**, compartiendo los logs en una única consola interactiva.

Desde **la raíz** del proyecto, ejecuta una única vez:

```bash
pnpm start
```

### ¿Qué ocurrirá al ejecutar esto?
1. **FastAPI (*[backend]* logs amarillos)**: Arranca Uvicorn en el puerto `8000`. Responderá a todas las peticiones que vengan del frontend a su vez cargando las tablas.
2. **React Native (*[mobile]* logs azules/blancos)**: Arranca Metro y Expo Router en el puerto `8081`. 

### Abrir o Interactuar desde tu Móvil o Simulador
En esa misma terminal de comandos que queda ejecutando `pnpm start`, verás un código QR y las siguientes opciones que controlan tu aplicación:
* Presiona <kbd>i</kbd> para lanzar rápidamente el **Simulador de iOS** (necesita Xcode abierto en el pasado previamente o instalado al menos).
* Presiona <kbd>a</kbd> para lanzar el **Emulador de Android** (Nota: en Android Studio debe haber un 'Virtual Device' previamente creado y funcionando).
* **Escanear el Código QR** desde la app gratuita **Expo Go** en tu smartphone físico iOS/Android para visualizar la app al instante. (¡Recuerda que el smartphone y tu PC deben estar conectados exactamente a la misma red WiFi/router para que puedan comunicarse a través de los puertos!).
* <kbd>w</kbd> para ver la aplicación de forma experimental como página web.
* <kbd>r</kbd> para forzar un refresco (reload) de pantalla si los logs de la app web o el simulador se congelan mientras estás desarrollando.

---

## 🛠 Comandos Útiles y Solución a Problemas

* **Apagar los servicios**: Pulsa repetidas veces <kbd>Ctrl</kbd> + <kbd>C</kbd> en la terminal interactiva de `pnpm start`.
* **Explorar la Base de Datos**: Ingresa a la URL del Studio Dashboard local (típicamente [http://127.0.0.1:54323](http://127.0.0.1:54323/project/default/editor)) para administrar a los usuarios, visualizar las tablas y hacer pruebas manuales gráficamente en Local mientras se está rodando y ejecutando `supabase start`.
* **Error de Puertos Ocupados ('EADDRINUSE')**: Ocurre generalmente si la terminal de expo / FastAPI se bloqueó  y se cerró abruptamente dejando el puerto de internet "enganchado". Limpia forzosamente los procesos cerrando el puerto zombie con este comando (en la terminal de Mac o Linux) antes de iniciar de nuevo:
   ```bash
   lsof -ti:8000,8081 | xargs kill -9
   ```
