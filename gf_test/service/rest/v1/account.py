from flask_restful import Resource

from gf_test.model.operation import Operation
from gf_test.service.rest.errorcode import ErrorCode
from gf_test.service.rest.status import Status


class Account(Resource):

    def __init__(self, session_maker):
        self.Session = session_maker

    def get(self, account_id):
        """
        Gets the details of a given account or an error if the account is not in
        the bank.
        """
        details = Operation(self.Session).account_details(account_id)

        if details is not None:
            details["status"] = Status.OK
        else:
            details = {
                "status": Status.ERROR,
                "error_code": ErrorCode.ACCOUNT_NOT_FOUND
            }

        return details
