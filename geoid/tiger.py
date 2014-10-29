"""
Classes for working with the geoids as they appear in the Tiger files, which omit the parts before 
the "us" string in the ACS form, usually starting with the state. 
"""

from . import base62_encode, base62_decode, Geoid, augment

class TigerGeoid(Geoid):

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}
    sl_width = 2
    width_pos = 2
    sl_format = ''
    elem_format = '{{{}:0{}d}}'
    sl_regex = ''
    elem_regex = '(?P<{}>.{{{}}})'
    encode = lambda x : x
    decode = lambda x : int(x)

# Really should use meta-classes here ...

class Region(TigerGeoid):

    region = None

    def __init__(self, region):
        super(Region,self).__init__(region=region)

class Division(TigerGeoid):

    region = None
    division = None

    def __init__(self, region, division):
        super(Region,self).__init__(region=region, division=division)

class State(TigerGeoid):

    state = None

    def __init__(self, state):
        super(Division,self).__init__(state=state)

class County(TigerGeoid):

    state = None
    county = None

    def __init__(self, state, county):
        super(County,self).__init__(state=state, county=county)


class Place(TigerGeoid):

    def __init__(self, place):
        super(Place,self).__init__(place=place)


class UrbanArea(TigerGeoid):

    def __init__(self, state, ua):
        super(UrbanArea,self).__init__(ua=ua)


class Tract(TigerGeoid):

    state = None
    county = None
    tract = None

    def __init__(self, state, county, tract):
        super(Tract,self).__init__(state=state, county=county, tract=tract)


class Blockgroup(TigerGeoid):

    state = None
    county = None
    tract = None
    blockgroup = None

    def __init__(self, state, county, tract, blockgroup):
        super(Blockgroup,self).__init__(state=state, county=county, tract=tract, blockgroup=blockgroup)

class Block(TigerGeoid):

    state = None
    county = None
    tract = None
    blockgroup = None

    def __init__(self, state, county, tract, blockgroup, block):
        super(Block,self).__init__(state=state, county=county, tract=tract, blockgroup=blockgroup, block=block)


augment(__name__, TigerGeoid)
