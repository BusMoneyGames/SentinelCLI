from Utilities import BaseSentinelTest
from SentinelReport.Reports import ReportsWriter


class TestReportsWriter(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()

        self.reports_writer = ReportsWriter.ReportsManager(self.sentinel_report_project_paths)

    def test_get_reports(self):
        self.reports_writer.write_all_reports()

    def test_add_report(self):
        data = {}

        self.reports_writer.add_report("Datatable", "unittest_data_table", data)
        self.reports_writer.write_all_reports()
