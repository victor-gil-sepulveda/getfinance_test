import json
import os
import shutil
import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from gf_test.model.model import Base, Bank
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
        session.add_all([
            Bank(name="Pankia"),
            Bank(name="Santonder"),
            Bank(name="DaBox")
        ])

        session.commit()
        self.session = session

    def test_AccountMovement(self):
        for b in self.session.query(Bank).filter():
            print b.name
            print json.dumps(b, cls=AlchemyEncoder)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
