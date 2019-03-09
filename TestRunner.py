import unittest

from SentinelTests.SentinelConfig._tests import test_confighelper


def suite():
    test_suit = unittest.TestSuite()
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_default'))
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_generate_overwrite'))

    return test_suit


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
