import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
import enum
from sqlalchemy.sql import case
from sqlalchemy.ext.hybrid import hybrid_property

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

    def serialize(self):
        return {
            "id": self.id,

        }


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
    movement_type = Column(Enum(MovementTypes), nullable=True)

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

