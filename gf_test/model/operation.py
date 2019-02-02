from sqlalchemy.sql.functions import func
from gf_test.model.model import AccountMovement, Account, MovementTypes
from gf_test.model.schemas import AccountMovementSchema
from sqlalchemy import or_

class Operation:

    def __init__(self, session):
        self.session = session

    def account_totals(self, acc_id):
        """
        Retrieves the total amount of money in one bank account with id = acc_id
        """
        total = self.session.query(AccountMovement.account_id,
                                   func.sum(AccountMovement.amount).label("total"))\
                          .filter(AccountMovement.account_id == acc_id)\
                          .group_by(AccountMovement.account_id)\
                          .first()[1]
        return total

    def account_movements(self, acc_id):
        """
        Retrieves the list of all movements bound to the account with id = acc_id
        """
        movements = self.session.query(AccountMovement) \
            .filter(AccountMovement.account_id == acc_id) \
            .all()
        acc_mov_schema = AccountMovementSchema()
        return [acc_mov_schema.dump(a).data for a in movements]

    def do_transfer(self, local_bank_id, src_acc_id, dst_acc_id, amount, info):
        """
        Creates a money transfer between bank accounts.
        Only checks for trivial errors (will not check for instance if local_bank_id is one
        of the banks in src/dst accounts).

        :param local_bank_id: The id of the bank issuing the transfer
        :param src_acc_id: The id of the account sending the money
        :param dst_acc_id: The id of the account that will receive the money
        :param amount: The quantity that will be transferred
        :param info: A string containing the user-defined info on the transfer operation
        :return: Empty string or a string containing an error message (if the operation failed).
        """

        # result = self.session.query(Account.bank_id) \
        #     .filter(or_(Account.id == src_acc_id, Account.id == dst_acc_id)) \
        #     .all()

        src_bank = self.session.query(Account.bank_id) \
            .filter(Account.id == src_acc_id) \
            .first()[0]

        dst_bank = self.session.query(Account.bank_id) \
            .filter(Account.id == dst_acc_id) \
            .first()[0]

        if src_bank == local_bank_id:

            src_movement = AccountMovement(account_id=src_acc_id,
                                           amount=-amount,
                                           movement_type=MovementTypes.TRANSFER_SRC,
                                           info=info)

            if src_bank != dst_bank:
                bank_expenses = AccountMovement(account_id=src_acc_id,
                                                amount=-2.5,
                                                movement_type=MovementTypes.BANK_EXPENSE,
                                                info="Transfer cost")
                self.session.add(bank_expenses)

            self.session.add(src_movement)

        else:
            dst_movement = AccountMovement(account_id=dst_acc_id,
                                           amount=amount,
                                           movement_type=MovementTypes.TRANSFER_DST,
                                           info=info)

            self.session.add(dst_movement)

        self.session.commit()
