

""" CLasses for working with census Geoids

"""


import inspect
import re
import sys
import six

names = {  # (summary level value, base 10 chars,  Base 62 chars, prefix fields)
    'null': 1,
    'us': 10,
    'region': 20,
    'division': 30,
    'state': 40,
    'county': 50,
    'cosub': 60,
    'place': 160,
    'ua': 400,
    'tract': 140,
    'blockgroup': 150,
    'block': 101,
    'sdelm': 950,
    'sdsec': 960,
    'sduni': 970,
    'zcta': 860,
    'zip': 1200,
    'sldl': 620,
    'sldu': 610,
    'cdcurr': 500,

    # Other Levels that don't have proper names yet. For these .allval() and
    # simplify() don't work properly.
    'state_aianhh': 260,
    'necta_nectadiv_state_county_cousub': 358,
    'state_aianhh_place': 269,
    'aianhh_state_county': 270,
    'state_cbsa_metdiv': 323,
    'state_aianhh280': 280,
    'state_place_county': 155,
    'aianhh_aitsce_state': 290,
    'state_aianhh_aihhtli': 283,
    'state_cdcurr_aianhh': 550,
    'state_concit': 170,
    'state_concit_place': 172,
    'state_aianhh_aihhtli286': 286,
    'cbsa': 310,
    'cbsa_state': 311,
    'cbsa_state_place': 312,
    'cbsa_state_county': 313,
    'cbsa_metdiv': 314,
    'cbsa_metdiv_state': 315,
    'state_cbsa': 320,
    'state_cbsa_place': 321,
    'state_cbsa_county': 322,
    'state_county_cousub_submcd': 67,
    'state_cbsa_metdiv_county': 324,
    'state_county_cousub_place': 70,
    'necta_state_county': 353,
    'state_puma5': 795,
    'csa': 330,
    'csa_state': 331,
    'csa_cbsa': 332,
    'csa_cbsa_state': 333,
    'cnecta': 335,
    'state_county_cousub_place_tract': 80,
    'cnecta_necta': 337,
    'cnecta_necta_state': 338,
    'state_csa': 340,
    'state_csa_cbsa': 341,
    'state_cnecta': 345,
    'state_cnecta_necta': 346,
    'necta': 350,
    'necta_state': 351,
    'necta_state_place': 352,
    'cnecta_state': 336,
    'necta_state_county_cousub': 354,
    'necta_nectadiv': 355,
    'necta_nectadiv_state': 356,
    'state_anrc': 230,
    'necta_nectadiv_state_county': 357,
    'state_necta': 360,
    'cbsa_metdiv_state_county': 316,
    'state_necta_county': 362,
    'state_necta_county_cousub': 363,
    'state_necta_nectadiv': 364,
    'state_necta_nectadiv_county': 365,
    'state_necta_nectadiv_county_cousub': 366,
    'ua_state': 410,
    'ua_state_county': 430,
    'state_sldu_county': 612,
    'state_sldu': 610,
    'state_sldl_county': 622,
    'state_sldl': 620,
    'state_cdcurr_county': 510,
    'state_necta_place': 361,
    'aianhh': 250,
    'aianhh_aitsce': 251,
    'aianhh_aihhtli': 252,
    'state_sldl_county': 622,
    'aianhh_aihhtli254': 254

}
lengths = {
    'null': 1,
    'aianhh': 4,  # American Indian Area/Alaska Native Area/ Hawaiian Home Land (Census)
    'aihhtli': '1',  # American Indian Trust Land/ Hawaiian Home Land Indicator. A str b/c Census val is a str
    'aitsce': 3,  # American Indian Tribal Subdivision (Census)
    'anrc': 5,  # Alaska Native Regional Corporation (FIPS)
    'blkgrp': 1,  # Block Group
    'blockgroup': 1,  # Block Group
    'block': 4,  # Block
    'cbsa': 5,  # Metropolitan and Micropolitan Statistical Area
    'cdcurr': 2,  # Current Congressional District ***
    'cnecta': 3,  # New England City and Town Combined Statistical Area
    'concit': 5,  # Consolidated City
    'county': 3,  # County of current residence
    'cousub': 5,  # County Subdivision (FIPS)
    'cosub': 5,  # County Subdivision (FIPS)
    'csa': 3,  # Combined Statistical Area
    'division': 1,  # Census Division
    'metdiv': 5,  # Metropolitan Statistical Area- Metropolitan Division
    'necta': 5,  # New England City and Town Area
    'nectadiv': 5,  # New England City and Town Area Division
    'place': 5,  # Place (FIPS Code)
    'puma5': 5,  # Public Use Microdata Area 5% File
    'region': 1,  # Census Region
    'sdelm': 5,  # State-School District (Elementary)
    'sdsec': 5,  # State-School District (Secondary)
    'sduni': 5,  # State-School District (Unified)
    'sldl': '3',  # State Legislative District Lower. A String to signal that the census value is a string
    'sldu': '3',  # State Legislative District Upper.  A String to signal that the census value is a string
    'state': 2,  # State (FIPS Code)
    'submcd': 5,  # Subminor Civil Division (FIPS)
    'tract': 6,  # Census Tract
    'ua': 5,  # Urban Area
    'ur': 1,  # Urban/Rural
    'us': 0,
    'zcta': 5,
    # Nonstandard
    'zip': 5,
}
segments = {
    1: ['null'],  # United States
    10: ['us'],  # United States
    20: ['region'],  # Region
    30: ['division'],  # Division
    40: ['state'],  # State
    50: ['state', 'county'],  # County
    60: ['state', 'county', 'cousub'],  # County Subdivision
    67: ['state', 'county', 'cousub', 'submcd'],  # State (Puerto Rico Only)-County-County Subdivision-Subbarrio
    70: ['state', 'county', 'cousub', 'place'],  # County Subdivision-Place/Remainder
    80: ['state', 'county', 'cousub', 'place', 'tract'],  # County Subdivision-Place/Remainder-Census Tract
    101: ['state', 'county', 'tract', 'block'],
    140: ['state', 'county', 'tract'],  # Census Tract
    150: ['state', 'county', 'tract', 'blockgroup'],  # Census Tract-Block Group
    155: ['state', 'place', 'county'],  # Place-County
    160: ['state', 'place'],  # Place
    170: ['state', 'concit'],  # Consolidated City
    172: ['state', 'concit', 'place'],  # Consolidated City-Place Within Consolidated City
    230: ['state', 'anrc'],  # State-Alaska Native Regional Corporation
    250: ['aianhh'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land
    251: ['aianhh', 'aitsce'],  # American Indian Area/Alaska NativeArea/HawaiianHomeLand-Tribal Subdivision/Remainder
    252: ['aianhh', 'aihhtli'],  # American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)4
    254: ['aianhh', 'aihhtli'],  # American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land
    260: ['state', 'aianhh'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-State
    269: ['state', 'aianhh', 'place'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-Place-Remainder
    270: ['aianhh', 'state', 'county'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-State-County
    280: ['state', 'aianhh'],  # State-American Indian Area/Alaska Native Area/Hawaiian Home Land
    283: ['state', 'aianhh', 'aihhtli'],
    # State-American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)
    286: ['state', 'aianhh', 'aihhtli'],
    # State-American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land
    290: ['aianhh', 'aitsce', 'state'],
    # American Indian Area/Alaska Native Area/Hawaiian Home Land-Tribal Subdivision/Remainder-State
    310: ['cbsa'],  # CBSA
    311: ['cbsa', 'state'],  # CBSA-State-County
    312: ['cbsa', 'state', 'place'],  # CBSA-State-Principal City
    313: ['cbsa', 'state', 'county'],  # CBSA-State-County
    314: ['cbsa', 'metdiv'],  # Metropolitan Statistical Area/Metropolitan Division
    315: ['cbsa', 'metdiv', 'state'],  # Metropolitan Statistical Area/Metropolitan Division-State
    316: ['cbsa', 'metdiv', 'state', 'county'],  # Metropolitan Statistical Area/Metropolitan Division-State-County
    320: ['state', 'cbsa'],  # State- CBSA
    321: ['state', 'cbsa', 'place'],  # State- CBSA -Principal City
    322: ['state', 'cbsa', 'county'],  # State- CBSA -County
    323: ['state', 'cbsa', 'metdiv'],  # State- Metropolitan Statistical Area/Metropolitan Division
    324: ['state', 'cbsa', 'metdiv', 'county'],  # State- Metropolitan Statistical Area/Metropolitan Division-County
    330: ['csa'],  # Combined Statistical Area
    331: ['csa', 'state'],  # Combined Statistical Area-State
    332: ['csa', 'cbsa'],  # Combined Statistical Area-CBSA
    333: ['csa', 'cbsa', 'state'],  # Combined Statistical Area-CBSA-State
    335: ['cnecta'],  # Combined New England City and Town Area
    336: ['cnecta', 'state'],  # Combined New England City and Town Area -State
    337: ['cnecta', 'necta'],  # Combined New England City and Town Area -New England City and Town Area
    338: ['cnecta', 'necta', 'state'],  # Combined New England City and Town Area -New England City and Town Area-State
    340: ['state', 'csa'],  # State-Combined Statistical Area
    341: ['state', 'csa', 'cbsa'],  # State-Combined Statistical Area-CBSA
    345: ['state', 'cnecta'],  # State-Combined New England City and Town Area

    346: ['state', 'cnecta', 'necta'],  # State-Combined New England City and Town Area-New England City and Town Area
    350: ['necta'],  # New England City and Town Area
    351: ['necta', 'state'],  # New England City and Town Area-State
    352: ['necta', 'state', 'place'],  # New England City and Town Area-State-Principal City
    353: ['necta', 'state', 'county'],  # New England City and Town Area-State-County
    354: ['necta', 'state', 'county', 'cousub'],  # New England City and Town Area-State-County-County Subdivision
    355: ['necta', 'nectadiv'],  # New England City and Town Area (NECTA)-NECTA Division
    356: ['necta', 'nectadiv', 'state'],  # New England City and Town Area (NECTA)-NECTA Division-State
    357: ['necta', 'nectadiv', 'state', 'county'],  # New England City and Town Area (NECTA)-NECTA Division-State-County
    358: ['necta', 'nectadiv', 'state', 'county', 'cousub'],
    # New England City and Town Area (NECTA)-NECTA Division-State-County-County Subdivision
    360: ['state', 'necta'],  # State-New England City and Town Area
    361: ['state', 'necta', 'place'],  # State-New England City and Town Area-Principal City
    362: ['state', 'necta', 'county'],  # State-New England City and Town Area-County
    363: ['state', 'necta', 'county', 'cousub'],  # State-New England City and Town Area-County-County Subdivision
    364: ['state', 'necta', 'nectadiv'],  # State-New England City and Town Area (NECTA)-NECTA Division
    365: ['state', 'necta', 'nectadiv', 'county'],  # State-New England City and Town Area (NECTA)-NECTA Division-County
    366: ['state', 'necta', 'nectadiv', 'county', 'cousub'],
    # State-New England City and Town Area (NECTA)-NECTA Division-County-County Subdivision
    400: ['ua'],  # Urban Area,
    410: ['ua', 'state'],  # Urban Area, State,
    430: ['ua','state','county'],  # Urban Area, State, County,

    500: ['state', 'cdcurr'],  # Congressional District
    510: ['state', 'cdcurr', 'county'],  #
    550: ['state', 'cdcurr', 'aianhh'],
    # Congressional District-American IndianArea/Alaska NativeArea/Hawaiian Home Land
    610: ['state', 'sldu'],  # State Senate District
    612: ['state', 'sldu', 'county'],  # State Senate District-County
    620: ['state', 'sldl'],  # State House District
    622: ['state', 'sldl', 'county'],  # State House District-County
    795: ['state', 'puma5'],  # State-Public Use MicroSample Area 5%
    860: ['zcta'],
    950: ['state', 'sdelm'],  # State-Elementary School District
    960: ['state', 'sdsec'],  # State-High School District
    970: ['state', 'sduni'],  # State-Unified School District
    # Nonstandard
    1200: ['zip']
}
descriptions = {
    1: 'United States',
    10: 'United States',
    20: 'Region',
    30: 'Division',
    40: 'State',
    50: 'County',
    60: 'County Subdivision',
    67: 'State (Puerto Rico Only)-County-County Subdivision-Subbarrio',
    70: 'County Subdivision-Place/Remainder',
    80: 'County Subdivision-Place/Remainder-Census Tract',
    101: 'block',
    140: 'Census Tract',
    150: 'Census Tract-Block Group',
    155: 'Place-County',
    160: 'Place',
    170: 'Consolidated City',
    172: 'Consolidated City-Place Within Consolidated City',
    230: 'State-Alaska Native Regional Corporation',
    250: 'American Indian Area/Alaska Native Area/Hawaiian Home Land',
    251: 'American Indian Area/Alaska NativeArea/HawaiianHomeLand-Tribal Subdivision/Remainder',
    252: 'American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)',
    254: 'American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land',
    260: 'American Indian Area/Alaska Native Area/Hawaiian Home Land-State',
    269: 'American Indian Area/Alaska Native Area/Hawaiian Home Land-Place-Remainder',
    270: 'American Indian Area/Alaska Native Area/Hawaiian Home Land-State-County',
    280: 'State-American Indian Area/Alaska Native Area/Hawaiian Home Land',
    283: 'aihhtli',
    286: 'aihhtli',
    290: 'state',
    310: 'CBSA',
    311: 'CBSA-State-County',
    312: 'CBSA-State-Principal City',
    313: 'CBSA-State-County',
    314: 'Metropolitan Statistical Area/Metropolitan Division',
    315: 'Metropolitan Statistical Area/Metropolitan Division-State',
    316: 'Metropolitan Statistical Area/Metropolitan Division-State-County',
    320: 'State- CBSA',
    321: 'State- CBSA -Principal City',
    322: 'State- CBSA -County',
    323: 'State- Metropolitan Statistical Area/Metropolitan Division',
    324: 'State- Metropolitan Statistical Area/Metropolitan Division-County',
    330: 'Combined Statistical Area',
    331: 'Combined Statistical Area-State',
    332: 'Combined Statistical Area-CBSA',
    333: 'Combined Statistical Area-CBSA-State',
    335: 'Combined New England City and Town Area',
    336: 'Combined New England City and Town Area -State',
    337: 'Combined New England City and Town Area -New England City and Town Area',
    338: 'Combined New England City and Town Area -New England City and Town Area-State',
    340: 'State-Combined Statistical Area',
    341: 'State-Combined Statistical Area-CBSA',
    345: 'State-Combined New England City and Town Area',
    346: 'State-Combined New England City and Town Area-New England City and Town Area',
    350: 'New England City and Town Area',
    351: 'New England City and Town Area-State',
    352: 'New England City and Town Area-State-Principal City',
    353: 'New England City and Town Area-State-County',
    354: 'New England City and Town Area-State-County-County Subdivision',
    355: 'New England City and Town Area (NECTA)-NECTA Division',
    356: 'New England City and Town Area (NECTA)-NECTA Division-State',
    357: 'New England City and Town Area (NECTA)-NECTA Division-State-County',
    358: 'New England City and Town Area (NECTA)-NECTA Division-State-County-County Subdivision',
    360: 'State-New England City and Town Area',
    361: 'State-New England City and Town Area-Principal City',
    362: 'State-New England City and Town Area-County',
    363: 'State-New England City and Town Area-County-County Subdivision',
    364: 'State-New England City and Town Area (NECTA)-NECTA Division',
    365: 'State-New England City and Town Area (NECTA)-NECTA Division-County-County Subdivision',
    400: 'Urban Area,',
    410: 'Urban Area, State,',
    430: 'Urban Area, State, County,',
    500: 'Congressional District',
    510: 'Congressional District, County',
    550: 'Congressional District-American IndianArea/Alaska NativeArea/Hawaiian Home Land',
    610: 'State Senate District',
    612: 'State Senate District-County',
    620: 'State House District',
    622: 'State House District-County',
    795: 'State-Public Use MicroSample Area 5%',
    860: 'ZIP Code Tabulation Area',
    950: 'State-Elementary School District',
    960: 'State-High School District',
    970: 'State-Unified School District',
}
plurals = {
    'county': 'counties',
    'place': 'places',
    'Sdlu': 'State '
}


class NotASummaryName(Exception):
    """An argument was not one of the valid summary names"""


class ParseError(Exception):
    """Error parsing a geoid"""


def parse_to_gvid(v):
    """Parse an ACS Geoid or a GVID to a GVID"""
    from geoid.civick import GVid
    from geoid.acs import AcsGeoid

    m1 = ''

    try:
        return GVid.parse(v)
    except ValueError as e:
        m1 = str(e)

    try:
        return AcsGeoid.parse(v).convert(GVid)
    except ValueError as e:
        raise ValueError("Failed to parse to either ACS or GVid: {}; {}".format(m1, str(e)))


def base62_encode(num):
    """Encode a number in Base X. WIth the built-in alphabet, its base 62

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    Stolen from: http://stackoverflow.com/a/1119769/1144479
    """

    num = int(num)

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    Stolen from: http://stackoverflow.com/a/1119769/1144479
    """

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return int(num)


def augment(module_name, base_class):
    """Call the augment() method for all of the derived classes in the module """

    for name, cls in inspect.getmembers(sys.modules[module_name],
                                        lambda x : inspect.isclass(x) and  issubclass(x, base_class) ):
        if cls == base_class:
            continue

        cls.augment()


def get_class(module, sl):

    for name, named_sl in names.items():
        if named_sl == sl or sl == name:
            return getattr(module, name.capitalize())

    raise NotASummaryName("No class for summary_level {}".format(sl))


def make_classes(base_class, module):
    """Create derived classes and put them into the same module as the base class.

    This function is called at the end of each of the derived class modules, acs, census, civik and tiger.
    It will create a set of new derived class in the module, one for  each of the enries in the `summary_levels`
    dict.

    """
    from functools import partial

    for k in names:

        cls = base_class.class_factory(k.capitalize())

        cls.augment()

        setattr(module, k.capitalize(), cls)

    setattr(module, 'get_class', partial(get_class, module))


class CountyName(object):
    """A Census county name, with methods to create shorter versions and return the types of division,
    which may be county, parish, borough, etc. """

    # Strip the county and state name. THis doesn't work for some locations
    # where the county is actually called a parish or a bario.

    state_name_pattern = r', (.*)$'
    state_name_re = re.compile(state_name_pattern)

    def __init__(self, name):
        self.name = name

    def intuit_name(self, name):
        """Return a numeric value in the range [-1,1), indicating the likelyhood that the name is for a valuable of
        of this type. -1 indicates a strong non-match, 1 indicates a strong match, and 0 indicates uncertainty. """

        raise NotImplementedError

    @property
    def state(self):
        try:
            county, state = self.name.split(',')
            return state
        except ValueError:
            # The search will fail for 'District of Columbia'
            return ''

    @property
    def medium_name(self):
        """The census name without the state"""
        return self.state_name_re.sub('', self.name)

    type_names = (
        'County', 'Municipio', 'Parish', 'Census Area', 'Borough',
        'Municipality', 'city', 'City and Borough')
    type_name_pattern = '|'.join('({})'.format(e) for e in type_names)
    type_names_re = re.compile(type_name_pattern)

    @property
    def division_name(self):
        """The type designation for the county or county equivalent, such as 'County','Parish' or 'Borough'"""
        try:
            return next(e for e in self.type_names_re.search(self.name).groups() if e is not None)
        except AttributeError:
            # The search will fail for 'District of Columbia'
            return ''

    county_name_pattern = r'(.+) {}, (.+)'.format(type_name_pattern)
    county_name_re = re.compile(county_name_pattern)

    @property
    def short_name(self):
        try:
            county, state = self.name.split(',')
        except ValueError:
            return self.name  # 'District of Colombia'

        return self.type_names_re.sub('', county)

    def __str__(self):
        return self.name

class Geoid(object):

    @classmethod
    def resolve_summary_level(cls, sl):
        try:
            return cls.sl_map[sl]
        except KeyError:
            return None

    @classmethod
    def make_format_string(cls, level):

        sl_num = names[level]

        segs = segments[sl_num]

        formats = []

        formats.append(cls.sl_format)

        for seg in segs:
            # Lengths dict may have strings to indicate string format usage.
            if int(lengths[seg]) <= 0:
                    continue

            if isinstance(lengths[seg], int):
                fmt = cls.elem_format
            else:
                fmt = cls.elem_str_format

            formats.append(fmt.format(seg, cls.part_width(lengths[seg])))

        return ''.join(formats)

    @classmethod
    def make_regex(cls, level):

        sl_num = names[level]

        segs = segments[sl_num]

        # Lengths dict may have strings to indicate string format usage.
        regexes = [cls.sl_regex] + [cls.elem_regex.format(seg, cls.part_width(lengths[seg]))
                                    for seg in segs if int(lengths[seg]) > 0]

        re_str = '^' + ''.join(regexes) + '$'

        return re_str

    @classmethod
    def augment(cls):
        """Augment the class with computed formats, regexes, and other things. This caches these values so
        they don't have to be created for every instance. """

        import re

        level_name = cls.__name__.lower()

        cls.sl = names[level_name]

        cls.class_map[cls.__name__.lower()] = cls

        cls.sl_map[cls.sl] = cls

        cls.fmt = cls.make_format_string(cls.__name__.lower())

        cls.regex_str = cls.make_regex(cls.__name__.lower())
        cls.regex = re.compile(cls.regex_str)

        # List of field names
        cls.level = level_name
        cls.fields = segments[cls.sl]


    @classmethod
    def get_class(cls, name_or_sl):
        """Return a derived class based on the class name or the summary_level"""
        try:
            return cls.sl_map[int(name_or_sl)]

        except TypeError as e:
            raise TypeError("Bad name or sl: {} : {}".format(name_or_sl, e))
        except ValueError:
            try:
                return cls.class_map[name_or_sl.lower()]
            except (KeyError, ValueError):
                raise NotASummaryName("Value '{}' is not a valid summary level".format(name_or_sl))

    def __init__(self, *args, **kwargs):

        # This is a bit unusual, because it means, that , unlike normal
        # python args, a kwarg can overwrite a position arg.

        d = dict(zip(self.fields, args + ((0,) * 10)))  # Add enough zeros to set all fields to zero

        d.update(kwargs)

        for k, v in d.items():
            if k in self.fields:
                try:
                    setattr(self, k, v)
                except TypeError as e:
                    raise TypeError("Failed to convert '{}' ({}) for field '{}' in {}: {}"
                                    .format(v, type(v), k, type(self), e))
                except ValueError as e:
                    raise ValueError("Failed to convert '{}' ({}) for field '{}' in {}: {}"
                                     .format(v, type(v), k, type(self), e))

    def __str__(self):

        d = self.__dict__
        d['sl'] = self.sl

        # Hacks for special string cases
        if 'sldu' in d:
            d['sldu'] = str(d['sldu']).zfill(3)

        if 'sldl' in d:
            d['sldl'] = str(d['sldl']).zfill(3)

        try:
            fn = six.get_method_function(self.encode)
            kwargs = {k: fn(v) for k, v in d.items()}
            return self.fmt.format(**kwargs)
        except (ValueError, KeyError) as e:
            raise ValueError("Bad value in {}, data {} for format {}: {}".format(type(self), d, self.fmt, e))

    @property
    def state_name(self):
        from geoid.censusnames import geo_names
        return geo_names[(self.state, 0)]

    @property
    def stusab(self):
        from geoid.censusnames import stusab
        try:
            return stusab[int(self.state)]
        except (AttributeError, ValueError):
            # Assume this is a Us object, or some other national object
            return 'US'

    @property
    def county_name(self):
        from geoid.censusnames import geo_names
        try:
            try:
                return CountyName(geo_names[(self.state, self.county)])
            except KeyError:
                try:
                    return CountyName("County #{}, {}".format(self.county,geo_names[(self.state, 0)]))
                except KeyError:
                    return CountyName("County #{}, State#{}".format(self.county, self.state))
        except Exception:
            return CountyName('')

    @property
    def geo_name(self):
        """
        Return a name of the state or county, or, for other lowever levels, the
        name of the level type in the county.

        :return:
        """
        if self.level == 'county':
            return str(self.county_name)

        elif self.level == 'state':
            return self.state_name

        else:
            if hasattr(self, 'county'):
                return "{} in {}".format(self.level,str(self.county_name))

            elif hasattr(self, 'state'):
                return "{} in {}".format(self.level, self.state_name)

            else:
                return "a {}".format(self.level)

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

    @classmethod
    def parse(cls, gvid, exception=True):
        """
        Parse a string value into the geoid of this class.

        :param gvid: String value to parse.
        :param exception: If true ( default) raise an eception on parse erorrs. If False, return a
        'null' geoid.
        :return:
        """

        if gvid == 'invalid':
            return cls.get_class('null')(0)

        if not bool(gvid):
            return None

        if not isinstance(gvid, six.string_types):
            raise TypeError("Can't parse; not a string. Got a '{}' ".format(type(gvid)))

        try:
            if not cls.sl:
                # Civick and ACS include the SL, so can call from base type.
                if six.PY3:
                    fn = cls.decode
                else:
                    fn = cls.decode.__func__

                sl = fn(gvid[0:cls.sl_width])
            else:
                sl = cls.sl  # Otherwise must use derived class.

        except ValueError as e:
            if exception:
                raise ValueError("Failed to parse gvid '{}': {}".format(gvid, str(e)))
            else:
                return cls.get_class('null')(0)

        try:
            cls = cls.sl_map[sl]
        except KeyError:
            if exception:
                raise ValueError("Failed to parse gvid '{}': Unknown summary level '{}' ".format(gvid, sl))
            else:
                return cls.get_class('null')(0)

        m = cls.regex.match(gvid)

        if not m:
            raise ValueError("Failed to match '{}' to '{}' ".format(gvid, cls.regex_str))

        d = m.groupdict()

        if not d:
            return None

        if six.PY3:
            fn = cls.decode
        else:
            fn = cls.decode.__func__

        d = {k: fn(v) for k, v in d.items()}

        try:
            del d['sl']
        except KeyError:
            pass

        return cls(**d)

    def convert(self, root_cls):
        """Convert to another derived class. cls is the base class for the derived type,
        ie AcsGeoid, TigerGeoid, etc. """

        d = self.__dict__
        d['sl'] = self.sl

        try:
            cls = root_cls.get_class(root_cls.sl)
        except (AttributeError, TypeError):
            # Hopefully because root_cls is a module
            cls = root_cls.get_class(self.sl)

        return cls(**d)

    def as_census(self):
        from geoid.census import CensusGeoid
        return self.convert(CensusGeoid)

    def as_acs(self):
        from geoid.acs import AcsGeoid
        return self.convert(AcsGeoid)

    def as_tiger(self):
        from geoid.tiger import TigerGeoid
        return self.convert(TigerGeoid)

    def promote(self, level=None):
        """Convert to the next higher level summary level"""

        if level is None:

            if len(self.fields) < 2:
                if self.level in ('region', 'division', 'state', 'ua'):
                    cls = self.get_class('us')
                else:
                    return None
            else:
                cls = self.get_class(self.fields[-2])
        else:
            cls = self.get_class(level)

        d = dict(self.__dict__.items())
        d['sl'] = self.sl

        return cls(**d)

    def summarize(self):
        """Convert all of the values to their max values. This form is used to represent the summary level"""

        raise NotImplementedError

    def allval(self):
        """Convert the last value to zero. This form represents the entire higher summary level at the granularity
        of the lower  summary level. For example, for a county, it means 'All counties in the state' """

        d = dict(self.__dict__.items())
        d['sl'] = self.sl

        d[self.level] = 0

        cls = self.get_class(self.sl)

        return cls(**d)

    @classmethod
    def nullval(cls):
        """Create a new instance where all of the values are 0"""

        d = dict(cls.__dict__.items())

        for k in d:
            d[k] = 0

        d['sl'] = cls.sl
        d[cls.level] = 0

        return cls(**d)

    @property
    def tuples(self):
        """Return tuples of field, value, in the order of the levels as they are defined """
        return [(field, getattr(self, field, None)) for field in self.fields]

    @property
    def is_summary(self):
        """Return True if this geoid is an summary -- all of the fields are 0"""

        return str(self) == str(self.summarize())

    @property
    def is_allval(self):
        """Return True if this geoid is an allval -- the last field is zero, but the first is not"""

        tups = self.tuples

        return tups[-1][1] == 0 and tups[0][1] != 0

    @property
    def level_plural(self):
        """Return the name of the level as a plural"""
        return plurals.get(self.level, self.level + "s")


def generate_all(sumlevel, d):
    """Generate a dict that includes all of the available geoid values, with keys
    for the most common names for those values. """

    from geoid.civick import GVid
    from geoid.tiger import TigerGeoid
    from geoid.acs import AcsGeoid

    sumlevel = int(sumlevel)

    d = dict(d.items())

    # Map common name variants
    if 'cousub' in d:
        d['cosub'] = d['cousub']
        del d['cousub']

    if 'blkgrp' in d:
        d['blockgroup'] = d['blkgrp']
        del d['blkgrp']

    if 'zcta5' in d:
        d['zcta'] = d['zcta5']
        del d['zcta5']

    gvid_class = GVid.resolve_summary_level(sumlevel)

    if not gvid_class:
        return {}

    geoidt_class = TigerGeoid.resolve_summary_level(sumlevel)
    geoid_class = AcsGeoid.resolve_summary_level(sumlevel)

    try:
        return dict(
            gvid=str(gvid_class(**d)),
            geoid=str(geoid_class(**d)),
            geoidt=str(geoidt_class(**d))
        )
    except:
        raise


def _generate_names():
    """ Code to generate the state and county names

    >>> python -c 'import geoid; geoid._generate_names()'

    """

    from ambry import get_library

    l = get_library()

    counties = l.partition('census.gov-acs-geofile-2009-geofile50-20095-50')
    states = l.partition('census.gov-acs-geofile-2009-geofile40-20095-40')

    names = {}
    for row in counties.remote_datafile.reader:
        names[(row.state, row.county)] = row.name

    for row in states.remote_datafile.reader:
        if row.component == '00':
            names[(row.state, 0)] = row.name

    pprint.pprint(names)