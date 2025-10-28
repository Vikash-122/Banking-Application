from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, phone=user.phone, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_account(db: Session, account: schemas.AccountCreate):
    acc_number = str(uuid.uuid4().int)[:12]
    db_account = models.Account(user_id=account.user_id, account_number=acc_number, account_type=account.account_type, balance=0.00)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def make_transaction(db: Session, txn: schemas.TransactionCreate):
    account = db.query(models.Account).filter(models.Account.account_id == txn.account_id).first()
    if not account:
        raise ValueError("Account not found")

    if txn.type == "deposit":
        account.balance = account.balance + txn.amount
    elif txn.type == "withdrawal":
        if account.balance < txn.amount:
            raise ValueError("Insufficient funds")
        account.balance = account.balance - txn.amount
    elif txn.type == "transfer":
        source = db.query(models.Account).get(txn.source_account_id)
        dest = db.query(models.Account).get(txn.destination_account_id)
        if source is None or dest is None:
            raise ValueError("Source or destination account not found")
        if source.balance < txn.amount:
            raise ValueError("Insufficient balance in source account")
        source.balance = source.balance - txn.amount
        dest.balance = dest.balance + txn.amount
    else:
        raise ValueError("Invalid transaction type")

    db_txn = models.Transaction(**txn.dict())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn
