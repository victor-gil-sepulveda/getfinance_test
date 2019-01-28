import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum


Base = declarative_base()


class Bank(Base):
    TABLE = 'bank'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)


class Account(Base):
    """
    A simple account
    """
    TABLE = 'account'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank = Column(Integer, ForeignKey(Bank.TABLE+'.id'))
    amount = Column(Float, default=0.0)
    name = Column(String(250))


class MovementTypes:
    TRANSFER = "TRANSFER"
    BANK_EXPENSE = "BANK_EXPENSE"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"


class Transfer(Base):
    """
    A transfer between bank accounts, holding some info and associated expenses
    """
    TABLE = 'transfer'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
    receiver_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
    amount = Column(Float, nullable=False)
    info = Column(String(250))
    cost = Column(Float, default=0.0)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    movement_type = Column(Enum(MovementTypes))


class TransferCost(Base):
    """
    This stores the comission that each bank applies for a transfer
    to another bank. Lookup table.
    """
    sender_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    receiver_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    cost = Column(Float, nullable=False)

engine = create_engine('sqlite:///getfinance_tech_test.db')

Base.metadata.create_all(engine)
