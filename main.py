from fastapi import FastAPI

from api.v1 import user
from api.v1 import token 

app = FastAPI()

app.include_router(user.router)
app.include_router(token.router)
