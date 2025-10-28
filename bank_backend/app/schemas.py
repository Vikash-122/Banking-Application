from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str]
    password: str

class AccountCreate(BaseModel):
    user_id: int
    account_type: str

class TransactionCreate(BaseModel):
    account_id: int
    type: str
    amount: float
    description: Optional[str] = None
    source_account_id: Optional[int] = None
    destination_account_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
