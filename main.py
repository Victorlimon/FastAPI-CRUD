from fastapi import FastAPI

from api.v1 import user

app = FastAPI()

app.include_router(user.router)

