from sqlalchemy.sql.functions import func
from gf_test.model.model import AccountMovement, Account, MovementTypes, Transfer
from gf_test.model.schemas import AccountMovementSchema, AccountSchema
from sqlalchemy import or_


class Operation:

    def __init__(self, session_creator):
        self.Session = session_creator

    def account_details(self, acc_id):
        """
        Retrieves the details of an account or None if we cannot find it
        """
        session = self.Session()
        account = session.query(Account)\
                         .filter(Account.id == acc_id)\
                         .first()

        acc_schema = AccountSchema()
        details = acc_schema.dump(account).data
        if details == {}:
            return None
        else:
            return details

    def account_totals(self, acc_id):
        """
        Retrieves the total amount of money in one bank account with id = acc_id
        """
        session = self.Session()
        total = session.query(AccountMovement.account_id,
                              func.sum(AccountMovement.amount).label("total"))\
                       .filter(AccountMovement.account_id == acc_id)\
                       .group_by(AccountMovement.account_id)\
                       .first()[1]
        return total

    def account_movements(self, acc_id):
        """
        Retrieves the list of all movements bound to the account with id = acc_id
        """
        session = self.Session()
        movements = session.query(AccountMovement) \
                           .filter(AccountMovement.account_id == acc_id) \
                           .all()
        acc_mov_schema = AccountMovementSchema()
        return [acc_mov_schema.dump(a).data for a in movements]

    def do_intra_transfer(self, src_acc_id, dst_acc_id, amount, info):
        """
        """

        src_movement = AccountMovement(account_id=src_acc_id,
                                       amount=-amount,
                                       movement_type=MovementTypes.TRANSFER_SRC,
                                       info=info)

        dst_movement = AccountMovement(account_id=dst_acc_id,
                                       amount=amount,
                                       movement_type=MovementTypes.TRANSFER_DST,
                                       info=info)

        session = self.Session()
        session.add(src_movement)
        session.add(dst_movement)
        session.commit()

    def do_inter_transfer(self, issuing_bank_id,
                          acc_id, bank_id,
                          src_account_number,
                          dst_account_number,
                          transfer_id,
                          amount, info):
        """
        """
        session = self.Session()

        if issuing_bank_id == bank_id:
            local_movement = AccountMovement(account_id=acc_id,
                                             amount=-amount,
                                             movement_type=MovementTypes.TRANSFER_SRC,
                                             info=info)

            cost = AccountMovement(account_id=acc_id,
                                   amount=-amount,
                                   movement_type=MovementTypes.BANK_EXPENSE,
                                   info="Transfer costs")

            transfer_side = Transfer(transfer_id=transfer_id,
                                     src_account_number=src_account_number,
                                     dst_account_number=dst_account_number,
                                     local_movement=local_movement,
                                     cost=cost)
            session.add(local_movement)
            session.add(cost)
            session.add(transfer_side)

        if issuing_bank_id != bank_id:
            local_movement = AccountMovement(account_id=acc_id,
                                             amount=amount,
                                             movement_type=MovementTypes.TRANSFER_DST,
                                             info=info)

            transfer_side = Transfer(transfer_id=transfer_id,
                                     src_account_number=src_account_number,
                                     dst_account_number=dst_account_number,
                                     local_movement=local_movement)

            session.add(local_movement)
            session.add(transfer_side)

        session.commit()
