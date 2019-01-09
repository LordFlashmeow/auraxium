from ..census import Query
from ..datatypes import StaticDatatype


class Server(StaticDatatype):
    _collection = 'world'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.name = data['name'][next(iter(data['name']))]

        @property
        def status(self):
            # perform request to get current state
            pass