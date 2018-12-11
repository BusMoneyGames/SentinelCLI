from unittest import TestCase
from SentinelUE4.LogParser import BuildLog
import os


class TestBuildLogParser(TestCase):

    def setUp(self):
        self.test_file = os.path.join(os.path.dirname(__file__), 'testdata', "TestLog_CookLog.txt")
        self.build_obj = BuildLog.BuildLogParser(self.test_file)

    def test_extract_errors(self):
        errors = self.build_obj.extract_errors()

        for e in errors:
            print(e)

