from flask_restful import Resource
from flask import request

class BankTransfer(Resource):

    def __init__(self):
        pass

    def put(self, args):
        """
        Creates the needed movements for a transfer
        """
        json_data = request.get_json(force=True)

        # Is the src account in my bank?
        # if not, error

        # Is the other account in my bank?

        # if yes, issue an intra bank transfer


        # if not, start the inter bank procedure

