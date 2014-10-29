"""
The Civic Knowledge geoid, a gvid, is  very similar to the census versions, but
expresses numbers in base 62 and includes other important values. 
"""

from . import base62_encode, base62_decode, Geoid, augment

class GVid(Geoid):

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}

    sl_width = 2
    sl_format = '{sl:0>2s}'
    elem_format = '{{{}:0>{}s}}'
    sl_regex = '(?P<sl>.{2})'
    elem_regex = '(?P<{}>.{{{}}})'
    width_pos = 1
    encode = base62_encode
    decode = base62_decode

class Region(GVid):

    region = None

    def __init__(self, region):
        super(Region,self).__init__(region=region)

class Division(GVid):

    region = None
    division = None

    def __init__(self, region, division):
        super(Region,self).__init__(region=region, division=division)

class State(GVid):

    state = None

    def __init__(self, state):
        super(Division,self).__init__(state=state)

class County(GVid):

    state = None
    county = None

    def __init__(self, state, county):
        super(County,self).__init__(state=state, county=county)


class Place(GVid):

    def __init__(self, place):
        super(Place,self).__init__(place=place)

        
class UrbanArea(GVid):
    
    def __init__(self, state, ua):
        super(UrbanArea,self).__init__(ua=ua)


class Tract(GVid):

    state = None
    county = None
    tract = None

    def __init__(self, state, county, tract):
        super(Tract,self).__init__(state=state, county=county, tract=tract)


class Blockgroup(GVid):

    state = None
    county = None
    tract = None
    blockgroup = None

    def __init__(self, state, county, tract, blockgroup):
        super(Blockgroup,self).__init__(state=state, county=county, tract=tract, blockgroup=blockgroup)

class Block(GVid):

    state = None
    county = None
    tract = None
    blockgroup = None

    def __init__(self, state, county, tract, blockgroup, block):
        super(Block,self).__init__(state=state, county=county, tract=tract, blockgroup=blockgroup, block=block)


augment(__name__, GVid)

