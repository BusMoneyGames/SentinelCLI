from Utilities import BaseSentinelTest
import pathlib
from SentinelUE4.Game.ClientOutput import ClientLogParser


class TestLogSegmentParser(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        # Not overwriting since this test does not to know about the environment

        # Test file
        test_log = (pathlib.PurePath(__file__)).parent.joinpath("testdata", "client_run_data_log.txt")

        f = open(test_log, "r")
        test_lines = f.readlines()
        f.close()

        self.log_segment_parser = ClientLogParser.ClientTestEntryParser("Unittest_Name", test_lines)

    def test_get_test_name(self):
        test_name = self.log_segment_parser._get_test_name()

    def test_get_gpu_data(self):
        gpu_data = self.log_segment_parser._get_gpu_data()


    def test_get_texture_data(self):
        texture_data = self.log_segment_parser.get_texture_data()


    def test_get_test_screenshot_path(self):
        screenshot_paths = self.log_segment_parser.get_test_screenshot_path()

