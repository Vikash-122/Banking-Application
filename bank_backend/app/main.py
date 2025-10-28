from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from .routes import auth as auth_router
from .auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Backend API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth_router.router)

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/accounts/")
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_id != account.user_id:
        raise HTTPException(status_code=403, detail="Cannot create account for other user")
    return crud.create_account(db, account)

@app.post("/transactions/")
def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    acct = db.query(models.Account).filter(models.Account.account_id == txn.account_id).first()
    if acct is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if acct.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only transact on your own accounts")
    try:
        return crud.make_transaction(db, txn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
