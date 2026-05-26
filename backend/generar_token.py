import jwt

# Nuestro secreto local y el ID del usuario que acabamos de crear en Supabase
secret = "super-secret-jwt-token-with-at-least-32-characters-long"
fake_user_id = "123e4567-e89b-12d3-a456-426614174000"

# Fabricamos la pulsera (el token)
token = jwt.encode({"sub": fake_user_id}, secret, algorithm="HS256")

print("\n--- COPIA ESTA LLAVE (SIN LOS GUIONES) ---")
print(token)
print("------------------------------------------\n")