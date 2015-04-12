"""Geoids for the decenial census"""

from . import base62_encode, base62_decode, Geoid, make_classes
import sys

class CensusGeoid(Geoid):

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}
    name_map = {}

    sl_width = 3
    width_pos = 1
    sl_format = '' # The '00' bit is for the geo component, always 00 in our use.
    elem_format = '{{{}:0{}d}}'
    sl_regex = ''
    elem_regex = '(?P<{}>.{{{}}})'
    encode = lambda x: int(x)
    decode = lambda x: int(x)

    @classmethod
    def class_factory(cls, name):
        def __init__(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)

        return type(name, (cls,), {"__init__": __init__})


make_classes(CensusGeoid, sys.modules[__name__])