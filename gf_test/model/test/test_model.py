import json
import os
import shutil
import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from gf_test.model.model import Base, Bank, Account, AccountMovement, MovementTypes
# from gf_test.model.schemas import AccountSchema
from gf_test.model.schemas import AccountSchema, AccountMovementSchema
from gf_test.model.tools import AlchemyEncoder

"""
What if we subtract money from an account that does not have enough money? It may fail ...

"""


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
        steve_account = Account(bank=pankia_bank, customer_name="Steve")
        jim_account = Account(bank=pankia_bank, customer_name="Jim")

        emma_account = Account(bank=santonder_bank, customer_name="Emma")
        sara_account = Account(bank=santonder_bank, customer_name="Sara")

        john_account = Account(bank=da_box_bank, customer_name="John")
        ralph_account = Account(bank=da_box_bank, customer_name="Ralph")

        jim_to_bank_transfer = AccountMovement(dst_account=jim_account,
                                               amount=50000, info="All my funds",
                                               movement_type=MovementTypes.DEPOSIT)
        jim_to_emma_transfer = AccountMovement(src_account=jim_account, dst_account=emma_account,
                                               amount=20000, info="Now we are even",
                                               movement_type=MovementTypes.TRANSFER)
        emma_to_steve_transfer = AccountMovement(src_account=emma_account, dst_account=steve_account,
                                                 amount=2500, info="Flat rent",
                                                 movement_type=MovementTypes.TRANSFER)
        emma_to_sara_transfer = AccountMovement(src_account=emma_account, dst_account=sara_account,
                                                amount=3000, info="Birthday!!",
                                                movement_type=MovementTypes.TRANSFER)

        session.add_all([
            pankia_bank, santonder_bank, da_box_bank,
            steve_account, jim_account, emma_account, sara_account, john_account, ralph_account,
            jim_to_bank_transfer, jim_to_emma_transfer, emma_to_steve_transfer, emma_to_sara_transfer
        ])
        session.commit()

        self.session = session

    def test_model_loaded(self):

        for b in self.session.query(Bank).all():
            print json.dumps(b, cls=AlchemyEncoder)

        acc_schema = AccountSchema()
        for a in self.session.query(Account).all():
            print acc_schema.dump(a).data
            print json.dumps(a, cls=AlchemyEncoder)

        acc_movement_schema = AccountMovementSchema()
        for am in self.session.query(AccountMovement).all():
            print acc_movement_schema.dump(am).data
            print json.dumps(am, cls=AlchemyEncoder)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
