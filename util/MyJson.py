import json


class MyJSONEncoder(json.JSONEncoder):
    """
    New JSONEcoder to handle ObjectId object
    """
    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)