"""Utilities"""

def simplify(geoids):
    """
    Given a list of geoids, reduce it to a simpler set. If there are five or more geoids at one summary level
    convert them to a single geoid at the higher level.

    :param geoids:
    :return:
    """

    from collections import defaultdict

    aggregated = defaultdict(set)

    d = {}

    for g in geoids:

        if not bool(g):
            continue

        av = g.allval()

        d[av] = None

        aggregated[av].add(g)

    compiled = set()

    for k, v in aggregated.items():
        if len(v) >= 5:
            compiled.add(k)
            compiled.add(k.promote())
        else:
            compiled |= v

    return compiled

def isimplify(geoids):
    """Iteratively simplify until the set stops getting smaller. """

    s0 = list(geoids)

    for i in range(10):
        s1 = simplify(s0)

        if len(s1) == len(s0):
            return s1

        s0 = s1

def iallval(t):
    """Recursively promote and compute allvals """

    if t:
        return [t.allval()] + iallval(t.promote())
    else:
        return []