from core.connect_db import db
from models.usuario import UsuarioComplete

class UsuarioRepository:
    async def get_all_users(self):
        async with db.get_connection() as conn:
            users = await conn.fetch("SELECT id, username, full_name, email, telefono, rol, hashed_password, activo FROM usuarios")
            return [UsuarioComplete(**user) for user in users]
    
    async def get_user(self, username: str):
        async with db.get_connection() as conn:
            user = await conn.fetchrow(
                "SELECT id, username, full_name, email, telefono, rol, hashed_password, activo FROM usuarios WHERE username = $1",
                username)
            return UsuarioComplete(**user) if user else None
    
    async def update_user_rol(self, username: str, rol: dict) -> UsuarioComplete:
        async with db.get_connection() as conn:
            query = """
                UPDATE usuarios
                SET rol = COALESCE($2, rol)
                WHERE username = $1
                RETURNING *
            """
            updated_user = await conn.fetchrow(
                query,
                username,
                rol.get("rol"),
            )
            return UsuarioComplete(**updated_user) if updated_user else None
'''
    
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
    
    async def delete_user(self, username: str) -> UserDB | None:
        async with db.get_connection() as conn:
            deleted_user = await conn.fetchrow(
                "DELETE FROM users WHERE username = $1 RETURNING *",
                username
            )
        return UserDB(**deleted_user) if deleted_user else None
        
    async def update_user(self, username: str, user_data: dict) -> UserDB:
        async with db.get_connection() as conn:
            query = """
                UPDATE users 
                SET full_name = COALESCE($2, full_name),
                    email = COALESCE($3, email),
                    disabled = COALESCE($4, disabled)
                WHERE username = $1
                RETURNING *
            """
            updated_user = await conn.fetchrow(
                query,
                username,
                user_data.get("full_name"),
                user_data.get("email"),
                user_data.get("disabled")
            )
            return UserDB(**updated_user) if updated_user else None
'''