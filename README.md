# Runity - Full Stack App

Este repositorio contiene tanto el **Frontend (Mobile)** como el **Backend (API)** de Runity, consolidados en un esquema tipo monorepo para facilitar el desarrollo.

## Estructura del Proyecto

- `/backend`: API construida con FastAPI, SQLAlchemy, Alembic y Supabase.
- `/mobile`: App móvil construida con React Native (Expo) y NativeWind.

## Requisitos Previos

- **Node.js**: v18+ (para el frontend y scripts).
- **Python**: 3.10+ (para el backend).
- **Virtualenv**: Se espera que el backend esté usando el directorio `venv/` dentro de `/backend`.

## Configuración Inicial

1. **Instalar Dependencias de todo el proyecto**
   ```bash
   pnpm install
   pnpm run install:all
   ```
   *(Esto instalará los paquetes de React Native y las dependencias de Python en el `venv` local del backend).*

2. **Configurar Variables de Entorno**
   - **Backend**: Copia `backend/.env.example` a `backend/.env` y llena los datos de conexión a Base de Datos / Supabase.
   - **Frontend**: Copia `mobile/.env.example` a `mobile/.env` y asegúrate de que `EXPO_PUBLIC_API_URL` apunte a la IP de tu servidor backend en desarrollo (por ejemplo, `http://localhost:8000` si usas simulador iOS, `http://10.0.2.2:8000` para emulador Android, o la IP de tu red local `http://192.168.x.x:8000` si pruebas en un dispositivo físico con Expo Go).

## Cómo Ejecutar el Proyecto

Para levantar tanto el Backend como el Frontend simultáneamente, ejecuta:

```bash
pnpm start
```

Esto levantará el backend en `http://0.0.0.0:8000` y el entorno de Expo. Podrás escanear el QR o abrir los simuladores para probar.
