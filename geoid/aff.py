
from geoid.core import base62_encode, base62_decode, make_classes, Geoid
import sys
from .acs import mostly_int

def mostly_int(v):
    try:
        return int(v)
    except ValueError:
        return v

class AffGeoid(Geoid):
    """American Fact Finder Geoid?

    This geoid appears in the reduced cartographic boundary files, from:

    https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html


    """

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}
    name_map = {}

    sl_width = 3

    sl_format = '{sl:0>3d}00000US'
    elem_format = '{{{}:0{}d}}'
    elem_str_format = '{{{}:0>{}}}'
    sl_regex = '(?P<sl>.{3})....US'
    elem_regex = '(?P<{}>.{{{}}})'
    encode = mostly_int
    decode = mostly_int

    @classmethod
    def part_width(cls, dec_width):
        return dec_width

    @classmethod
    def class_factory(cls, name):
        def __init__(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)

        return type(name, (cls,), {"__init__": __init__})

    def summarize(self):
        """Convert all of the values to their max values. This form is used to represent the summary level"""

        s = str(self.allval())

        return self.parse(s[:7] + ''.join(['9'] * len(s[7:])))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __ge__(self, other):
        return str(self) >= str(other)


make_classes(AffGeoid, sys.modules[__name__])