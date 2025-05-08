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
