from fastapi import APIRouter, Depends, HTTPException, status
from services.usuario import UsuarioService
from typing import Annotated
from models.usuario import Usuario, UserRoleUpdate
from core.dependencies import get_current_active_user, get_current_user_cliente, get_current_user_admin
from core.config import settings


router = APIRouter( tags=["usuarios"], prefix="/users")
service = UsuarioService()


@router.get("/", response_model=list[Usuario])  
async def list_users(
    current_user: Annotated[Usuario, Depends(get_current_user_admin)]
):
    return await service.get_all_users()


@router.get("/me", response_model=Usuario)
async def read_users_me(
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    return current_user

@router.patch("/{username}/role")
async def update_user_role(
    username: str,
    rol: UserRoleUpdate,
    current_user: Usuario = Depends(get_current_user_admin)
    ):
    return await service.update_user_rol_service(
        username=username,
        rol=rol,
    )


'''



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
'''