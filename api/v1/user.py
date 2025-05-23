from fastapi import APIRouter, Depends, HTTPException, status
from services.user import UserService
from typing import Annotated
from models.user import User
from core.dependencies import get_current_active_user
from models.user import UserDB, UserUpdateRequest
from core.config import settings


router = APIRouter( tags=["users"])
service = UserService()



@router.get("/", response_model=list[User])  
async def list_users():
    return await service.get_all_users()

@router.get("/perri")  
async def setting():
    return [settings.DB_URL]


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("/{username}")
async def user(username: str):
    return await service.get_user(username)



@router.post("/users")
async def register_user(user_data: UserDB):
    # Verificar si el usuario ya existe
    existing_user = await service.get_user(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    return await service.create_user_service(user_data)

@router.delete("/users/{username}")
async def delete_user(username: str):
    success = await service.delete_user_service(username)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

@router.patch("/users/{username}", response_model=UserDB)
async def update_user(
    username: str,
    update_data: UserUpdateRequest,
):
    return await service.update_user_service(
        username=username,
        update_data=update_data,
    )