import React, { useState, useEffect } from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  View,
  Pressable,
  TextInput,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { useRouter } from 'expo-router';
import { useAuth } from '@/hooks/use-auth';

export default function LoginScreen() {
  const router = useRouter();
  const { signIn, loading: authLoading, error: authError, session } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // Si ya está autenticado, ir a home
  useEffect(() => {
    if (session) {
      router.replace('/(tabs)');
    }
  }, [session, router]);

  // Email validation
  const validateEmail = (value: string) => {
    if (!value.trim()) {
      setEmailError('El email es requerido');
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      setEmailError('Por favor ingresa un email válido');
      return false;
    }
    setEmailError('');
    return true;
  };

  // Password validation
  const validatePassword = (value: string) => {
    const errors = [];

    if (!value) {
      setPasswordError('La contraseña es requerida');
      return false;
    }

    if (value.length < 8) {
      errors.push('Mínimo 8 caracteres');
    }
    if (!/[A-Z]/.test(value)) {
      errors.push('Mínimo una mayúscula');
    }
    if (!/[a-z]/.test(value)) {
      errors.push('Mínimo una minúscula');
    }
    if (!/[0-9]/.test(value)) {
      errors.push('Mínimo un número');
    }
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value)) {
      errors.push('Mínimo un símbolo');
    }

    if (errors.length > 0) {
      setPasswordError(errors.join(', '));
      return false;
    }

    setPasswordError('');
    return true;
  };

  const handleEmailChange = (text: string) => {
    setEmail(text);
    if (emailError) {
      validateEmail(text);
    }
  };

  const handlePasswordChange = (text: string) => {
    setPassword(text);
    if (passwordError) {
      validatePassword(text);
    }
  };

  const handleLogin = async () => {
    const isEmailValid = validateEmail(email);
    const isPasswordValid = validatePassword(password);

    if (!isEmailValid || !isPasswordValid) {
      return;
    }

    try {
      await signIn(email, password);
      // Navegación automática via useEffect cuando session cambia
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Error en login';
      Alert.alert('Error', errorMsg);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.headerContainer}>
          <Text style={styles.title}>Bienvenido</Text>
          <Text style={styles.subtitle}>Inicia sesión para continuar</Text>
        </View>

        {/* Logo/Icon */}
        <View style={styles.iconContainer}>
          <View style={styles.iconBox}>
            <MaterialIcons name="fitness-center" size={48} color="#004f5d" />
          </View>
        </View>

        {/* Form Container */}
        <View style={styles.formContainer}>

          {/* Email Field */}
          <View style={styles.formControl}>
            <Text style={styles.label}>Email</Text>
            <TextInput
              style={[
                styles.input,
                emailError ? styles.inputError : styles.inputValid,
              ]}
              placeholder="tu@email.com"
              value={email}
              onChangeText={handleEmailChange}
              keyboardType="email-address"
              autoCapitalize="none"
              placeholderTextColor="#b0b0b0"
            />
            {emailError ? (
              <Text style={styles.errorText}>{emailError}</Text>
            ) : (
              <Text style={styles.helperText}>
                Usaremos esto para tu cuenta
              </Text>
            )}
          </View>

          {/* Password Field */}
          <View style={styles.formControl}>
            <Text style={styles.label}>Contraseña</Text>
            <View style={styles.passwordInputContainer}>
              <TextInput
                style={[
                  styles.passwordInput,
                  passwordError
                    ? styles.inputError
                    : styles.inputValid,
                ]}
                placeholder="••••••••"
                value={password}
                onChangeText={handlePasswordChange}
                secureTextEntry={!showPassword}
                placeholderTextColor="#b0b0b0"
              />
              <Pressable
                onPress={() => setShowPassword(!showPassword)}
                style={styles.passwordToggle}
              >
                <MaterialIcons
                  name={showPassword ? 'visibility' : 'visibility-off'}
                  size={20}
                  color="#004f5d"
                />
              </Pressable>
            </View>
            {passwordError ? (
              <Text style={styles.errorText}>{passwordError}</Text>
            ) : (
              <Text style={styles.helperText}>
                Mín. 8 caracteres con mayúscula, minúscula, número y símbolo
              </Text>
            )}
          </View>

           {/* Login Button */}
           <Pressable
             onPress={handleLogin}
             style={[
               styles.loginButton,
               (!email || !password || authLoading) && styles.loginButtonDisabled,
             ]}
             disabled={!email || !password || authLoading}
           >
             {authLoading ? (
               <ActivityIndicator size="small" color="#ffffff" />
             ) : (
               <Text style={styles.buttonText}>Iniciar Sesión</Text>
             )}
           </Pressable>

           {/* Auth Error Message */}
           {authError && (
             <View style={styles.errorAlert}>
               <MaterialIcons name="error" size={16} color="#ef4444" />
               <Text style={styles.errorAlertText}>{authError}</Text>
             </View>
           )}

          {/* Forgot Password */}
          <Pressable style={styles.forgotPasswordContainer}>
            <Text style={styles.forgotPasswordText}>
              ¿Olvidaste tu contraseña?
            </Text>
          </Pressable>

           {/* Sign Up Link */}
           <View style={styles.signupContainer}>
             <Text style={styles.signupText}>¿No tienes cuenta? </Text>
             <Pressable onPress={() => router.push('/register')}>
               <Text style={styles.signupLink}>Regístrate aquí</Text>
             </Pressable>
           </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    paddingHorizontal: 24,
    paddingVertical: 24,
  },
  headerContainer: {
    marginBottom: 32,
    marginTop: 16,
  },
  title: {
    fontSize: 36,
    fontWeight: '700',
    color: '#262626',
    marginBottom: 8,
    lineHeight: 44,
  },
  subtitle: {
    fontSize: 18,
    color: '#8da1b4',
    fontWeight: '500',
    lineHeight: 24,
  },
  iconContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  iconBox: {
    height: 100,
    width: 100,
    borderRadius: 50,
    backgroundColor: '#ecf1f4',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#8ca0ac',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.14,
    shadowRadius: 14,
    elevation: 4,
  },
  formContainer: {
    paddingHorizontal: 0,
  },
  formControl: {
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#262626',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1.5,
    borderColor: '#dfe7eb',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: 'white',
    height: 56,
    fontSize: 16,
    color: '#262626',
  },
  inputValid: {
    borderColor: '#dfe7eb',
  },
  inputError: {
    borderColor: '#ef4444',
  },
  passwordInputContainer: {
    position: 'relative',
  },
  passwordInput: {
    borderWidth: 1.5,
    borderColor: '#dfe7eb',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 12,
    paddingRight: 50,
    backgroundColor: 'white',
    height: 56,
    fontSize: 16,
    color: '#262626',
  },
  passwordToggle: {
    position: 'absolute',
    right: 16,
    top: 18,
  },
  errorText: {
    fontSize: 13,
    color: '#ef4444',
    fontWeight: '500',
    marginTop: 6,
  },
  helperText: {
    fontSize: 13,
    color: '#8da1b4',
    marginTop: 6,
  },
  loginButton: {
    backgroundColor: '#004f5d',
    borderRadius: 25,
    paddingVertical: 16,
    marginTop: 16,
    marginBottom: 24,
    shadowColor: '#8ca0ac',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.14,
    shadowRadius: 14,
    elevation: 4,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loginButtonDisabled: {
    backgroundColor: '#004f5d',
    shadowColor: 'rgba(0, 0, 0, 0.05)',
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
  },
  forgotPasswordContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  forgotPasswordText: {
    fontSize: 16,
    color: '#10bfb5',
    fontWeight: '600',
  },
  signupContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingBottom: 20,
  },
  signupText: {
    fontSize: 16,
    color: '#8da1b4',
  },
  signupLink: {
    fontSize: 16,
    color: '#1ac8c1',
    fontWeight: '700',
  },
  errorAlert: {
    flexDirection: 'row',
    backgroundColor: '#fee2e2',
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
    alignItems: 'center',
    gap: 8,
  },
  errorAlertText: {
    flex: 1,
    fontSize: 13,
    color: '#991b1b',
    fontWeight: '500',
  },
});

