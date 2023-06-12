"""
An implementation of MutableAttr.
"""
from typing import TypeVar, Tuple, Dict, cast, Mapping, Optional, Any, Iterator
from attrdictionary.mixins import MutableAttr

__all__ = ["AttrMap"]
__v = TypeVar('__v')
_AttrMap__v = TypeVar('_AttrMap__v')

class AttrMap(MutableAttr[__v]):
    """
    An implementation of MutableAttr.
    """
    def __init__(self, items:Optional[Mapping[str, __v]]= None, sequence_type:type= tuple):
        if items is None:
            items = {}
        elif not isinstance(items, Mapping):
            items = dict(items)

        self._setattr("_sequence_type", sequence_type)
        self._setattr("_mapping", items)
        self._setattr("_allow_invalid_attributes", False)

    def _configuration(self):
        """
        The configuration for an attrmap instance.
        """
        return self._sequence_type

    def __getitem__(self, key:str) -> __v:
        """
        Access a value associated with a key.
        """
        __mapping:Mapping[str, __v] = self._mapping
        return __mapping[key]

    def __setitem__(self, key:str, value:Any):
        """
        Add a key-value pair to the instance.
        """
        self._mapping[key] = value

    def __delitem__(self, key):
        """
        Delete a key-value pair
        """
        del self._mapping[key]

    def __len__(self) -> int:
        """
        Check the length of the mapping.
        """
        return len(self._mapping)

    def __iter__(self) -> Iterator[__v]:
        """
        Iterated through the keys.
        """
        return iter(self._mapping)

    def __repr__(self):
        """
        Return a string representation of the object.
        """
        # sequence type seems like more trouble than it is worth.
        # If people want full serialization, they can pickle, and in
        # 99% of cases, sequence_type won't change anyway
        return f"AttrMap({repr(self._mapping)})"

    def __getstate__(self) -> Tuple[Dict[str, __v], type, bool]:
        """
        Serialize the object.
        """
        return (
            self._mapping,
            self._sequence_type,
            self._allow_invalid_attributes,
        )

    def __setstate__(self, state):
        """
        Deserialize the object.
        """
        mapping, sequence_type, allow_invalid_attributes = cast(Tuple[Dict[str, __v], type, bool], state)
        self._setattr("_mapping", mapping)
        self._setattr("_sequence_type", sequence_type)
        self._setattr("_allow_invalid_attributes", allow_invalid_attributes)

    @classmethod
    def _constructor(cls, mapping, configuration) -> "AttrMap[__v]":
        """
        A standardized constructor.
        """
        return cls(mapping, sequence_type=configuration)
