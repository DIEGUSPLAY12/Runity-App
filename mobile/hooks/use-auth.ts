/**
 * Hook useAuth - maneja sesión y token de usuario
 * Almacena token en expo-secure-store
 */

import { useEffect, useState } from 'react';
import * as SecureStore from 'expo-secure-store';
import { login as apiLogin, register as apiRegister, refreshToken as apiRefreshToken, AuthResponse } from '@/lib/api';

const TOKEN_KEY = 'runity_auth_token';
const REFRESH_TOKEN_KEY = 'runity_refresh_token';

export interface User {
  id: string;
  email: string;
  username?: string;
}

interface AuthState {
  session: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export function useAuth() {
   const [state, setState] = useState<AuthState>({
     session: null,
     token: null,
     loading: true,
     error: null,
   });

   // Al iniciar, intenta restaurar token
   useEffect(() => {
     restoreToken();
   }, []);

   /**
    * Intenta restaurar la sesión del almacenamiento seguro
    * Si hay token guardado, lo restaura; si no, pone loading en false
    */

  const restoreToken = async () => {
    try {
      const savedToken = await SecureStore.getItemAsync(TOKEN_KEY);
      if (savedToken) {
        setState((prev) => ({
          ...prev,
          token: savedToken,
          loading: false,
        }));
      } else {
        setState((prev) => ({
          ...prev,
          loading: false,
        }));
      }
    } catch (err) {
      console.error('[Auth] Error restoring token:', err);
      setState((prev) => ({
        ...prev,
        loading: false,
      }));
    }
  };

   const signIn = async (email: string, password: string) => {
     setState((prev) => ({ ...prev, loading: true, error: null }));
     try {
       const response = await apiLogin(email, password);
       await SecureStore.setItemAsync(TOKEN_KEY, response.access_token);
       // Guardar refresh_token si está disponible
       if (response.user?.id) {
         // Aquí podrías guardar el refresh_token si lo tienes
       }

       setState({
         session: response.user || null,
         token: response.access_token,
         loading: false,
         error: null,
       });

       return response;
     } catch (err) {
       const message = err instanceof Error ? err.message : 'Error en login';
       setState((prev) => ({
         ...prev,
         loading: false,
         error: message,
       }));
       throw err;
     }
   };

   const signUp = async (email: string, password: string, username?: string) => {
     setState((prev) => ({ ...prev, loading: true, error: null }));
     try {
       const response = await apiRegister(email, password, username);
       // Guardar access_token en almacenamiento seguro
       await SecureStore.setItemAsync(TOKEN_KEY, response.access_token);

       setState({
         session: response.user || null,
         token: response.access_token,
         loading: false,
         error: null,
       });

       return response;
     } catch (err) {
       const message = err instanceof Error ? err.message : 'Error en registro';
       setState((prev) => ({
         ...prev,
         loading: false,
         error: message,
       }));
       throw err;
     }
   };

   const signOut = async () => {
     try {
       await SecureStore.deleteItemAsync(TOKEN_KEY);
       await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
       setState({
         session: null,
         token: null,
         loading: false,
         error: null,
       });
     } catch (err) {
       console.error('[Auth] Error signing out:', err);
     }
   };

   const refreshAccessToken = async (refreshToken: string) => {
     try {
       const response = await apiRefreshToken(refreshToken);
       await SecureStore.setItemAsync(TOKEN_KEY, response.access_token);

       setState((prev) => ({
         ...prev,
         token: response.access_token,
         session: response.user || prev.session,
       }));

       return response;
     } catch (err) {
       console.error('[Auth] Error refreshing token:', err);
       // Si falla el refresh, limpiar session
       await signOut();
       throw err;
     }
   };

  return {
    session: state.session,
    token: state.token,
    loading: state.loading,
    error: state.error,
    signIn,
    signUp,
    signOut,
    refreshAccessToken,
  };
}

