from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from ..misc import LocalizedString
from .ability import Ability
from .faction import Faction
from .image import Image, ImageSet
from .skill import SkillSet
from .profile import Profile


class Item(CachableDataType):
    """A PS2 item.

    An item is a player-bound entity in the game world. This includes obvious
    examples like weapons or consumables, but also depot items like camo or
    cosmetics.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self._active_ability_id = None
        self.description = None
        self._faction_id = None
        self._image_id = None
        self._image_set_id = None
        self.is_default_attachment = None
        self.is_vehicle_weapon = None
        self.max_stack_size = None
        self.name = None
        self._passive_ability_id = None
        self._skill_set_id = None

        # Define properties
        @property
        def active_ability(self):
            try:
                return self._active_ability
            except AttributeError:
                self._active_ability = Ability.get(cls=self.__class__,
                                                   id=self._active_ability_id)
                return self._active_ability

        @property
        def attachments(self):
            try:
                return self._attachments
            except AttributeError:
                q = Query(type='item_attachment')
                d = q.add_filter(field='item_id', value=self.id).get()
                self._attachments = Item.list(cls=self.__class__,
                                              ids=[i['attachment_item_id'] for i in d])
                return self._attachments

        @property
        def faction(self):
            try:
                return self._faction
            except AttributeError:
                self._faction = Faction.get(cls=self.__class__,
                                            id=self._faction_id)
                return self._faction

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

        @property
        def passive_ability(self):
            try:
                return self._passive_ability
            except AttributeError:
                self._passive_ability = Ability.get(cls=self.__class__,
                                                    id=self._passive_ability_id)
                return self._passive_ability

        @property
        def profiles(self):
            try:
                return self._profiles
            except AttributeError:
                q = Query(type='item_profile')
                d = q.add_filter(field='item_id', value=self.id).get()
                self._profiles = Profile.list(cls=self.__class__, ids=[
                                              i['profile_id'] for i in d])
                return self._profiles

        @property
        def skill_set(self):
            try:
                return self._skill_set
            except AttributeError:
                self._skill_set = SkillSet.get(
                    cls=self.__class__, id=self._skill_set_id)
                return self._skill_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self._active_ability_id = d.get('activatable_ability_id')
        self.description = LocalizedString(d['description'])
        self._faction_id = d['faction_id']
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.is_default_attachment = d['is_default_attachment']
        self.is_vehicle_weapon = d['is_vehicle_weapon']
        self.max_stack_size = d['max_stack_size']
        self.name = LocalizedString(d['name'])
        self._passive_ability_id = d.get('passive_ability_id')
        self._skill_set_id = d.get('skill_set_id')


class ItemCategory(EnumeratedDataType):
    """The category of an item.

    Groups items into groups.
    Examples include "Knife", "Assault Rifle" or "VO Pack".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

        # Define properties
        @property
        def items(self):
            """Returns a list of all items that belong to this category."""
            try:
                return self._items
            except AttributeError:
                q = Query(type='item')
                d = q.add_filter(field='item_category', value=self.id).get()
                self._items = Item.list(cls=self.__class__, ids=[
                                        i['item_id'] for i in d])
                return self._items

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d['name'])


class ItemType(EnumeratedDataType):
    """The type of item.

    This includes entries like "Attachment" or "Weapon", but also abstract
    objects like "Give Currency" or "Reward Set".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.code = None
        self.name = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.code = d['code']
        self.name = d['name']
