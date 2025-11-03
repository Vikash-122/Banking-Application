from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class AccountCreate(BaseModel):
    username: str
    account_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Transaction(BaseModel):
    type: str
    source_account_number: str
    destination_account_number: str
    amount: int
    description: str
