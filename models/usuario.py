from pydantic import BaseModel
from enum import Enum

class RolUsuario(str, Enum):
    cliente = 'cliente'
    motorizado = 'motorizado'
    admin = 'admin'
    restaurante = 'restaurante'

class Usuario(BaseModel):
    username: str  
    full_name: str | None = None
    email: str | None = None
    telefono: str | None = None
    rol : RolUsuario | None = None
    activo: bool | None = None

class UsuarioDep(Usuario):
    id: int | None = None

class UsuarioDB(Usuario):
    hashed_password: str
    
class Actualizar_usuario(BaseModel):
    full_name: str | None = None
    email: str | None = None
    activo: bool | None = None

class UserRoleUpdate(BaseModel):
    rol: str

class UsuarioComplete(UsuarioDB):
    id: int
