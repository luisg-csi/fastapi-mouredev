### users db api ###

from fastapi import FastAPI, status, HTTPException, APIRouter
from typing import Union
from db.models.users import User
from db.schema.users import user_schema
from db.client import db_client

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={404: {"message": "No encontrado"}})


"""#entidad User
class User(BaseModel):
    id: int
    name: str
    url: str
    age: int"""

users_db = ["""User(id=0, name="Luis Gonzalez", url= "https://subliandev.dev", age=38),
              User(id=1, name="Javier Gonzalez", url= "https://metalrezas.dev", age=34),
              User(id=2, name="Fabiana Gonzalez", url= "https://fabianita.dev", age=9),
              User(id=3, name="Dayana Gonzalez", url= "https://ayanamata.dev", age=44)"""]




@router.get("/")
def usersfake():
    return users_db

# paramatros por path
@router.get("/{id}")
def userfake(id: int):
    return search_user(id)

# parametros por query
@router.get("/")
def userfakequery(id: int):
    return search_user(id)


def search_user(id: int):
    userfake = filter(lambda user: user.id == id, users_db)
    try:
        return list(userfake)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

# crear usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    #if type(search_user(user.id)) == User:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "El usuario ya existe")

    #users_db.routerend(user)
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    print("User: ", new_user)
    return User(**new_user)

# actualizar usuario
@router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate( users_db):
        if saved_user.id == user.id:
            users_db[index] = user
            found = True
            return {"msg": f"Registro {index} Actualizado"}

    if not found:
        return {"error": f"No se ha encontrado el usuario"}

@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate( users_db):
        if saved_user.id == id:
            del users_db[index]
            found = True
            return {"msg": f"Registro {index} eliminado"}

    if not found:
        return {"error": f"No se ha encontrado el usuario"}