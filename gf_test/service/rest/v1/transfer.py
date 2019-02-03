from flask_restful import Resource
from flask import request

from gf_test.model.operation import Operation
from gf_test.service.rest.errorcode import ErrorCode
from gf_test.service.rest.status import Status


class BankTransfer(Resource):

    def __init__(self, session_maker):
        self.Session = session_maker

    def put(self):
        """
        Creates the needed movements for a transfer
        """
        json_data = request.get_json(force=True)

        # Is the src account in my bank?
        # if not, error
        src_acc_details = Operation(self.Session).account_details(json_data["source"])
        if src_acc_details is None:
            return {
                "status": Status.ERROR,
                "error_code": ErrorCode.ACCOUNT_NOT_FOUND
            }

        # Is the other account in my bank?
        dst_acc_details = Operation(self.Session).account_details(json_data["source"])

        # if yes, issue an intra bank transfer (2 movements)
        if dst_acc_details is not None:
            Operation(self.Session).do_intra_transfer(json_data["source"], json_data["destination"],
                                                      json_data["amount"], json_data["info"])
        else:
            # if not, start the inter bank procedure
            if json_data["amount"] > 2000.:
                return {
                    "status": Status.ERROR,
                    "error_code": ErrorCode.Transfer.AMOUNT_EXCEEDED
                }

            # Find the other account