# Runity - Fitness App con Expo + Supabase

Aplicación móvil de tracking de entrenamientos construida con **Expo**, **React Native** y **Supabase**.

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Copia `env-example` a `.env.local`:

```bash
cp env-example .env.local
```

Luego edita `.env.local` con tus credenciales de Supabase:

```env
EXPO_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
EXPO_PUBLIC_SUPABASE_ANON_KEY="your_anon_key_here"
```

**⚠️ IMPORTANTE:** 
- Solo las variables que empiezan con `EXPO_PUBLIC_*` se exponen al cliente.
- **Nunca expongas** `DATABASE_URL`, `AWS_ACCESS_KEY_ID`, o `AWS_SECRET_ACCESS_KEY` en el cliente.
- Esos secretos deben estar solo en tu servidor/backend.

### 3. Iniciar la app

```bash
npx expo start
```

Luego selecciona:
- `i` para iOS Simulator
- `a` para Android Emulator
- `w` para Web
- `s` para Expo Go (en tu teléfono)

## 📁 Estructura del proyecto

```
app/
  ├── _layout.tsx          # Root layout + router
  ├── login.tsx            # Pantalla de login (conectado a Supabase Auth)
  ├── register.tsx         # Pantalla de registro
  └── (tabs)/              # Tabs layout
      ├── index.tsx        # Home / Feed
      ├── create.tsx       # Crear entrenamiento
      ├── workout.tsx      # Ver entrenamientos
      ├── comunity.tsx     # Comunidad
      └── profile.tsx      # Perfil

lib/
  ├── supabase.ts          # Cliente Supabase
  └── supabase-health.ts   # Funciones de diagnóstico

hooks/
  ├── use-auth.ts          # Hook de autenticación
  └── use-color-scheme.ts  # Hook de tema

components/
  ├── ui/                  # Componentes reutilizables
  └── ...
```

## 🔐 Seguridad

### Variables públicas (cliente)
- `EXPO_PUBLIC_SUPABASE_URL`
- `EXPO_PUBLIC_SUPABASE_ANON_KEY`

### Variables privadas (servidor solamente)
- `DATABASE_URL` - Conexión a PostgreSQL
- `AWS_ACCESS_KEY_ID` - Acceso a Storage S3
- `AWS_SECRET_ACCESS_KEY` - Acceso a Storage S3
- `SUPABASE_JWT_SECRET` - Secret de JWT para Auth

## 🧪 Pruebas de conexión

### Desde la app
1. Navega a Login (`app/login.tsx`)
2. Intenta iniciar sesión - si funciona, la conexión a Supabase es exitosa

### Desde código
```typescript
import { testSupabaseConnection } from '@/lib/supabase-health';

const result = await testSupabaseConnection();
console.log(result); // { success: true, message: '...' }
```

## 🔄 Flujo de autenticación

La app usa el hook `useAuth()`:

```typescript
import { useAuth } from '@/hooks/use-auth';

function MyComponent() {
  const { session, loading, signIn, signUp, signOut } = useAuth();

  if (loading) return <Text>Cargando...</Text>;
  if (!session) return <LoginScreen />;
  
  return <HomeScreen />;
}
```

## 🎨 Diseño

- **UI Library:** Gluestack UI + NativeWind (Tailwind CSS)
- **Icons:** Expo Vector Icons (Material Icons)
- **State Management:** Zustand
- **Theme:** Light/Dark mode automático

## 📚 Recursos

- [Expo Docs](https://docs.expo.dev)
- [Supabase Docs](https://supabase.com/docs)
- [React Native](https://reactnative.dev)
- [Tailwind CSS](https://tailwindcss.com)

## 🤝 Contribuir

Si encuentras bugs o tienes sugerencias, abre un issue o PR.

## 📄 Licencia

Proyecto privado - Runity 2026
