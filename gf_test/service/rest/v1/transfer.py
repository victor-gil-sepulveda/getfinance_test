from flask_restful import Resource
from flask import request

from gf_test.model.operation import Operation
from gf_test.model.tools import parse_acc_number, gen_transfer_id
from gf_test.service.rest import v1
from gf_test.service.rest.errorcode import ErrorCode
from gf_test.service.rest.restmethod import RestMethod
from gf_test.service.rest.status import Status
from gf_test.service.rest.tools import do_request, ep_url


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
        src_acc_number = json_data["source"]
        try:
            src_bank_id, src_acc_id = parse_acc_number(src_acc_number)
        except ValueError:
            return {
                "status": Status.ERROR,
                "error_code": ErrorCode.Transfer.BAD_SRC_ACCOUNT_NUMBER
            }
        src_acc_details = Operation(self.Session).account_details(src_acc_id)
        if src_acc_details is None:
            return {
                "status": Status.ERROR,
                "error_code": ErrorCode.ACCOUNT_NOT_FOUND
            }

        # Is the other account in my bank?
        dst_acc_number = json_data["destination"]
        try:
            dst_bank_id, dst_acc_id = parse_acc_number(dst_acc_number)
        except ValueError:
            return {
                "status": Status.ERROR,
                "error_code": ErrorCode.Transfer.BAD_DST_ACCOUNT_NUMBER
            }
        dst_acc_details = Operation(self.Session).account_details(dst_acc_id)

        # if yes, issue an intra bank transfer (2 movements)
        if dst_acc_details is not None:
            Operation(self.Session).do_intra_transfer(src_acc_id, dst_acc_id,
                                                      json_data["amount"], json_data["info"])
        else:
            # if not, start the inter bank procedure
            if json_data["amount"] > 2000.:
                return {
                    "status": Status.ERROR,
                    "error_code": ErrorCode.Transfer.AMOUNT_EXCEEDED
                }

            # Find the other account
            # Get the bank url

            # Ask for the details
            #TODO: we will assume this step is OK (the other bank owns this account)

            # Perform one side transfer and get the id
            transfer_id = gen_transfer_id(json_data["source"], json_data["destination"])

            # Perform one side transfer
            Operation(self.Session).do_inter_transfer(
                            issuing_bank_id=src_bank_id,
                            acc_id=src_acc_id,
                            bank_id=src_bank_id,
                            src_account_number=src_acc_details,
                            dst_account_number=dst_acc_details,
                            transfer_id=transfer_id,
                            amount=json_data["amount"],
                            info=json_data["info"])

            # Perform the other side (in the other bank DB)
            # Gt the other bank url
            bank_url = ...

            # generate the endpoint
            transfer_endpoint = ep_url(bank_url, "transfer_one_side", v1)

            data = {
                "issuing_bank_id": src_bank_id,
                "acc_id": dst_acc_id,
                "src_account_number": src_acc_number,
                "dst_account_number": dst_acc_number,
                "transfer_id": transfer_id,
                "amount": json_data["amount"],
                "info": json_data["info"]
            }

            do_request(transfer_endpoint, RestMethod.PUT, data=data)

            # We assume this is alwais OK
            # TODO: CHECK

class OneSideBankTransfer(Resource):

    def __init__(self, session_maker):
        self.Session = session_maker

    def put(self):
        json_data = request.get_json(force=True)
        Operation(self.Session).do_inter_transfer(**json_data)
