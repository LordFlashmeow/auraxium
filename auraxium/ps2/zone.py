from ..census import Query
from ..datatypes import StaticDatatype
from .ability import Ability


class Zone(StaticDatatype):
    _collection = 'zone'

    def __init__(self, id):
        self.id = id

        data = Quest(self.__class__, id=id).get_single()
        self.code = data['code']
        self.description = data['description'][next(iter(data['description']))]
        self.hex_size = int(data['hex_size'])
        self.name = data['name'][next(iter(data['name']))]


class ZoneEffect(InterimDatatype):
    _cache_size = 100
    _collection = 'zone_effect'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.ability = Ability(data['ability_id'])
        self.type = ZoneEffectType(data['zone_effect_type_id'])
        self.parameters = {}
        self.strings = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass


class ZoneEffectType(StaticDatatype):
    _collection = 'zone_effect_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
        self.parameters = {}
        self.strings = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass