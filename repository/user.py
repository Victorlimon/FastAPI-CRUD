from core.connect_db import db
from models.user import UserDB

class UserRepository:
    async def get_all_users(self):
        async with db.get_connection() as conn:
            users = await conn.fetch("SELECT username, full_name, email, hashed_password, disabled FROM users")
            return [UserDB(**user) for user in users]
    
    async def get_user(self, username: str):
        async with db.get_connection() as conn:
            user = await conn.fetchrow(
                "SELECT username, full_name, email, hashed_password, disabled FROM users WHERE username = $1",
                username)
            return UserDB(**user) if user else None
    
    async def create_user(self, user: UserDB) -> UserDB:
        async with db.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO users (username, full_name, email, hashed_password, disabled)
                VALUES ($1, $2, $3, $4, $5)
                """,
                user.username,
                user.full_name,
                user.email,
                user.hashed_password,
                user.disabled
            )
            return user
    
    async def delete_user(self, username: str) -> bool:
        async with db.get_connection() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE username = $1",
                username
            )
            # Retorna True si se eliminó al menos un registro
            return result.split()[-1] == '1'