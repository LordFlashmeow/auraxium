from ..datatypes import CachableDataType
from ..misc import LocalizedString


class Title(CachableDataType):
    """A title.

    A player title a player can equip. The title id "0" signifies that the
    player has not selected any title.

    """

    _collection = 'title'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d['name'])
