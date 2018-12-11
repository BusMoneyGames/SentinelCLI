import SentinelReport.sentinel_generate_reports
from Utilities import BaseSentinelTest


class TestGenerate_reports(BaseSentinelTest.SentinelBaseTest):

    def test_generate_reports(self):
        SentinelReport.sentinel_generate_reports.generate_reports(self.sentinel_report_project_paths)

    def test_generate_client_reports(self):
        SentinelReport.sentinel_generate_reports.generate_client_run_reports(self.sentinel_report_project_paths)