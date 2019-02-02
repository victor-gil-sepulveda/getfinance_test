import inspect
import json
import os
import unittest
import os.path

import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from gf_test.model.model import Base, Bank, Account, AccountMovement, MovementTypes
from gf_test.model.operation import Operation
from gf_test.model.schemas import AccountSchema, AccountMovementSchema, BankSchema
import gf_test.model.test as test_module

"""
What if we subtract money from an account that does not have enough money? It may fail ...

"""


class TestModel(unittest.TestCase):
    TEST_DB = 'test_gf_model.db'

    @classmethod
    def setUpClass(cls):
        # get test data folder
        cls.data_folder = os.path.join(os.path.dirname(inspect.getfile(test_module)), "data")

    def setUp(self):
        # Populate the DB
        if os.path.exists(TestModel.TEST_DB):
            os.remove(TestModel.TEST_DB)
        engine = create_engine('sqlite:///'+TestModel.TEST_DB)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

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

        jim_to_bank_mov = AccountMovement(account=jim_account,
                                          amount=50000,
                                          movement_type=MovementTypes.DEPOSIT,
                                          created=datetime.datetime.strptime('24052010', "%d%m%Y").date(),
                                          info="All my money")

        jim_to_emma_src = AccountMovement(account=jim_account,
                                          amount=-20000,
                                          movement_type=MovementTypes.TRANSFER_SRC,
                                          created=datetime.datetime.strptime('24052010',
                                                                             "%d%m%Y").date(),
                                          info="Now we are even")

        jim_to_emma_dst = AccountMovement(account=emma_account,
                                          amount=20000,
                                          movement_type=MovementTypes.TRANSFER_DST,
                                          created=datetime.datetime.strptime('24052010',
                                                                             "%d%m%Y").date(),
                                          info="Now we are even")

        emma_to_steve_src = AccountMovement(account=emma_account,
                                            amount=-2500,
                                            movement_type=MovementTypes.TRANSFER_SRC,
                                            created=datetime.datetime.strptime('24052010',
                                                                               "%d%m%Y").date(),
                                            info="Flat rent")

        emma_to_steve_dst = AccountMovement(account=steve_account,
                                            amount=2500,
                                            movement_type=MovementTypes.TRANSFER_DST,
                                            created=datetime.datetime.strptime('24052010',
                                                                               "%d%m%Y").date(),
                                            info="Flat rent")

        emma_to_sara_src = AccountMovement(account=emma_account,
                                           amount=-3000,
                                           movement_type=MovementTypes.TRANSFER_SRC,
                                           created=datetime.datetime.strptime('24052010',
                                                                              "%d%m%Y").date(),
                                           info="Birthday!!")

        emma_to_sara_dst = AccountMovement(account=sara_account,
                                           amount=3000,
                                           movement_type=MovementTypes.TRANSFER_DST,
                                           created=datetime.datetime.strptime('24052010',
                                                                              "%d%m%Y").date(),
                                           info="Birthday!!")

        session.add_all([
            pankia_bank, santonder_bank, da_box_bank,
            steve_account, jim_account, emma_account, sara_account, john_account, ralph_account,
            jim_to_bank_mov,
            jim_to_emma_src, jim_to_emma_dst, emma_to_steve_src,emma_to_steve_dst, emma_to_sara_src, emma_to_sara_dst
        ])

        session.commit()

        self.session = session

    def test_model_loaded(self):
        data = []

        bank_schema = BankSchema()
        for b in self.session.query(Bank).all():
            data.append(bank_schema.dump(b).data)

        acc_schema = AccountSchema()
        for a in self.session.query(Account).all():
            data.append(acc_schema.dump(a).data)

        acc_movement_schema = AccountMovementSchema()
        for am in self.session.query(AccountMovement).all():
            data.append(acc_movement_schema.dump(am).data)

        # fp = open(os.path.join(self.data_folder, "loaded_data.json"), "w")
        # json.dump(data, fp=fp, indent=4, sort_keys=True)
        fp = open(os.path.join(self.data_folder, "loaded_data.json"), "r")
        expected = json.load(fp)
        self.assertCountEqual(data, expected)

    def test_account_totals(self):
        jim_id = self.session.query(Account.id).filter(Account.customer_name == 'Jim').first()[0]
        self.assertEqual(Operation(self.session).account_totals(jim_id), 30000)

        emma_id = self.session.query(Account.id).filter(Account.customer_name == 'Emma').first()[0]
        self.assertEqual(Operation(self.session).account_totals(emma_id), 14500)

    def test_account_list(self):
        emma_id = self.session.query(Account.id).filter(Account.customer_name == 'Emma').first()[0]
        movements = Operation(self.session).account_movements(emma_id)
        # fp = open(os.path.join(self.data_folder, "emma_movements.json"), "w")
        # json.dump(movements, fp=fp, indent=4, sort_keys=True)
        fp = open(os.path.join(self.data_folder, "emma_movements.json"), "r")
        expected = json.load(fp)
        self.assertCountEqual(movements, expected)

    def test_transfer_creation_from_local_bank(self):
        Operation(self.session).do_transfer(1, 1, 4, 100, "lol")

if __name__ == '__main__':
    unittest.main()
