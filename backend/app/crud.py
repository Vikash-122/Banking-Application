from fastapi import HTTPException
from . import schemas, dbTables
# from .main import db_dependency//
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def create_user(user_req:schemas.UserCreate, db):
    hashed_pw = pwd_context.hash(user_req.password)
    user = dbTables.User(username = user_req.username, hashed_password=hashed_pw, email = user_req.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_account(user_id:int, account_req:schemas.AccountCreate, db):
    acc_number = str(uuid.uuid4().int)[:12]
    account_info = dbTables.Account(
        account_number= acc_number,
        user_id = user_id,
        account_type= account_req.account_type,
    )
    db.add(account_info)
    db.commit()
    db.refresh(account_info)
    return account_info

def create_transaction(transaction_req: schemas.Transaction, db):
    match transaction_req.type:
        case 'deposit':
            return create_deposit_transaction(transaction_req, db)
        case 'withdraw':
            return create_withdraw_transaction(transaction_req, db)
        case 'transfer':
            return create_transfer_transaction(transaction_req, db)
    return None

    # checking if source account have enough money

def create_deposit_transaction(transaction_req: schemas.Transaction, db):
    user_account = db.query(dbTables.Account).filter(
        dbTables.Account.account_number == transaction_req.destination_account_number).first()

    if not user_account:
        raise HTTPException(status_code=400, detail="Incorrect account number")

    transaction_info = dbTables.Transaction(
        account_id= user_account.account_id,
        type = transaction_req.type,
        amount= transaction_req.amount,
        description= transaction_req.description,
        source_account_number= transaction_req.source_account_number,
        destination_account_number= transaction_req.destination_account_number,
    )
    user_account.balance += transaction_req.amount
    db.add(transaction_info)
    db.commit()
    db.refresh(transaction_info)

    return transaction_info

def create_withdraw_transaction(transaction_req: schemas.Transaction, db):
    user_account = db.query(dbTables.Account).filter(
        dbTables.Account.account_number == transaction_req.source_account_number).first()

    if not user_account:
        raise HTTPException(status_code=400, detail="Incorrect account number")

    if user_account.balance < transaction_req.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    transaction_info = dbTables.Transaction(
        account_id= user_account.account_id,
        type = transaction_req.type,
        amount= transaction_req.amount,
        description= transaction_req.description,
        source_account_number= transaction_req.source_account_number,
        destination_account_number= transaction_req.destination_account_number,
    )
    user_account.balance -= transaction_req.amount
    db.add(transaction_info)
    db.commit()
    db.refresh(transaction_info)
    return transaction_info

def create_transfer_transaction(transaction_req: schemas.Transaction, db):
    # transaction_id = str(uuid.uuid4().int)[:12]
    user_account = db.query(dbTables.Account).filter(
        dbTables.Account.account_number == transaction_req.source_account_number).first()
    destination_account = db.query(dbTables.Account).filter(
        dbTables.Account.account_number == transaction_req.destination_account_number).first()

    if not (user_account and destination_account):
        raise HTTPException(status_code=400, detail="Incorrect account number")

    if user_account.balance < transaction_req.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    transaction_info = dbTables.Transaction(
        account_id= user_account.account_id,
        type = transaction_req.type,
        amount= transaction_req.amount,
        description= transaction_req.description,
        source_account_number= transaction_req.source_account_number,
        destination_account_number= transaction_req.destination_account_number,
    )
    user_account.balance -= transaction_req.amount
    destination_account.balance += transaction_req.amount
    db.add(transaction_info)
    db.commit()
    db.refresh(transaction_info)
    return transaction_info

def get_accounts(db, user):
    accounts = db.query(dbTables.Account).filter(dbTables.Account.user_id == user['user_id']).all()
    return accounts