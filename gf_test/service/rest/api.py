from flask_restful import Api

from gf_test.service.rest import v1
from gf_test.service.rest.tools import API_PREFIX


def get_version(version_module):
    name = version_module.__name__
    return name.split(".")[-1]


def gen_resource_url(api_prefix, version_module, resource_name):
    url_parts = [api_prefix, get_version(version_module), resource_name]
    return "/"+"/".join(url_parts)


def setup_rest_api(flask_app):
    api = Api(flask_app)

    version = v1

    api.add_resource(version.Account,
                     gen_resource_url(API_PREFIX, version, "account/<account_id>"))

    api.add_resource(version.AccountMovements,
                     gen_resource_url(API_PREFIX, version, "/<account_id>/list"))

    api.add_resource(version.BankTransfer,
                     gen_resource_url(API_PREFIX, version, "/transfer"))

    api.add_resource(version.OneSideBankTransfer,
                     gen_resource_url(API_PREFIX, version, "/transfer_one_side"))

    api.add_resource(version.AddFunds,
                     gen_resource_url(API_PREFIX, version, "/<account_id>/add"))

    api.add_resource(version.RemoveFunds,
                     gen_resource_url(API_PREFIX, version, "/<account_id>/retire"))

