from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from gf_test.model.model import Account, Bank, AccountMovement, Transfer


class RecBankSchema(ModelSchema):
    accounts = fields.Nested("AccountSchema", many=False)

    class Meta:
        model = Bank


class RecAccountSchema(ModelSchema):
    bank = fields.Nested("BankSchema", many=False)

    class Meta:
        model = Account


class RecAccountMovementSchema(ModelSchema):
    account = fields.Nested("AccountSchema", many=False)

    class Meta:
        model = AccountMovement


class RecTransferSchema(ModelSchema):
    src_accmov = fields.Nested("AccountMovementSchema", many=False)
    dst_accmov = fields.Nested("AccountSchema", many=False)

    class Meta:
        model = Transfer


class BankSchema(ModelSchema):

    class Meta:
        model = Bank


class AccountSchema(ModelSchema):

    class Meta:
        model = Account


class AccountMovementSchema(ModelSchema):

    class Meta:
        model = AccountMovement


class TransferSchema(ModelSchema):

    class Meta:
        model = Transfer
