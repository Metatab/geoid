"""
Classes for working with the geoids as they appear in the Tiger files, which omit the parts before 
the "us" string in the ACS form, usually starting with the state. 
"""

from . import base62_decode, Geoid, make_classes
from .core import base62_encode, base62_decode, make_classes, Geoid
import sys

class TigerGeoid(Geoid):

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}
    name_map = {}

    sl_width = 2
    width_pos = 1
    sl_format = ''
    elem_format = '{{{}:0{}d}}'
    elem_str_format = '{{{}:s}}'
    sl_regex = ''
    elem_regex = '(?P<{}>.{{{}}})'
    encode = lambda x : int(x)
    decode = lambda x : int(x)

    @classmethod
    def part_width(cls, dec_width):
        return dec_width

    @classmethod
    def class_factory(cls, name):

        def __init__(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)

        return type(name, (cls,), {"__init__": __init__})


make_classes(TigerGeoid, sys.modules[__name__])