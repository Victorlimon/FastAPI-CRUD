from core.connect_db import db
from models.restaurante import RestauranteView, RestauranteCreate


class RestautenteRepository:
    async def get_all_restaurants(self):
        async with db.get_connection() as conn:
            restaurants = await conn.fetch("SELECT nombre_comercial, direccion, horario_apertura, descripcion FROM restaurantes")
            return [RestauranteView(**restaurant) for restaurant in restaurants]
    
    async def create_restaurants(self, restaurant: RestauranteCreate) -> RestauranteCreate:
        async with db.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO restaurantes (usuario_id, nombre_comercial, direccion, horario_apertura, descripcion)
                VALUES ($1, $2, $3, $4, $5)
                """,
                restaurant.usuario_id,
                restaurant.nombre_comercial,
                restaurant.direccion,
                restaurant.horario_apertura,
                restaurant.descripcion
            )
            return restaurant
    
    '''
    async def get_user(self, username: str):
        async with db.get_connection() as conn:
            user = await conn.fetchrow(
                "SELECT username, full_name, email, telefono, rol, hashed_password, activo FROM usuarios WHERE username = $1",
                username)
            return UsuarioDB(**user) if user else None
    
    async def update_user_rol(self, username: str, rol: dict) -> UsuarioDB:
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
            return UsuarioDB(**updated_user) if updated_user else None
    '''