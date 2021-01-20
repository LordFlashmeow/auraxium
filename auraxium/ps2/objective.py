"""Objective class definitions."""

from typing import Optional
from ..base import Cached
from ..census import Query
from ..models import ObjectiveData, ObjectiveTypeData
from ..proxy import InstanceProxy


class ObjectiveType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of objective.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'objective_type'
    data: ObjectiveTypeData
    dataclass = ObjectiveTypeData
    id_field = 'objective_type_id'

    # Type hints for data class fallback attributes
    objective_type_id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]


class Objective(Cached, cache_size=10, cache_ttu=60.0):
    """A objective presented to a character."""

    collection = 'objective'
    data: ObjectiveData
    dataclass = ObjectiveData
    id_field = 'objective_id'

    # Type hints for data class fallback attributes
    objective_id: int
    objective_type_id: int
    objective_group_id: int
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]

    def type(self) -> InstanceProxy[ObjectiveType]:
        """Return the objective type of this objective."""
        query = Query(
            ObjectiveType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ObjectiveType.id_field, value=self.data.objective_type_id)
        return InstanceProxy(ObjectiveType, query, client=self._client)
