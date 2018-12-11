from Utilities import BaseSentinelTest
import SentinelUE4.ue4_data_parse as ue4_data_parse
import logging
import pathlib
import CONSTANTS
from pprint import pprint

L = logging.getLogger()


class TestBaseExtractedObject(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)
        test_log = (pathlib.Path(__file__)).parent.joinpath("testdata", "BlueprintSample_Default.log")

        # TODO move this into a static folder instead of using whats in the ue4 project
        self.extracted_object = ue4_data_parse.BaseExtractedObject(test_log)

    def test_get_path(self):
        print(self.extracted_object.file_path)

