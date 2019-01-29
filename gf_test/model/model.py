import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum

Base = declarative_base()


class Bank(Base):
    TABLE = 'bank'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))


class Account(Base):
    """
    A simple account
    """
    TABLE = 'account'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank = Column(Integer, ForeignKey(Bank.TABLE+'.id'))
    customer_name = Column(String(32))
    amount = Column(Float, default=0.0)


class MovementTypes(enum.Enum):
    TRANSFER = "TRANSFER"
    BANK_EXPENSE = "BANK_EXPENSE"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"


class AccountMovement(Base):
    """
    A transfer between bank accounts, holding some info and associated expenses
    """
    TABLE = 'accountmovement'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    src_account = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
    dst_account = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
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
    TABLE = 'transfercost'
    __tablename__ = TABLE
    sender_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    receiver_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    cost = Column(Float, nullable=False)

# engine = create_engine('sqlite:///getfinance_tech_test.db')
#
# Base.metadata.create_all(engine)
