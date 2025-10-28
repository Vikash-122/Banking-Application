from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="owner")

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    account_number = Column(String(20), unique=True, nullable=False)
    account_type = Column(String(20), nullable=False)
    balance = Column(Numeric(15,2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id", ondelete="CASCADE"))
    type = Column(String(20), nullable=False)
    amount = Column(Numeric(15,2), nullable=False)
    description = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    source_account_id = Column(Integer, ForeignKey("accounts.account_id"))
    destination_account_id = Column(Integer, ForeignKey("accounts.account_id"))

    account = relationship("Account", back_populates="transactions")

    __table_args__ = (CheckConstraint('amount > 0', name='positive_amount'),)
