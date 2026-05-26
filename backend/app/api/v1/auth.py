import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession
from supabase import create_client, Client

from app.core.db import get_db
from dotenv import load_dotenv
from app.models.domain import Profile
from app.schemas.auth import UserRegister
from app.schemas.auth import UserLogin
from app.schemas.auth import TokenRefreshRequest

router = APIRouter()
load_dotenv()

# Variables de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Cliente Supabase (lazy initialization)
_supabase_client: Client | None = None

def get_supabase_client() -> Client:
    """Inicializa el cliente de Supabase de forma lazy (solo cuando se necesita)."""
    global _supabase_client
    
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise RuntimeError("Faltan variables de entorno de Supabase (SUPABASE_URL, SUPABASE_ANON_KEY)")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    return _supabase_client

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: DbSession = Depends(get_db)):
    """
    Registra un usuario, crea su perfil y devuelve el token de sesión inmediatamente.
    (Requiere que 'enable_confirmations = false' en la config de Supabase).
    """
    try:
        # 1. Registrar en Supabase Auth
        supabase = get_supabase_client()
        auth_response = supabase.auth.sign_up({
            "email": user_in.email,
            "password": user_in.password
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Error al crear el usuario en Supabase.")
            
        new_user_id = auth_response.user.id

        # 2. Crear el perfil en la base de datos local si no existe
        existing_profile = db.query(Profile).filter(Profile.id == new_user_id).first()
        if not existing_profile:
            new_profile = Profile(
                id=new_user_id,
                display_name=user_in.display_name
            )
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
        
        # 3. Extraer el token de acceso
        # Como quitamos la confirmación por email, Supabase devuelve la sesión directamente
        access_token = auth_response.session.access_token if auth_response.session else None
        
        if not access_token:
             raise HTTPException(
                 status_code=400, 
                 detail="Usuario creado pero no se obtuvo token. Verifica que enable_confirmations=false en Supabase."
             )

        return {
            "message": "Cuenta creada y perfil generado con éxito", 
            "user_id": new_user_id,
            "display_name": user_in.display_name,
            "access_token": access_token,
            "refresh_token": auth_response.session.refresh_token

        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Fallo en el registro: {str(e)}")

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_in: UserLogin):
    """
    Inicia sesión con un usuario existente y devuelve un nuevo token JWT.
    """
    supabase = get_supabase_client() # ¡CUIDADO! Te faltaba inicializar el cliente aquí
    
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": user_in.email,
            "password": user_in.password
        })
        
        if not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="No se ha devuelto sesión. Verifica confirmaciones."
            )

        return {
            "message": "Inicio de sesión exitoso",
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "user_id": auth_response.user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Error real de Supabase: {str(e)}"
        )

@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(token_req: TokenRefreshRequest):
    """
    Recibe un refresh_token válido y devuelve un nuevo access_token y refresh_token.
    Ideal para mantener la sesión viva en el frontend sin pedir credenciales.
    """
    supabase = get_supabase_client()
    
    try:
        auth_response = supabase.auth.refresh_session(token_req.refresh_token)
        
        if not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Refresh token inválido o expirado"
            )

        return {
            "message": "Token refrescado con éxito",
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "user_id": auth_response.user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"No se pudo refrescar el token: {str(e)}"
        )