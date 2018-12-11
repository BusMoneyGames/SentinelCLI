from Utilities import BaseSentinelTest
import SentinelDataParser.build_log_parser as build_log_parser

class TestCookLogParser(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        self.build_log_parser = build_log_parser.CookLogParser(self.sentinel_report_project_paths)

    def test_get_log_lines(self):
        self.build_log_parser.get_log_lines()
