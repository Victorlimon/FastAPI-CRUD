from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from core.config import settings
from repository.usuario import UsuarioRepository
from models.usuario import UsuarioDep
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



async def get_user_repository() -> UsuarioRepository:
    return UsuarioRepository()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UsuarioRepository = Depends(get_user_repository)
) -> UsuarioDep:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    
    user = await user_repo.get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: UsuarioDep = Depends(get_current_user),
) -> UsuarioDep:
    if not current_user.activo:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_user_cliente(
    current_user: UsuarioDep = Depends(get_current_active_user)
) -> UsuarioDep:
    if current_user.rol != "cliente":
        raise HTTPException(status_code=400, detail="Acceso denegado")
    return current_user

async def get_current_user_admin(
    current_user: UsuarioDep = Depends(get_current_active_user)
) -> UsuarioDep:
    if current_user.rol != "admin":
        raise HTTPException(status_code=400, detail="Acceso denegado")
    return current_user

async def get_current_user_restaurante(
    current_user: UsuarioDep = Depends(get_current_active_user)
) -> UsuarioDep:
    if current_user.rol != "restaurante":
        raise HTTPException(status_code=400, detail="Acceso denegado")
    return current_user

