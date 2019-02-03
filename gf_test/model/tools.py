import datetime
import hashlib
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


#From https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    try:
                        fields[field] = data.id
                    except:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def parse_acc_number(acc_id):
    b_id, a_id = acc_id.split("-")
    return int(b_id), int(a_id)


def gen_transfer_id(src_acc_number, dst_acc_number):
    m = hashlib.sha256()
    m.update(src_acc_number+dst_acc_number+str(datetime.datetime.now()))
    return m.hexdigest()


