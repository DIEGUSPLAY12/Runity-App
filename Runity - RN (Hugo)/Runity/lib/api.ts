/**
 * Cliente API para conectarse a FastAPI backend
 * Maneja requests, errores y timeout
 */

const API_URL = process.env.EXPO_PUBLIC_API_URL;
console.log("Mi API URL es:", API_URL);
const API_PREFIX = '/api/v1'; // Prefijo de versión del backend
const TIMEOUT_MS = 10000; // 10 segundos

// Tipos de respuesta del backend (Runity)
export interface LoginResponse {
  message: string;
  access_token: string;
  refresh_token: string;
  user_id: string;
}

export interface RegisterResponse {
  message: string;
  user_id: string;
  display_name: string;
  access_token: string;
  refresh_token: string;
}

// Tipo unificado para el hook
export interface AuthResponse {
  access_token: string;
  token_type?: string;
  user?: {
    id: string;
    email: string;
    username?: string;
  };
}

export interface AuthError {
  detail?: string;
  error?: string;
  message?: string;
}

// Utilidad para timeout en fetch
function fetchWithTimeout(url: string, options: RequestInit, timeoutMs: number = TIMEOUT_MS) {
  return Promise.race([
    fetch(url, options),
    new Promise<Response>((_, reject) =>
      setTimeout(() => reject(new Error('Conexión expirada. Verifica tu API.')), timeoutMs)
    ),
  ]);
}

/**
 * Login - POST /api/v1/auth/login
 * Espera: { email: string, password: string }
 * Devuelve: { access_token, user_id, refresh_token }
 */
export async function login(email: string, password: string): Promise<AuthResponse> {
  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_API_URL no configurada');
  }

  try {
    const res = await fetchWithTimeout(`${API_URL}${API_PREFIX}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errorData = (await res.json()) as AuthError;
      throw new Error(errorData.detail || errorData.error || 'Login falló');
    }

    const data = (await res.json()) as LoginResponse;

    // Transformar a formato estándar
    return {
      access_token: data.access_token,
      token_type: 'bearer',
      user: {
        id: data.user_id,
        email: email,
      },
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Error desconocido en login';
    console.error('[API] Login error:', message);
    throw new Error(message);
  }
}

/**
 * Register - POST /api/v1/auth/register
 * Espera: { email: string, password: string, display_name: string }
 * Devuelve: { access_token, user_id, display_name, refresh_token }
 */
export async function register(
  email: string,
  password: string,
  username?: string
): Promise<AuthResponse> {
  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_API_URL no configurada');
  }

  // Si no hay username, usar email como display_name
  const displayName = username && username.trim().length > 0
    ? username
    : email.split('@')[0]; // Extrae la parte antes del @

  try {
    const res = await fetchWithTimeout(`${API_URL}${API_PREFIX}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        display_name: displayName
      }),
    });

    if (!res.ok) {
      const errorData = (await res.json()) as AuthError;
      const errorMsg = errorData.detail || errorData.error || 'Registro falló';
      console.error('[API] Register error details:', { status: res.status, error: errorData });
      throw new Error(errorMsg);
    }

    const data = (await res.json()) as RegisterResponse;

    // Transformar a formato estándar
    return {
      access_token: data.access_token,
      token_type: 'bearer',
      user: {
        id: data.user_id,
        email: email,
        username: data.display_name,
      },
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Error desconocido en registro';
    console.error('[API] Register error:', message);
    throw new Error(message);
  }
}

/**
 * Test de conexión - GET /api/v1/health o GET /
 * Devuelve: { ok: true } o { message: "..." }
 */
export async function testConnection(): Promise<boolean> {
  if (!API_URL) {
    console.warn('EXPO_PUBLIC_API_URL no configurada');
    return false;
  }

  try {
    // Intenta primero /api/v1/health, luego /
    let res = await fetchWithTimeout(`${API_URL}${API_PREFIX}/health`, { method: 'GET' }, 5000);
    if (!res.ok) {
      res = await fetchWithTimeout(`${API_URL}/`, { method: 'GET' }, 5000);
    }
    return res.ok;
  } catch (err) {
    console.warn('[API] Health check failed:', err);
    return false;
  }
}

/**
 * Refresh Token - POST /api/v1/auth/refresh
 * Espera: { refresh_token: string }
 * Devuelve: { access_token, refresh_token, user_id, message }
 */
export async function refreshToken(refreshToken: string): Promise<AuthResponse> {
  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_API_URL no configurada');
  }

  try {
    const res = await fetchWithTimeout(`${API_URL}${API_PREFIX}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!res.ok) {
      const errorData = (await res.json()) as AuthError;
      throw new Error(errorData.detail || errorData.error || 'Refresh token falló');
    }

    const data = (await res.json()) as LoginResponse;

    // Transformar a formato estándar
    return {
      access_token: data.access_token,
      token_type: 'bearer',
      user: {
        id: data.user_id,
        email: '', // El backend no devuelve email en refresh
      },
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Error desconocido en refresh';
    console.error('[API] Refresh token error:', message);
    throw new Error(message);
  }
}

/**
 * Llamada genérica autenticada
 * Manda token en header Authorization: Bearer <token>
 */
export async function authenticatedFetch(
  endpoint: string,
  token: string,
  options: RequestInit = {}
) {
  if (!API_URL) {
    throw new Error('EXPO_PUBLIC_API_URL no configurada');
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
    ...((options.headers as Record<string, string>) || {}),
  };

  return fetchWithTimeout(`${API_URL}${API_PREFIX}${endpoint}`, {
    ...options,
    headers,
  });
}

