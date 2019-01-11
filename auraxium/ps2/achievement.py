from ..census import Query
from ..datatypes import InterimDatatype
from .image import Image, ImageSet
from .item import Item
# from .objective import ObjectiveSet
from .reward import Reward


class Achievement(InterimDatatype):
    """An achievement in PlanetSide 2.

    An achievement is a blanket term covering both weapon medals and service
    ribbons.

    """

    # Since achievements are quite light-weight and cannot be resolved further,
    # their cache size can be safely increased.
    _cache_size = 100
    _collection = 'achievement'

    def __init__(self, id):
        self.id = id
        data = super(Achievement, self).get_data(self)

        self.description = data.get('description')
        self.item = Item(data.get('item_id'))
        self.image = Image(data.get('image_id'), path=data.get('image_path'))
        self.image_set = ImageSet(data.get('image_set_id'))
        self.name = data.get('name')
        # self.objective_group = None  # Identical to objective_set?
        self.repeatable = data.get('repeatable')
        self.reward = Reward(data.get('reward_id'))

    def __str__(self):
        return 'Achievement (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
