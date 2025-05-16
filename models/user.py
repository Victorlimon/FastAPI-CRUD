from pydantic import BaseModel

class User(BaseModel):
    username: str  
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserDB(User):
    hashed_password: str
    
class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None
