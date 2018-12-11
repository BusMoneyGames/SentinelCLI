from Utilities import BaseSentinelTest
from SentinelUE4 import ue4_data_parse

class TestConvert_raw_data_to_json(BaseSentinelTest.SentinelBaseTest):

    def test_convert_raw_data_to_json(self):
        ue4_data_parse.convert_raw_data_to_json(self.unreal_project_paths)
