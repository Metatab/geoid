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
    grains = set()

    d = {}

    for g in geoids:

        if not bool(g):
            continue

        av = g.allval()

        d[av] = None

        aggregated[av].add(g)

        grains.add(g.summarize())

    compiled = set()

    for k, v in aggregated.items():
        if len(v) >= 5:
            compiled.add(k)
            compiled.add(k.promote())
        else:

            compiled |= v

    return compiled, grains
