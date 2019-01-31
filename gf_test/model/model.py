import datetime
import json

from evdev._input import device_read_many
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql import case
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class MovementTypes(enum.Enum):
    TRANSFER = "TRANSFER"
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
    """
    A transfer between bank accounts, holding some info and associated expenses
    """
    TABLE = 'accountmovement'
    __tablename__ = TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    src_account_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
    dst_account_id = Column(Integer, ForeignKey(Account.TABLE+'.id'), nullable=True)
    amount = Column(Float, nullable=False)
    info = Column(String(250))
    cost = Column(Float, default=0.0)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    movement_type = Column(Enum(MovementTypes), nullable=False)
    src_account = relationship("Account", foreign_keys=[src_account_id])
    dst_account = relationship("Account", foreign_keys=[dst_account_id])

    # Basically I am using this example: https://docs.sqlalchemy.org/en/latest/orm/mapped_sql_expr.html
    @hybrid_property
    def movement_cost(self):
        if self.src_account != self.dst_account and self.src_account != None:
            return 2.5
        else:
            return 0.0

    @movement_cost.expression
    def movement_cost(cls):
        return case([
            (cls.src_account != cls.dst_account and cls.src_account != None, 2.5),
        ], else_=0.0)
