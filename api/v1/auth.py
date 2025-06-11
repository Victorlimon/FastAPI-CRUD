from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from core.security import create_access_token
from services.usuario import UsuarioService
from core.config import settings


router = APIRouter( tags=["autentificacion"], prefix="/auth")

service = UsuarioService()

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")


