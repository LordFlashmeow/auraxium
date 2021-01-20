"""Currency class definition."""

from ..base import Cached
from ..models import CurrencyData
from ..types import LocaleData


class Currency(Cached, cache_size=10, cache_ttu=3600.0):
    """A currency obtainable by characters."""

    collection = 'currency'
    data: CurrencyData
    dataclass = CurrencyData
    id_field = 'currency_id'

    # Type hints for data class fallback attributes
    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int
