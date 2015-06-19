__author__ = 'eric'

import unittest


class BasicTests(unittest.TestCase):

    def test_civick(self):
        from geoid import civick

        region = civick.Region(1)

        self.assertEqual('0k1', str(region))

        tract = civick.Tract(6,72,34)

        self.assertEqual('2g061a0000y', str(tract))

        self.assertEqual('2g061a0000y', str(civick.GVid.parse(str(tract))))

        self.assertEqual('0a', str(civick.GVid.parse(str(civick.Us()))))



    def test_tiger(self):
        from geoid import tiger

        self.assertEqual('06072000034', str(tiger.Tract(6, 72, 34)))
        self.assertEqual('06072000034', str(tiger.Tract.parse('06072000034')))

        self.assertEqual('440030209032037', str(tiger.Block.parse('440030209032037')))
        self.assertEqual('999999999999999', str(tiger.Block.parse('999999999999999')))

    def test_acs(self):
        from geoid import acs

        self.assertEqual(str(acs.State(53)), str(acs.AcsGeoid.parse('04000US53')))
        self.assertEqual(str(acs.County(53,9)), str(acs.AcsGeoid.parse('05000US53009')))
        self.assertEqual(str(acs.Blockgroup(53, 33,1800,3)), str(acs.AcsGeoid.parse('15000US530330018003')))

    def test_parse(self):
        from geoid import tiger
        from geoid import acs
        from geoid import civick

        self.assertEqual(tiger.County, tiger.TigerGeoid.get_class('county'))
        self.assertEqual (tiger.County, tiger.TigerGeoid.get_class(50))

        self.assertEqual('440030209032037',
                         str(tiger.Block.parse('440030209032037').convert(civick.GVid).convert(tiger.TigerGeoid)))

        self.assertEqual('2g061a0000y',
                         str(civick.GVid.parse('2g061a0000y').convert(tiger.TigerGeoid).convert(civick.GVid)))

    def test_convert(self):
        from geoid import tiger
        from geoid import acs
        from geoid import civick

        g = acs.Blockgroup(53, 33,1800,3)



        print str(g)
        cg = g.convert(civick)

        print str(g)
        cg = g.convert(civick.Blockgroup)

        print str(cg)

        cg = g.convert(civick.County)

        print str(cg)


    def test_promote(self):
        from geoid import tiger
        from geoid import acs
        from geoid import civick
        from geoid.util import iallval

        g = acs.Blockgroup(53, 33, 1800, 3)

        self.assertEquals(acs.Tract, type(g.promote()))
        self.assertEquals(acs.County, type(g.promote().promote()))
        self.assertEquals(acs.State, type(g.promote().promote().promote()))
        self.assertEquals(acs.Us, type(g.promote().promote().promote().promote()))

        self.assertEquals(acs.State, type(g.promote('state')))
        self.assertEquals('04000US53', str(g.promote('state')))

        # The Summary value, with all 0 except for the summary level, represents the summary level
        self.assertEquals('15000US999999999999', str(g.summarize()))
        self.assertEquals('14000US99999999999', str(g.promote().summarize()))
        self.assertEquals('05000US99999', str(g.promote().promote().summarize()))

        # The all value represents all of the lower summary level values at the higher summary level.
        self.assertEquals('15000US530330018000',  str(g.allval()))
        self.assertEquals('14000US53033000000', str(g.promote().allval()))
        self.assertEquals('05000US53000', str(g.promote().promote().allval()))

        self.assertEquals(g.summarize().county, 999)
        self.assertEquals(g.allval().county, 33)
        self.assertEquals(g.allval().blockgroup, 0)

        self.assertTrue(g.summarize().is_summary)
        self.assertFalse(g.allval().is_summary)

        self.assertTrue(g.allval().is_allval)
        self.assertFalse(g.summarize().is_allval)

        # Check that summarized gvids don't look lika allvals for state level
        g = civick.GVid.parse('0E06')
        self.assertEqual('0E06',str(g))
        self.assertEqual('0EZZ', str(g.summarize()))
        self.assertEqual('0E00', str(g.allval()))

        g = civick.County(6,72)
        self.assertEqual('0O061a', str(g))
        self.assertEqual('0OZZZZ', str(g.summarize()))
        self.assertEqual('0O0600', str(g.allval()))

        g = civick.GVid.parse('0E06')
        self.assertEqual('0a', str(g.promote()))

        self.assertEqual(None,  civick.Us().promote())
        self.assertEqual('0a', str(civick.Us().summarize()))
        self.assertEqual('0a', str(civick.Us().allval()))



        print [ str(x) for x in  iallval(civick.Blockgroup(53, 33, 1800, 3))]


    def test_simplify(self):

        from geoid import acs
        from geoid.util import simplify, isimplify


        geoids = []

        for state in [10,11,12]:
            geoids.append(acs.State(state))

        for state in [1,2]:
            for county in range(1,6):
                geoids.append(acs.County(state, county))

        for state in [3,4]:
            for county in range(1,4):
                geoids.append(acs.County(state, county))

        compiled = simplify(geoids)
        print [ str(x) for x in  compiled]

        print '---'

        geoids = []

        for state in  range(0,6):
            for county in range(6,12):
                for tract in range(12,20):
                    geoids.append(acs.Tract(state, county, tract))

        print len(geoids)

        s0 = isimplify(geoids)

        for g in sorted( str(x) for x in s0):
            print g

        print '---'

        for g in simplify(simplify(geoids)):
            if g.is_allval:
                print str(g)


    def xtest_dump(self):
        from geoid import summary_levels
        from geoid import civick

        for k,v in summary_levels.items():
            print "<option value={}>{}</option>".format(str(civick.GVid.get_class(k)().summarize() ), k.capitalize())

if __name__ == '__main__':
    unittest.main()
