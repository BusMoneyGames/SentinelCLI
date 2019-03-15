import unittest

from SentinelTests.SentinelConfig._tests import test_confighelper
from SentinelTests.SentinelUE4Component._tests import test_buildbinaries


def suite():
    test_suit = unittest.TestSuite()
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_default'))
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_generate_overwrite'))

    test_suit.addTest(test_buildbinaries.TestSentinelUE4ComponentBuild('test_detailed_help'))
    test_suit.addTest(test_buildbinaries.TestSentinelUE4ComponentBuild('test_build_default'))

    return test_suit


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
