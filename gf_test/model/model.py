import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()


class MovementTypes(enum.IntEnum):
    UNKNOWN = -1
    TRANSFER_SRC = 0
    TRANSFER_DST = 1
    BANK_EXPENSE = 2
    WITHDRAWAL = 3
    DEPOSIT = 4


class Bank(Base):
    TABLE = 'bank'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    current = Column(Boolean, default=False)
    account = relationship("Account", back_populates=__tablename__, uselist=True)


class Account(Base):
    """
    A simple account
    """
    TABLE = 'account'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'))
    customer_name = Column(String(32))
    amount = Column(Float, default=0.0)
    bank = relationship("Bank", back_populates=__tablename__, uselist=False)


class AccountMovement(Base):
    TABLE = 'accountmovement'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=False)
    account = relationship("Account", foreign_keys=[account_id])
    movement_type = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    info = Column(String(250))
