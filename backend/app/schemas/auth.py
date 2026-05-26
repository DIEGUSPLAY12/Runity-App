from pydantic import BaseModel, Field, EmailStr

class UserRegister(BaseModel):
    """
    Datos necesarios para registrar a un nuevo usuario desde la app.
    """
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    display_name: str = Field(..., min_length=2, description="Nombre visible en el perfil")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str