from fastapi import FastAPI,APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITMO = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "4723cba290fbc10ce38afd19f0404b15"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

crypt  = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

users_db = { 
            "mouredev":{
                "username": "mouredev",
                "full_name": "Brais Moure",
                "email": "bmoure@mouredev.com",
                "disabled": False,
                "password": "$2a$12$9/tAhWwKGuOWj9JXJZVpXu19O4B4h6ZiP0qhPnTpY8jB3XWpsJQSa"},
            "subliandev":{
                "username": "subliandev",
                "full_name": "Luis Gonzalez",
                "email": "lgonzalez@subliandev.com",
                "disabled": True,
                "password": "$2a$12$9/tAhWwKGuOWj9JXJZVpXu19O4B4h6ZiP0qhPnTpY8jB3XWpsJQSa"},
            "fabina":{
                "username": "fabina",
                "full_name": "Fabiana Gonzalez",
                "email": "fabiana@subliandev.com",
                "disabled": False,
                "password": "$2a$12$9/tAhWwKGuOWj9JXJZVpXu19O4B4h6ZiP0qhPnTpY8jB3XWpsJQSa"}
            }

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    excepcion = HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Credenciales de autenticación inválidas",
                                headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub")
        if username is None:
            raise excepcion
    except JWTError:
        raise excepcion
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    acces_token = {"sub": user.username,
                   "exp": datetime.utcnow() +  timedelta(minutes=ACCES_TOKEN_DURATION)
                   }

    return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITMO), "token_type": "bearer"}

@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user