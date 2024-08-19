from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Union

#router = FastAPI()
router = APIRouter(tags=["users"],)
#iniciar server : uvicorn user:router --reload

#entidad User
class User(BaseModel):
    id: int
    name: str
    url: str
    age: int

users_fake = [User(id=0, name="Luis Gonzalez", url= "https://subliandev.dev", age=38),
              User(id=1, name="Javier Gonzalez", url= "https://metalrezas.dev", age=34),
              User(id=2, name="Fabiana Gonzalez", url= "https://fabianita.dev", age=9),
              User(id=3, name="Dayana Gonzalez", url= "https://ayanamata.dev", age=44)]

@router.get("/users")
def users():
    return [{"name": "Luis Gonzalez", "url": "https://subliandev.dev"},
            {"name": "Javier Gonzalez", "url": "https://metalrezas.dev"},
            {"name": "Dayana Mata", "url": "https://d.ayanamata.dev"},
            {"name": "Fabiana Gonzalez", "url": "https://fabianita.dev"},
            {"name": "Nancy Pereira", "url": "https://luinanper.dev"}]

@router.get("/usersclass")
def usersclass():
    return User(name="Luis Gonzalez", url="https://subliandev.dev", age=38)

@router.get("/usersfake")
def usersfake():
    return users_fake

# paramatros por path
@router.get("/userfake/{id}")
def userfake(id: int):
    return search_user(id)

# parametros por query
@router.get("/userfakequery/")
def userfakequery(id: int):
    return search_user(id)


def search_user(id: int):
    userfake = filter(lambda user: user.id == id, users_fake)
    try:
        return list(userfake)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

# crear usuario
@router.post("/user/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "El usuario ya existe")

    users_fake.routerend(user)
    return user

# actualizar usuario
@router.put("/user")
async def user(user: User):
    found = False
    for index, saved_user in enumerate( users_fake):
        if saved_user.id == user.id:
            users_fake[index] = user
            found = True
            return {"msg": f"Registro {index} Actualizado"}

    if not found:
        return {"error": f"No se ha encontrado el usuario"}

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate( users_fake):
        if saved_user.id == id:
            del users_fake[index]
            found = True
            return {"msg": f"Registro {index} eliminado"}

    if not found:
        return {"error": f"No se ha encontrado el usuario"}