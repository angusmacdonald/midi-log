import unittest

import tree

class TestTree(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_depth(self):
        testTree = tree.PackageTree()

        self.assertEquals(testTree.getLargestDepth(), 0)

        testTree.add('com.package')

        self.assertEquals(testTree.getLargestDepth(), 2)

        testTree.add('com.package.util.security')

        self.assertEquals(testTree.getLargestDepth(), 4)

    def test_get_instrument(self):
        testTree = tree.PackageTree()

        testTree.add('com.package')
        testTree.add('com.package.util.security')
        testTree.add('com.package.core.func')

        num = testTree.getInstrumentAtDepth('com.package.core.security', 3)

        self.assertTrue(num > 0)


if __name__ == '__main__':
    unittest.main()