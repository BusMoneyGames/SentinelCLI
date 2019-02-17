from Utilities import BaseSentinelTest
from SentinelUE4.Game.ClientOutput import ClientRunProcessor
import pathlib
import os


class TestClientRunProcessor(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):

        self.test_data_path = pathlib.Path(os.path.dirname(__file__)).joinpath("test_data",
                                                                               "sentinelTest_StaticMeshAssetTest01")
        super().setUp()

    def test_process_images(self):
        test_run = ClientRunProcessor.ClientRunProcessor(self.test_data_path)
        test_run.process_images()
