import json
import os
import shutil
import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from gf_test.model.model import Base, Bank, Account
from gf_test.model.tools import AlchemyEncoder


class TestModel(unittest.TestCase):
    TEST_DB = 'test_gf_model.db'

    def setUp(self):
        if os.path.exists(TestModel.TEST_DB):
            os.remove(TestModel.TEST_DB)
        engine = create_engine('sqlite:///'+TestModel.TEST_DB)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Populate the DB

        ## Banks
        pankia_bank = Bank(name="Pankia")
        santonder_bank = Bank(name="Santonder")
        da_box_bank = Bank(name="DaBox")

        # Accounts
        steve_account = Account(bank=pankia_bank.id, customer_name="Steve")
        jim_account = Account(bank=pankia_bank.id, customer_name="Jim")

        emma_account = Account(bank=santonder_bank.id, customer_name="Emma")
        sara_account = Account(bank=santonder_bank.id, customer_name="Sara")

        john_account = Account(bank=da_box_bank.id, customer_name="John")
        ralph_account = Account(bank=da_box_bank.id, customer_name="Ralph")


        session.add_all([
            pankia_bank, santonder_bank, da_box_bank,

            steve_account, jim_account, emma_account, sara_account, john_account, ralph_account
        ])

        session.commit()
        self.session = session

    def test_AccountMovement(self):
        for b in self.session.query(Bank).filter():
            print json.dumps(b, cls=AlchemyEncoder)

        for a in self.session.query(Account).filter():
            print json.dumps(a, cls=AlchemyEncoder)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
