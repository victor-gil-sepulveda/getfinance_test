from sqlalchemy.sql.functions import func
from gf_test.model.model import AccountMovement
from gf_test.model.schemas import AccountMovementSchema


class Operation:

    def __init__(self, session):
        self.session = session

    def account_totals(self, acc_id):

        total = self.session.query(AccountMovement.account_id,
                                   func.sum(AccountMovement.amount).label("total"))\
                          .filter(AccountMovement.account_id == acc_id)\
                          .group_by(AccountMovement.account_id)\
                          .first()[1]
        return total

    def account_movements(self, acc_id):
        movements = self.session.query(AccountMovement) \
            .filter(AccountMovement.account_id == acc_id) \
            .all()
        acc_mov_schema = AccountMovementSchema()
        return [acc_mov_schema.dump(a).data for a in movements]
