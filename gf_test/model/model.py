from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

Base = declarative_base()


class Bank(Base):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)


class Account(Base):
    """
    A simple account
    """
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, default=0.0)


class Transfer(Base):
    """
    A transfer between banks, holding some infoand associated expenses
    """
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('account.id'))
    receiver_id = Column(Integer, ForeignKey('account.id'))
    amount = Column(Float, nullable=False)
    info = Column(String(250))
    cost = Column(Float(250), default=0.0)


class TransferCost(Base):
    """
    This stores the comission that each bank applies for a transfer
    to another bank.
    """
    sender_id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    receiver_id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    cost = Column(Float)

engine = create_engine('sqlite:///getfinance_tech_test.db')

Base.metadata.create_all(engine)
