from Utilities import BaseSentinelTest
import BaseProjectPaths

import pprint


class TestSentinelParsedData(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        parsed_data_path = self.sentinel_report_project_paths.get_parsed_data_path()
        self.parsed_obj = BaseProjectPaths.SentinelParsedData(parsed_data_path)

    def test_get_all_files(self):
        self.parsed_obj.get_parsed_files()

    def test_get_data_by_category(self):
        data = self.parsed_obj.get_data_by_category("Texture2D")
        pprint.pprint(data)

    def test_get_categories(self):
        categories = self.parsed_obj.get_categories()
        print(categories)