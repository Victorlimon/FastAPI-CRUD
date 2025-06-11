from repository.usuario import UsuarioRepository
from core.security import verify_password
from core.security import get_password_hash
from models.usuario import UsuarioDB, UserRoleUpdate


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()
    
    async def get_all_users(self):
        return await self.repository.get_all_users()
    
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
    async def create_user_service(self, user_data: UserDB):
        # Hash de la contraseña
        hashed_password = get_password_hash(user_data.hashed_password)
        
        user_db = UserDB(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
            disabled=False
        )
        return await self.repository.create_user(user_db)

    async def delete_user_service(self, username: str):
        return await self.repository.delete_user(username)

    async def update_user_service(
        self, 
        username: str,
        update_data: UserUpdateRequest,
    ) -> UserDB:
        # Convertir modelo Pydantic a dict, excluyendo campos no actualizables
        update_dict = update_data.dict(exclude_unset=True)
        
        return await self.repository.update_user(username, update_dict)
    '''