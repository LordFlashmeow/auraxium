"""Defines player-state-related data types for PlanetSide 2."""

from ...base_api import Query
from ..datatypes import DataType


class PlayerState(DataType):
    """A player state.

    Used to handle changing cone of fires and other fields based on what the
    player is doing.

    """

    _collection = 'player_state'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')


class PlayerStateGroup(DataType):
    """Controls CoF modifiers depending on what the player is doing.

    I inferred `player_state_group_2` is a complete replacement for
    `player_state_group`, this might require correcting if I am wrong.

    """

    _collection = 'player_state_group_2'
    _id_field = 'player_state_group_id'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._player_states = None  # Internal (See properties)

    # Define properties
    @property
    def player_states(self):
        """A list of player states that art in this group."""
        try:
            return self._player_states
        except AttributeError:
            data = Query('player_state_group_2', player_state_group_id=self.id_).limit(6).get()
            self._player_states = [PlayerStateGroupEntry(data=ps) for ps in data]
            self._player_states.sort(key=lambda ps: ps.player_state_id)
            return self._player_states

    def populate(self, data=None):
        # Do nothing; just here for technicalities' sake
        pass


class PlayerStateGroupEntry():  # pylint: disable=too-many-instance-attributes, too-few-public-methods
    """An entry within a player state group."""

    def __init__(self, data):
        # Set attribute values
        self.can_iron_sight = data.get('can_iron_sight')
        self.cof_grow_rate = data.get('cof_grow_rate')  # bloom?
        self.cof_max = data.get('cof_max')
        self.cof_min = data.get('cof_min')
        self.cof_recovery_delay = data.get('cof_recovery_delay')
        self.cof_recovery_rate = data.get('cof_recovery_rate')
        self.cof_shots_before_penalty = data.get('cof_shots_before_penalty')
        self.cof_recovery_delay_threshold = data.get(
            'cof_recovery_delay_threshold')
        self.cof_turn_penalty = data.get('cof_turn_penalty')
        self.player_state_id = data.get('player_state_id')

    @property
    def player_state(self):
        """Returns the corresponding player state."""
        return PlayerState.get(id_=self.player_state_id)
