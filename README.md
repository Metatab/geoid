geoid
=====

Classes for working with census geoids

This module provides dynamically generated classes for parsing and creating each of the approximately 85 Census 
summary levels. It can parse the forms of genoides that appear in the Decenial Census, the ACS, and Tiger files. 
Additionally, it can read and write a more compact format, civick,  that use base62 representation for the numbers. 

Use
---

The geoid module in file geoid/__init__.py,  has a list of the geoid classes that you can instantiate. Or, to print
the list:

    $ python -c 'import geoid; print geoid.names'

The first dozen are the ones you'll use most frequently: 

```bash
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
'zcta': 860
```

The classes are all dynamically generated, so you won't be able to find a class file. 

```python
from geoid import acs
g = acs.Blockgroup(53, 33, 1800, 3)
print g.state, g.county.g.tract.g.blockgroup

gs = str(g)
g = acs.AcsGeoid.parse(gs)
```

Creating
--------

TBD

Parsing
-------
TBD

Parse Generally, or parse to a specific class. 

Access Members
--------------


Promotion, Conversion, Summarization, AllVals
---------------------------------------------

Promote: create a higher level geoid from a lower level one
Convert: Change the type, for instance from a Census geoid to an ACS geoid
Summarize: Create a value to represent a summary level
AllVal: Create a value to represent coverage of an entire region

Caveats
-------

The geoids don't preserve the component, so, for instance,  '03001US1' will get changed to '03000US1'


### Running tests
```bash
git clone git@github.com:CivicKnowledge/geoid.git
cd geoid
python setup.py test
```


