from flask_restful import Resource
from

from gf_test.model.model import AccountMovement


class AccountMovements(Resource):

    def __init__(self):
        pass

    def get(self, account_id):
        # Get all movements for an account id
        movements = AccountMovement.query\
            .filter((AccountMovement.src_account_id == account_id \
                    or AccountMovement.src_account_id == account_id))

        for movement in movements:
            # serialize every movement
