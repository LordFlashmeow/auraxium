from ..census import Query
from ..datatypes import EnumeratedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet


class Faction(EnumeratedDataType):
    """Represents a faction in PlanetSide 2.

    Factions are static datatypes. Each one should only need to be
    initialized once.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None
        self._image_id = None
        self._image_set_id = None
        self.is_playable = None
        self.tag = None

        # Define properties
        @property
        def image(self):
            try:
                return self._image
            except AttributeError:
                self._image = Image.get(cls=self.__class__, id=self._image_id)
                return self._image

        @property
        def image_set(self):
            try:
                return self._image_set
            except AttributeError:
                self._image_set = ImageSet.get(cls=self.__class__,
                                               id=self._image_set_id)
                return self._image_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d['name'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.is_playable = True if d['user_selectable'] == '1' else False
        # NOTE: As of the writing of this module, Nanite Systems does not have
        # a tag. As this might change with the introduction of combat robots, I
        # wrote this section in a way that should be able to handle that.
        self.tag = 'NS' if d['code_tag'] == 'None' else d['code_tag']
