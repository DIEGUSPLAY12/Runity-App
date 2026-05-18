import React, { useState } from 'react';
import {
    ScrollView,
    StyleSheet,
    Text,
    View,
    Pressable,
    TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';

export default function RegisterScreen() {
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showRepeatPassword, setShowRepeatPassword] = useState(false);

    const [usernameError, setUsernameError] = useState('');
    const [emailError, setEmailError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const [repeatPasswordError, setRepeatPasswordError] = useState('');

    // Username validation
    const validateUsername = (value: string) => {
        if (!value.trim()) {
            setUsernameError('El nombre de usuario es requerido');
            return false;
        }
        if (value.trim().length < 3) {
            setUsernameError('El nombre de usuario debe tener al menos 3 caracteres');
            return false;
        }
        setUsernameError('');
        return true;
    };

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

    // Repeat password validation
    const validateRepeatPassword = (value: string) => {
        if (!value) {
            setRepeatPasswordError('Debes confirmar tu contraseña');
            return false;
        }
        if (value !== password) {
            setRepeatPasswordError('Las contraseñas no coinciden');
            return false;
        }
        setRepeatPasswordError('');
        return true;
    };

    const handleUsernameChange = (text: string) => {
        setUsername(text);
        if (usernameError) {
            validateUsername(text);
        }
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
        // Revalidate repeat password if it exists
        if (repeatPassword) {
            validateRepeatPassword(repeatPassword);
        }
    };

    const handleRepeatPasswordChange = (text: string) => {
        setRepeatPassword(text);
        if (repeatPasswordError) {
            validateRepeatPassword(text);
        }
    };

    const handleRegister = () => {
        const isUsernameValid = validateUsername(username);
        const isEmailValid = validateEmail(email);
        const isPasswordValid = validatePassword(password);
        const isRepeatPasswordValid = validateRepeatPassword(repeatPassword);

        if (
            isUsernameValid &&
            isEmailValid &&
            isPasswordValid &&
            isRepeatPasswordValid
        ) {
            console.log('Registration successful:', {
                username,
                email,
                password,
            });
            // Navigate to login after successful registration
            router.push('/(tabs)');
        }
    };

    const isFormValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        repeatPassword.trim();

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView
                contentContainerStyle={styles.content}
                showsVerticalScrollIndicator={false}
            >
                {/* Header */}
                <View style={styles.headerContainer}>
                    <Text style={styles.title}>Crear Cuenta</Text>
                    <Text style={styles.subtitle}>Únete a la comunidad de Runity</Text>
                </View>

                {/* Logo/Icon */}
                <View style={styles.iconContainer}>
                    <View style={styles.iconBox}>
                        <MaterialIcons name="fitness-center" size={48} color="#004f5d" />
                    </View>
                </View>

                {/* Form Container */}
                <View style={styles.formContainer}>
                    {/* Username Field */}
                    <View style={styles.formControl}>
                        <Text style={styles.label}>Nombre de Usuario</Text>
                        <TextInput
                            style={[
                                styles.input,
                                usernameError ? styles.inputError : styles.inputValid,
                            ]}
                            placeholder="Tu nombre de usuario"
                            value={username}
                            onChangeText={handleUsernameChange}
                            autoCapitalize="none"
                            placeholderTextColor="#b0b0b0"
                        />
                        {usernameError ? (
                            <Text style={styles.errorText}>{usernameError}</Text>
                        ) : (
                            <Text style={styles.helperText}>
                                Mínimo 3 caracteres
                            </Text>
                        )}
                    </View>

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
                                    passwordError ? styles.inputError : styles.inputValid,
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

                    {/* Repeat Password Field */}
                    <View style={styles.formControl}>
                        <Text style={styles.label}>Confirmar Contraseña</Text>
                        <View style={styles.passwordInputContainer}>
                            <TextInput
                                style={[
                                    styles.passwordInput,
                                    repeatPasswordError
                                        ? styles.inputError
                                        : styles.inputValid,
                                ]}
                                placeholder="••••••••"
                                value={repeatPassword}
                                onChangeText={handleRepeatPasswordChange}
                                secureTextEntry={!showRepeatPassword}
                                placeholderTextColor="#b0b0b0"
                            />
                            <Pressable
                                onPress={() => setShowRepeatPassword(!showRepeatPassword)}
                                style={styles.passwordToggle}
                            >
                                <MaterialIcons
                                    name={showRepeatPassword ? 'visibility' : 'visibility-off'}
                                    size={20}
                                    color="#004f5d"
                                />
                            </Pressable>
                        </View>
                        {repeatPasswordError ? (
                            <Text style={styles.errorText}>{repeatPasswordError}</Text>
                        ) : (
                            <Text style={styles.helperText}>
                                Repite tu contraseña
                            </Text>
                        )}
                    </View>

                    {/* Register Button */}
                    <Pressable
                        onPress={handleRegister}
                        style={[
                            styles.registerButton,
                            !isFormValid && styles.registerButtonDisabled,
                        ]}
                        disabled={!isFormValid}

                    >
                        <Text style={styles.buttonText}>Crear Cuenta</Text>
                    </Pressable>

                    {/* Login Link */}
                    <View style={styles.loginContainer}>
                        <Text style={styles.loginText}>¿Ya tienes cuenta? </Text>
                        <Pressable onPress={() => router.push('/login')}>
                            <Text style={styles.loginLink}>Inicia sesión aquí</Text>
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
    backButton: {
        alignSelf: 'flex-start',
        padding: 8,
        marginBottom: 16,
    },
    headerContainer: {
        marginBottom: 32,
        marginTop: 8,
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
        marginBottom: 20,
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
        marginBottom: 12,
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
    registerButton: {
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
    registerButtonDisabled: {
        backgroundColor: '#004f5d',
        shadowColor: 'rgba(0, 0, 0, 0.05)',
    },
    buttonText: {
        fontSize: 18,
        fontWeight: '700',
        color: '#ffffff',
    },
    loginContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingBottom: 20,
    },
    loginText: {
        fontSize: 16,
        color: '#8da1b4',
    },
    loginLink: {
        fontSize: 16,
        color: '#1ac8c1',
        fontWeight: '700',
    },
});

