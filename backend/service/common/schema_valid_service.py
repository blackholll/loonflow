from service.base_service import BaseService
from schema import SchemaUnexpectedTypeError


class SchemaValidService(BaseService):

    @staticmethod
    def parse_integer_list(value):
        print("11111")
        if value is None:
            return
        else:
            try:
                return [int(item if item != "" else 0) for item in value]
            except Exception:
                raise MyCustomError("11111")

    @staticmethod
    def parse_str_list(value):
        return [str(item) for item in value]



class MyCustomError(Exception):
    pass