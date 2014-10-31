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

        print acs.State(53)
        print acs.County(6,73)


if __name__ == '__main__':
    unittest.main()
