""" CLasses for working with census Geoids

"""

__version__ = '0.0.1'
__author__ = "eric@civicknowledge.com"

summary_levels = { # (summary level value, base 10 chars,  Base 62 chars, prefix fields)
    'region' : (20,1,1,[]),
    'division' : (30,1,1,['region']),
    'state' : (40,2,2,[]),
    'county' : (50,3,2,['state']),
    'cosub' : (60,5,3,['state','county']),
    'place' : (160,5,4,['state']),
    'urbanarea': (999,5, 4, []),
    'tract' : (140,6,5,['state','county']),
    'blockgroup' : (150,1,1,['state','county','tract']), # Appears to always be the 1000's digit of block.
    'block' : (101,4,2,['state','county','tract']),
}




def base62_encode(num):
    """Encode a number in Base X. WIth the built-in alphabet, its base 62

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    Stolen from: http://stackoverflow.com/a/1119769/1144479
    """
    
    alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
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
    
    alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return int(num)

import inspect,sys

def augment(module_name, base_class):
    """Call the augment() method for all of the derived classes in the module """

    for name, cls in inspect.getmembers(sys.modules[module_name],
                                        lambda x : inspect.isclass(x) and  issubclass(x, base_class) ):
        if cls == base_class:
            continue

        cls.augment()

def make_classes(base_class, module):
    """Create derived classes and put them into the same module as the base class"""

    for k, v in summary_levels.items():

        cls = base_class.class_factory(k.capitalize())

        cls.augment()

        setattr(module, k.capitalize(), cls)



class Geoid(object):

    # sl_format = '{sl:0>2s}'
    # elem_format = '{{{}:0>{}s}}'
    # sl_regex = '(?P<sl>.{2})'
    # elem_regex = '(?P<{}>.{{{}}})'

    @classmethod
    def resolve_summary_level(cls, sl):
        return cls.sl_map[cls.encode.__func__(sl)][0]

    @classmethod
    def make_format_string(cls, level):
        sl_entry = summary_levels[level]

        segs = sl_entry[3] + [level]

        formats = [cls.sl_format] + [cls.elem_format.format(seg, summary_levels[seg][cls.width_pos]) for seg in segs]

        return ''.join(formats)

    @classmethod
    def make_regex(cls, level):


        sl_entry = summary_levels[level]

        segs = sl_entry[3] + [level]

        regexes = [cls.sl_regex] + [cls.elem_regex.format(seg, summary_levels[seg][cls.width_pos]) for seg in segs]

        re_str = '^' + ''.join(regexes) + "$"

        return re_str

    @classmethod
    def augment(cls):
        """Augment the class with computed formats, regexes, and other things. This caches these values so
        they don't have to be created for every instance. """

        import re

        level_name = cls.__name__.lower()

        sl_entry = summary_levels[level_name]

        cls.sl = cls.encode.__func__(sl_entry[0])

        cls.class_map[cls.__name__.lower()] = cls

        cls.sl_map[cls.sl] = (cls, sl_entry)

        cls.fmt = cls.make_format_string(cls.__name__.lower())

        cls.regex_str = cls.make_regex(cls.__name__.lower())
        cls.regex = re.compile(cls.regex_str)

        # List of field names
        cls.fields = sl_entry[3] + [level_name]

    def __init__(self, *args, **kwargs):

        # This is a bit unusual, because it means, that , unlike nornal
        # python args, a kwarg can overwrite a position arg.

        d = dict(zip(self.fields, args))

        d.update(kwargs)

        for k, v in d.items():
            if k in self.fields:
                setattr(self, k, self.encode.__func__(v))

    def __str__(self):

        d = self.__dict__
        d['sl'] = self.sl

        return self.fmt.format(**self.__dict__)

    @classmethod
    def parse(cls, gvid):

        if not cls.sl:
            sl = gvid[0:cls.sl_width]  # Civick and ACS include the SL, so can call from base type.

        else:
            sl = cls.sl # Otherwise must use derived class.

        cls, sl_entry = cls.sl_map[sl]

        m = cls.regex.match(gvid)

        if not m:
            raise Exception("Failed to match '{}' to '{}' ".format(gvid,cls.regex_str))

        d = m.groupdict()

        if not d:
            return None

        d = {k: cls.decode.__func__(v) for k, v in d.items()}

        try:
            del d['sl']
        except KeyError:
            pass

        return cls(**d)

