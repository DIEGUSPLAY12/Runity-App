import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

# Esquema de seguridad basado en tokens de tipo Bearer
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Middleware que extrae el ID del usuario del JWT de Supabase.
    En entorno local se omite la validación de firma debido a las claves asimétricas del nuevo CLI.
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token, 
            options={
                "verify_signature": False, 
                "verify_aud": False, 
                "verify_exp": True
            }
        )
        
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: identificador de usuario ausente",
            )
            
        return UUID(user_id)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión ha expirado",
        )
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de acceso inválidas"
        )