from Utilities import BaseSentinelTest
import SentinelUE4.ue4_data_parse as ue4_data_parse
import logging
import CONSTANTS
from pprint import pprint

L = logging.getLogger()


class TestRawData(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        # TODO move this into a static folder instead of using whats in the ue4 project
        raw_data_path = self.unreal_project_paths.get_output_data_path(CONSTANTS.RAW_DATA_FOLDER_NAME)
        self.raw_data_object = ue4_data_parse.RawData(raw_data_path)

    def test_get_raw_data_path(self):
        print(self.raw_data_object.path_to_raw_data)

    def test_get_asset_of_type(self):
        self.raw_data_object.get_asset_types("Blueprint")
