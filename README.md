# Runity App

Aplicación móvil para registrar y gestionar actividades físicas en tiempo real. Runity permite a los usuarios rastrear sus sesiones de ejercicio, participar en desafíos, conectar con amigos y visualizar estadísticas detalladas de su actividad física.

## 📱 Características

- **Registro de Actividades**: Captura automática de datos de actividad física en tiempo real
- **Desafíos Competitivos**: Participa en retos con amigos y compara resultados
- **Sistema Social**: Conecta con otros usuarios, síguelos y comparte logros
- **Estadísticas Detalladas**: Visualiza análisis completos de tu actividad física
- **Notificaciones en Tiempo Real**: Recibe alertas sobre eventos importantes
- **Presencia en Vivo**: Ve quién está activo en la comunidad

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado en dos aplicaciones principales:

```
Runity App/
├── Runity - FastApi (Diego)/    # Backend API
└── Runity - RN (Hugo)/          # Aplicación móvil
```

## 💻 Stack Tecnológico

### Backend (FastAPI)
- **Framework**: FastAPI 0.135.1
- **Servidor**: Uvicorn con UVLoop
- **Base de Datos**: PostgreSQL via Supabase
- **ORM**: SQLAlchemy 2.0
- **Migraciones**: Alembic
- **Autenticación**: PyJWT
- **Validación**: Pydantic 2.12
- **Herramientas**: Python 3.x, Ruff (linting), python-dotenv

### Frontend (React Native)
- **Framework**: React Native 0.81.5
- **Build Tool**: Expo 54.0
- **Lenguaje**: TypeScript
- **Navegación**: Expo Router 6.0 + React Navigation
- **Estilos**: TailwindCSS con NativeWind 4.1
- **Estado Global**: Zustand 5.0
- **Animaciones**: React Native Reanimated, Legend Motion
- **UI Components**: Gluestack UI 3.0
- **Iconos**: Expo Vector Icons

### Base de Datos
- **Supabase** (PostgreSQL managed)
- Migraciones SQL en `supabase/migrations/`

## 🚀 Guía de Instalación y Ejecución

### Requisitos Previos

- **Node.js**: 18+ (para el frontend)
- **Python**: 3.8+ (para el backend)
- **Git**: Para clonar el repositorio
- **Expo CLI**: `npm install -g expo-cli` (opcional, pero recomendado)
- **Acceso a Supabase**: Credenciales de base de datos

### 1. Clonar el Repositorio

```bash
cd /Users/diegogarcia/Desktop/Runity\ App
git clone <url-del-repo>
```

### 2. Configurar Backend (FastAPI)

#### Paso 1: Navegar a la carpeta del backend

```bash
cd "Runity - FastApi (Diego)"
```

#### Paso 2: Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

#### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar variables de entorno

Crea un archivo `.env` en la raíz del backend con:

```
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
JWT_SECRET_KEY=tu_clave_secreta_aqui
ENVIRONMENT=development
```

#### Paso 5: Ejecutar migraciones de base de datos

```bash
alembic upgrade head
```

#### Paso 6: Iniciar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El API estará disponible en `http://localhost:8000`

**Documentación interactiva**: `http://localhost:8000/docs` (Swagger UI)

### 3. Configurar Frontend (React Native)

#### Paso 1: Navegar a la carpeta del frontend

```bash
cd "../Runity - RN (Hugo)/Runity"
```

#### Paso 2: Instalar dependencias

```bash
npm install
# o
yarn install
```

#### Paso 3: Configurar variables de entorno

Crea un archivo `.env` basado en `env-example`:

```bash
cp env-example .env
```

Completa las variables con tu configuración de API y Supabase.

#### Paso 4: Iniciar el servidor de desarrollo

**Para iOS**:
```bash
npm run ios
```

**Para Android**:
```bash
npm run android
```

**Para Web**:
```bash
npm run web
```

**Genérico (elige plataforma)**:
```bash
npm start
```

## 📁 Estructura de Directorios

### Backend
```
Runity - FastApi (Diego)/
├── app/
│   ├── main.py              # Punto de entrada de la app
│   ├── api/                 # Rutas y endpoints
│   ├── core/                # Configuración y BD
│   ├── models/              # Modelos de dominio
│   ├── schemas/             # Esquemas Pydantic
│   └── services/            # Lógica de negocio
├── alembic/                 # Migraciones de BD
├── tests/                   # Suite de pruebas
├── pyproject.toml           # Configuración de Ruff
├── requirements.txt         # Dependencias Python
└── generar_token.py        # Utilidad para generar tokens
```

### Frontend
```
Runity - RN (Hugo)/Runity/
├── app/                     # Rutas y screens (Expo Router)
├── components/              # Componentes reutilizables
├── constants/               # Constantes de la app
├── hooks/                   # Hooks personalizados
├── assets/                  # Imágenes y recursos
├── package.json             # Dependencias de Node
└── tailwind.config.js       # Configuración de Tailwind
```

## 🧪 Testing

### Backend

```bash
cd "Runity - FastApi (Diego)"
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=app tests/
```

### Frontend

```bash
cd "Runity - RN (Hugo)/Runity"
npm run lint
```

## 📝 Comandos Útiles

### Backend
- `uvicorn app.main:app --reload` - Iniciar servidor con hot-reload
- `alembic revision --autogenerate -m "descripción"` - Crear nueva migración
- `alembic upgrade head` - Aplicar migraciones
- `python generar_token.py` - Generar token JWT

### Frontend
- `npm start` - Iniciar servidor de desarrollo
- `npm run ios` - Ejecutar en simulador iOS
- `npm run android` - Ejecutar en emulador Android
- `npm run web` - Ejecutar en navegador web
- `npm run lint` - Verificar estilo de código
- `npm run reset-project` - Resetear proyecto a estado inicial

## 🔧 Configuración de Desarrollo

### IDE Recomendado
- **Backend**: VS Code con extensiones de Python y FastAPI
- **Frontend**: VS Code con extensiones de React Native y TypeScript

### Extensiones Recomendadas
- Backend: Pylance, Python, FastAPI
- Frontend: ES7+ React/Redux snippets, TypeScript Vue Plugin, Tailwind CSS IntelliSense

## 📚 Documentación Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Native Docs](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [Supabase Docs](https://supabase.com/docs)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
2. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
3. Push a la rama (`git push origin feature/AmazingFeature`)
4. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 👥 Autores

- **Backend**: Diego García
- **Frontend**: Hugo

---

**Última actualización**: 18 de mayo de 2026
