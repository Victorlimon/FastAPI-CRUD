from pydantic import BaseModel

class RestauranteView(BaseModel):
    nombre_comercial: str | None = None
    direccion: str | None = None
    horario_apertura: str | None = None
    descripcion: str | None = None

class RestauranteCreate(RestauranteView):
    usuario_id: str  