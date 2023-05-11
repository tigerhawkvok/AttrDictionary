"""
dotdict contains several mapping objects that allow access to their
keys as attributes.
"""
from dotdict.default import AttrDefault
from dotdict.dictionary import AttrDict
from dotdict.mapping import AttrMap

__all__ = ["AttrMap", "AttrDict", "AttrDefault"]
