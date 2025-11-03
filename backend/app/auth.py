# auth.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, schemas, dbTables, database
from typing import Annotated
from .crud import pwd_context
from jose import jwt
import os
router = APIRouter(prefix='/auth', tags=['Users'])

SECRET_KEY = "P06Edn8sAvOeUCUdinb7MvERBmhjBU6gGk3GkEGEZ8E"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_cur_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {'user_id': user_id, 'username': username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def valid_user(username:str, password: str, db):
    user = db.query(dbTables.User).filter(dbTables.User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = valid_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = {'user_id': user.user_id, 'username': user.username}
    access_token = create_access_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {'access_token': access_token, 'token_type': 'bearer'}