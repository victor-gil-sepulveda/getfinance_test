from flask_restful import Resource


class AccountMovements(Resource):

    def __init__(self):
        pass

    def get(self, account_id):
        pass

    def post(self):
        """
        Adds an account movement to the bank account.
        """
