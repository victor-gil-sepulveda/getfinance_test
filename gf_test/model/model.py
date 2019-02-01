import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum

from sqlalchemy.orm import relationship

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

    @staticmethod
    def total(session):
        pass


class AccountMovement(Base):
    TABLE = 'accountmovement'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=False)
    account = relationship("Account", foreign_keys=[account_id])
    movement_type = Column(Integer, nullable=False)
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
