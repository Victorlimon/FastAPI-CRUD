import asyncpg
from contextlib import asynccontextmanager
from core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.DB_URL, 
            min_size=2,
            max_size=10,
            timeout=30,
            
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def get_connection(self):
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            yield conn

# Instancia global que debes exportar
db = Database()