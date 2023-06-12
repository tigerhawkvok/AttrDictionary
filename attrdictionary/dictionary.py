"""
A dict that implements MutableAttr.
"""
from typing import TypeVar, Tuple, Dict, cast, Mapping
from attrdictionary.mixins import MutableAttr

__all__ = ["AttrDict"]
__v = TypeVar('__v')
_AttrDict__v = TypeVar('_AttrDict__v')
#  -> "AttrDict[__k, __v]"

class AttrDict(dict, MutableAttr[__v]):
    """
    A dict that implements MutableAttr.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setattr('_sequence_type', tuple)
        self._setattr('_allow_invalid_attributes', False)
        # self.__sequenceType:type = tuple
        # self.__allowInvalid:bool = False

    # @property
    # def _sequence_type(self) -> type:
    #     return self.__sequenceType

    # @_sequence_type.setter
    # def _sequence_type(self, value:type):
    #     # if not isinstance(value, type):
    #     #     raise TypeError(f"sequence_type must be a type (got {type(value)})")
    #     self.__sequenceType = value

    # @property
    # def _allow_invalid_attributes(self) -> bool:
    #     return self.__allowInvalid

    def _configuration(self) -> type:
        """
        The configuration for an attrmap instance.
        """
        return self._sequence_type

    def __getstate__(self) -> Tuple[Dict[str, __v], type, bool]:
        """
        Serialize the object.
        """
        return (
            self.copy(),
            self._sequence_type,
            self._allow_invalid_attributes,
        )

    def __setstate__(self, state):
        """
        Deserialize the object.
        """
        mapping, sequence_type, allow_invalid_attributes = cast(Tuple[Dict[str, __v], type, bool], state)
        self.update(mapping)
        # self.__sequenceType = sequence_type
        # self.__allowInvalid = allow_invalid_attributes
        self._setattr('_sequence_type', sequence_type)
        self._setattr('_allow_invalid_attributes', allow_invalid_attributes)

    def __repr__(self):
        return "AttrDict({contents})".format(
            contents=super().__repr__(),
        )

    @classmethod
    def _constructor(cls, mapping:Mapping[str, __v], configuration:type) -> "AttrDict[__v]":
        """
        A standardized constructor.
        """
        attr = cls(mapping)
        # attr._sequenceType = configuration
        attr._setattr('_sequence_type', configuration)

        return attr
