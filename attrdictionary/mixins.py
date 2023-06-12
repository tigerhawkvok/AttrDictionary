"""
Mixin Classes for Attr-support.
"""
import re
from abc import abstractmethod
from typing import Any, TypeVar, Union, overload, Tuple, Mapping, MutableMapping, Sequence

from attrdictionary.merge import merge

__all__ = ["Attr", "MutableAttr"]
__v = TypeVar('__v')
_Attr__v = TypeVar('_Attr__v')

class Attr(Mapping[str, __v]):
    """
    A mixin class for a mapping that allows for attribute-style access
    of values.

    A key may be used as an attribute if:
     * It is a string
     * It matches /^[A-Za-z][A-Za-z0-9_]*$/ (i.e., a public attribute)
     * The key doesn't overlap with any class attributes (for Attr,
        those would be 'get', 'items', 'keys', 'values', 'mro', and
        'register').

    If a values which is accessed as an attribute is a Sequence-type
    (and is not a string/bytes), it will be converted to a
    _sequence_type with any mappings within it converted to Attrs.

    NOTE: This means that if _sequence_type is not None, then a
        sequence accessed as an attribute will be a different object
        than if accessed as an attribute than if it is accessed as an
        item.
    """
    @abstractmethod
    def _configuration(self):
        """
        All required state for building a new instance with the same
        settings as the current object.
        """

    @classmethod
    def _constructor(cls, mapping, configuration) -> "Attr[__v]":
        """
        A standardized constructor used internally by Attr.

        mapping: A mapping of key-value pairs. It is HIGHLY recommended
            that you use this as the internal key-value pair mapping, as
            that will allow nested assignment (e.g., attr.foo.bar = baz)
        configuration: The return value of Attr._configuration
        """
        raise NotImplementedError("You need to implement this")

    def __call__(self, key:str) -> __v:
        """
        Dynamically access a key-value pair.

        key: A key associated with a value in the mapping.

        This differs from __getitem__, because it returns a new instance
        of an Attr (if the value is a Mapping object).
        """
        if key not in self:
            raise AttributeError(
                "'{cls} instance has no attribute '{name}'".format(
                    cls=self.__class__.__name__, name=key,
                ),
            )

        return self._build(self[key])

    def __getattr__(self, key:str) -> __v:
        """
        Access an item as an attribute.
        """
        if key not in self or not self._valid_name(key):
            raise AttributeError(
                "'{cls}' instance has no attribute '{name}'".format(
                    cls=self.__class__.__name__, name=key,
                ),
            )

        return self._build(self[key])

    def __add__(self, other:Mapping[str, Any]) -> "Attr[Any]":
        """
        Add a mapping to this Attr, creating a new, merged Attr.

        other: A mapping.

        NOTE: Addition is not commutative. a + b != b + a.
        """
        if not isinstance(other, Mapping):
            return NotImplemented

        return self._constructor(merge(self, other), self._configuration())

    def __radd__(self, other:Mapping[str, Any]) -> "Attr[Any]":
        """
        Add this Attr to a mapping, creating a new, merged Attr.

        other: A mapping.

        NOTE: Addition is not commutative. a + b != b + a.
        """
        if not isinstance(other, Mapping):
            return NotImplemented

        return self._constructor(merge(other, self), self._configuration())

    @overload
    def _build(self, obj:Union[str, bytes]) -> Union[str, bytes]: ...
    @overload
    def _build(self, obj:Sequence[__v]) -> Tuple[__v]: ...
    @overload
    def _build(self, obj:Mapping[str, __v]) -> "Attr[__v]": ...
    @overload
    def _build(self, obj:Any) -> Any: ...
    def _build(self, obj:Union[Sequence, Mapping[str, Any], Any]):
        """
        Conditionally convert an object to allow for recursive mapping
        access.

        obj: An object that was a key-value pair in the mapping. If obj
            is a mapping, self._constructor(obj, self._configuration())
            will be called. If obj is a non-string/bytes sequence, and
            self._sequence_type is not None, the obj will be converted
            to type _sequence_type and build will be called on its
            elements.
        """
        if isinstance(obj, Mapping):
            obj = self._constructor(obj, self._configuration())
        elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
            sequence_type = getattr(self, "_sequence_type", None)
            if sequence_type:
                obj = sequence_type(self._build(element) for element in obj)

        return obj

    @classmethod
    def _valid_name(cls, key:str) -> bool:
        """
        Check whether a key is a valid attribute name.

        A key may be used as an attribute if:
         * It is a string
         * It matches /^[A-Za-z][A-Za-z0-9_]*$/ (i.e., a public attribute)
         * The key doesn't overlap with any class attributes (for Attr,
            those would be 'get', 'items', 'keys', 'values', 'mro', and
            'register').
        """
        return (
                isinstance(key, str)  and
                (re.match("^[A-Za-z][A-Za-z0-9_]*$", key) is not None) and
                not hasattr(cls, key)
        )


class MutableAttr(Attr[__v], MutableMapping):
    """
    A mixin class for a mapping that allows for attribute-style access
    of values.
    """
    def _setattr(self, key:str, value:Any):
        """
        Add an attribute to the object, without attempting to add it as
        a key to the mapping.
        """
        super().__setattr__(key, value)

    def __setattr__(self, key:str, value:Any):
        """
        Add an attribute.

        key: The name of the attribute
        value: The attributes contents
        """
        if self._valid_name(key):
            self[key] = value
        elif getattr(self, "_allow_invalid_attributes", True):
            self._setattr(key, value)
        else:
            raise TypeError(
                f"'{self.__class__.__name__}' does not allow attribute creation. (attempted {key} = {value})",
            )

    def _delattr(self, key:str):
        """
        Delete an attribute from the object, without attempting to
        remove it from the mapping.
        """
        super().__delattr__(key)

    def __delattr__(self, key:str):
        """
        Delete an attribute.

        key: The name of the attribute
        """
        if self._valid_name(key):
            del self[key]
        elif getattr(self, "_allow_invalid_attributes", True):
            super().__delattr__(key)
        else:
            raise TypeError(
                f"'{self.__class__.__name__}' does not allow attribute deletion.",
            )
