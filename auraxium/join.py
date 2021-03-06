from typing import Tuple, Union

from .census import List, Term, SearchModifier, generate_term
from .log import logger
from .type import CensusValue


class Join():
    """Represents an inner (or joined) query.

    Created by the `Query.join()` and `Join.join()` methods.
    Do not instantiate manually.
    """

    def __init__(self, collection: str, inject_at: str = '',
                 is_list: bool = False, on: str = '', is_outer: bool = True,
                 to: str = '', show: List[str] = None, hide: List[str] = None,
                 **kwargs: CensusValue) -> None:
        """Initializer."""

        self.collection = collection
        self._inner_joins: List['Join'] = []
        self.is_list = is_list
        self.is_outer = is_outer
        self.inject_at = inject_at
        self.parent_field = on
        self.child_field = to
        self.show = [] if show is None else show
        self.hide = [] if hide is None else hide
        # Additional kwargs are passed on to the `add_term` method
        self.terms: List[Term] = []

        for field, value in kwargs.items():
            self.terms.append(generate_term(field.replace('__', '.'), value))

    def add_term(self, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO) -> 'Join':
        """Add a search term to this join.

        Any results returned by a join must meet every term defined
        for it.
        """

        new_term = Term(field, value, modifier)
        self.terms.append(new_term)
        return self

    def set_hide(self, *args: Union[str, List[str]]) -> 'Join':
        """Hide the given field names from the response."""
        self.hide = list(args)
        if self.hide and self.show:
            logger.warning('"Show" will take precedent over "hide".')
        return self

    def join(self, collection: str, inject_at: str = '',
             is_list: bool = False, on: str = '', is_outer: bool = True,
             to: str = '', **kwargs: Tuple[str, CensusValue]) -> 'Join':
        """Create an inner join for this join.

        All arguments passed to this function are forwarded to the new
        Join's initializer. The created join is returned.
        """
        inner_join = Join(collection, inject_at, is_list,
                          on, is_outer, to, **kwargs)
        self._inner_joins.append(inner_join)
        return inner_join

    def set_show(self, *args: Union[str, List[str]]) -> 'Join':
        """Only include the given field names in the response."""
        self.show = list(args)
        if self.hide and self.show:
            logger.warning('"Show" will take precedent over "hide".')
        return self

    def terms(self, *args: Term) -> 'Join':
        """Apply the given list of terms to the join."""
        self.terms = list(args)
        return self

    def process_join(self) -> str:
        """Process the join and return its string representation.

        This also recursively processes any inner joins.
        """
        # The collection (sometimes referred to a "type" in the docs) of the join
        string = self.collection
        # Keys
        if self.is_list:
            string += '^list:1'
        if not self.is_outer:
            string += '^outer:0'
        if self.inject_at:
            string += '^inject_at:' + self.inject_at
        if self.parent_field:
            string += '^on:' + self.parent_field
        if self.child_field:
            string += '^to:' + self.child_field
        # Show & hide
        if self.show:
            string += '^show:' + "'".join(self.show)
            if self.hide:
                logger.warning('"c:show" overwrites "c:hide"')
        elif self.hide:
            string += '^hide:' + "'".join(self.hide)
        # Terms
        if self.terms:
            string += '^terms:' + '\''.join([t.to_url() for t in self.terms])
        # Process inner joins
        if self._inner_joins:
            string += '('
            string += ','.join(j.process_join() for j in self._inner_joins)
            string += ')'
        return string
