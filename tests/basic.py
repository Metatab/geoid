__author__ = 'eric'

import unittest


class BasicTests(unittest.TestCase):

    def test_basic(self):
        from geoid import civick

        region = civick.Region(1)

        print region

        tract = civick.Tract(6,72,34)

        print tract


        print civick.GVid.parse(str(tract))

    def test_tiger(self):
        from geoid import tiger

        self.assertEqual('067200034', str(tiger.Tract(6, 72, 34)))
        self.assertEqual('067200034', str(tiger.Tract.parse('067200034')))

        self.assertEqual('022900003001', str(tiger.Block.parse('022900003001')))
        self.assertEqual('999999999999', str(tiger.Block.parse('999999999999')))

if __name__ == '__main__':
    unittest.main()
