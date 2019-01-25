import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime

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


class Transfer(Base):
    """
    A transfer between banks, holding some info and associated expenses
    """
    TABLE = 'transfer'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey(Account.TABLE+'.id'))
    receiver_id = Column(Integer, ForeignKey(Account.TABLE+'.id'))
    amount = Column(Float, nullable=False)
    info = Column(String(250))
    cost = Column(Float, default=0.0)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class BankExpense(Base):
    """
    Stores the expenses due to bank services. Now we only have transfers,
    and we only want to store, so we can keep it simple.
    """
    __tablename__ = 'bankexpense'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transfer = Column(Integer, ForeignKey(Transfer.TABLE + '.id'))
    cost = Column(Float, default=0.0)


class TransferCost(Base):
    """
    This stores the comission that each bank applies for a transfer
    to another bank. Lookup table.
    """
    sender_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    receiver_bank_id = Column(Integer, ForeignKey(Bank.TABLE+'.id'), primary_key=True)
    cost = Column(Float)

engine = create_engine('sqlite:///getfinance_tech_test.db')

Base.metadata.create_all(engine)
