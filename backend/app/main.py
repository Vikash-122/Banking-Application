from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from . import schemas, database, crud, dbTables, auth

app = FastAPI(title = "BANK BACKEND")
app.include_router(auth.router)
database.Base.metadata.create_all(bind = database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_cur_user)]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/create_user")
async def create_user(user_req: schemas.UserCreate, db: db_dependency):
    return crud.create_user(user_req, db)

@app.get("/all_users")
async def all_users(db: db_dependency):
    return db.query(dbTables.User).all()

@app.post("/create_account")
async def create_account(acc_req: schemas.AccountCreate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return crud.create_account(user['user_id'], acc_req, db)

@app.get("/accounts")
async def get_accounts(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return crud.get_accounts(db, user)

@app.post("/transaction")
async def create_transaction(transaction:schemas.Transaction, db:db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return crud.create_transaction(transaction, db)

