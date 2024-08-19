from pydantic import BaseModel

#entidad User
class User(BaseModel):
    id: str | None
    username: str
    email: str
