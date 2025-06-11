from fastapi import APIRouter, Depends, HTTPException, status
from services.restaurante import RestauranteService
from typing import Annotated
from models.restaurante import RestauranteCreate, RestauranteView
from models.usuario import UsuarioDep
from core.dependencies import get_current_user_restaurante, get_current_user_admin
from core.config import settings


router = APIRouter( tags=["restautante"], prefix="/restaurantes")
service = RestauranteService()


@router.get("/all", response_model=list[RestauranteView])  
async def list_restaurants(
    current_user: Annotated[UsuarioDep, Depends(get_current_user_admin)]
):
    return await service.get_all_restaurants()


@router.patch("/")  
async def list_restaurants_1(
    restaurante_data: RestauranteView,
    current_user: Annotated[UsuarioDep, Depends(get_current_user_admin)]
):
    nuevo_restaurante = RestauranteCreate(
            usuario_id=current_user.id,
            nombre_comercial=restaurante_data.nombre_comercial,
            direccion=restaurante_data.direccion,
            horario_apertura=restaurante_data.horario_apertura,
            descripcion=restaurante_data.descripcion,
        )
    return await service.create_restaurant_service(nuevo_restaurante)

