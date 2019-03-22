import unittest
import argparse

from SentinelTests.SentinelConfig._tests import test_confighelper
from SentinelTests.SentinelUE4Component._tests import test_buildbinaries


def get_editor_tests():

    test_suit = unittest.TestSuite()
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_default'))
    test_suit.addTest(test_confighelper.TestSentinelConfig('test_generate_overwrite'))

    test_suit.addTest(test_buildbinaries.TestSentinelUE4ComponentBuild('test_detailed_help'))
    test_suit.addTest(test_buildbinaries.TestSentinelUE4ComponentBuild('test_build_default'))

    return test_suit


def main(raw_args=None):
    parser = argparse.ArgumentParser(description='Runs sentinel tasks for Unreal Engine.',
                                     add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-editor", action='store_true')


    args = parser.parse_args(raw_args)

    test_suites = []
    runner = unittest.TextTestRunner()

    if args.editor:
        test_suites.append(get_editor_tests())

    if test_suites:
        for each_suit in test_suites:
            runner.run(each_suit)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(get_editor_tests())
