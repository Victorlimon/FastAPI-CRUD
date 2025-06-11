from fastapi import FastAPI

from api.v1 import user
from api.v1 import token
from api.v1 import auth
from api.v1 import usuario
from api.v1 import restaurantes
from api.v1 import upload

app = FastAPI()

#app.include_router(user.router)
#app.include_router(token.router)
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(restaurantes.router)
app.include_router(upload.router)