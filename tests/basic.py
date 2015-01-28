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


if __name__ == '__main__':
    unittest.main()
