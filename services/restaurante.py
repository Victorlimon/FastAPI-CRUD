from repository.restaurante import RestautenteRepository
from core.security import verify_password
from core.security import get_password_hash
from models.restaurante import RestauranteCreate, RestauranteView


class RestauranteService:
    def __init__(self):
        self.repository = RestautenteRepository()
    
    async def get_all_restaurants(self):
        return await self.repository.get_all_restaurants()
    
    async def create_restaurant_service(self, restaurant_data: RestauranteCreate):

        restaurant_db = RestauranteCreate(
            usuario_id=restaurant_data.usuario_id,
            nombre_comercial=restaurant_data.nombre_comercial,
            direccion=restaurant_data.direccion,
            horario_apertura=restaurant_data.horario_apertura,
            descripcion=restaurant_data.descripcion
        )
        return await self.repository.create_restaurants(restaurant_db)
    
    '''
    async def get_user(self, username: str):
        return await self.repository.get_user(username)
    
    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    
    async def update_user_rol_service(
        self, 
        username: str,
        rol: UserRoleUpdate,
    ) -> UsuarioDB:
        # Convertir modelo Pydantic a dict, excluyendo campos no actualizables
        rol = rol.dict(exclude_unset=True)
        
        return await self.repository.update_user_rol(username, rol)
    '''