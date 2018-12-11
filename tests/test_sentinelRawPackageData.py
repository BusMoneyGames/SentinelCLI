from Utilities import BaseSentinelTest
import BaseProjectPaths


class TestSentinelRawPackageData(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        raw_path = self.sentinel_report_project_paths.get_raw_output_folder()
        self.raw_obj = BaseProjectPaths.SentinelRawPackageData(raw_path)

    def test_get_all_default_files(self):
        self.raw_obj.get_all_default_files()
