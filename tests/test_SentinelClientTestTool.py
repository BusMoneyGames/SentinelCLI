from Utilities import BaseSentinelTest

import SentinelClientTestTool


class TestRun_startup_tests(BaseSentinelTest.SentinelBaseTest):
    def test_run_startup_tests(self):
        SentinelClientTestTool.run_startup_tests(self.sentinel_report_project_paths)
