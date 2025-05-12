from repository.user import UserRepository
from core.security import verify_password



class UserService:
    def __init__(self):
        self.repository = UserRepository()

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
    
    async def registration_user():
        return "hola"

