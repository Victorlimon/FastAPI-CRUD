from fastapi import APIRouter, Depends
from services.user import UserService
from typing import Annotated
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_active_user



router = APIRouter( tags=["users"])
service = UserService()


@router.get("/", response_model=list[User])  # <-- Nuevo endpoint
async def list_users():
    return await service.get_all_users()

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("/{username}")
async def user(username: str):
    return await service.get_user(username)


@router.post("/usercreate")
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return ["regustration"]