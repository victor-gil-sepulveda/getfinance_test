import datetime
import json

from evdev._input import device_read_many
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum

from sqlalchemy.orm import relationship

Base = declarative_base()


class MovementTypes(enum.Enum):
    TRANSFER_SRC = "TRANSFER_SRC"
    TRANSFER_DST = "TRANSFER_DST"
    BANK_EXPENSE = "BANK_EXPENSE"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    UNKNOWN = "UNKNOWN"


class Bank(Base):
    TABLE = 'bank'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
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
    movement_type = Column(Enum(MovementTypes), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class Transfer(Base):
    """
    A transfer between bank accounts, holding some info and associated expenses
    """
    TABLE = 'transfer'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    src_accmov_id = Column(Integer, ForeignKey(AccountMovement.TABLE+'.id'), nullable=True)
    dst_accmov_id = Column(Integer, ForeignKey(AccountMovement.TABLE+'.id'), nullable=True)
    src_accmov = relationship("AccountMovement", foreign_keys=[src_accmov_id])
    dst_accmov = relationship("AccountMovement", foreign_keys=[dst_accmov_id])
    info = Column(String(250))
