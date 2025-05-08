from repository.user import UserRepository
from core.security import verify_password
from fastapi import Depends, HTTPException, status
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from models.token import TokenData
from models.user import UserDB

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def get_all_users(self):
        return await self.repository.get_all_users()
    
    async def get_user(self, username: str):
        return await self.repository.get_user(username)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_user( username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
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
        user = await self.repository.get_user( username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self,
        current_user: Annotated[UserDB, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
