from fastapi import APIRouter, HTTPException, Depends, status
from models.user import UserDB
from services.user import UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from models.token import Token
from datetime import datetime, timedelta, timezone
from core.security import create_access_token
from models.user import UserDB


from core.security import verify_password
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from models.token import TokenData
from models.user import UserDB
from services.user import UserService
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")
router = APIRouter(prefix="/api/v1/users", tags=["users"])
service = UserService()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await service.get_user("victor")
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserDB, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.get("/", response_model=list[UserDB])  # <-- Nuevo endpoint
async def list_users():
    return await service.get_all_users()


@router.get("/{username}")
async def user(username: str):
    return await service.get_user(username)

@router.get("/user", response_model=UserDB)
async def read_users_me(
    current_user: Annotated[UserDB, Depends(get_current_active_user)],
):
    return current_user


@router.post("/auth")
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")

