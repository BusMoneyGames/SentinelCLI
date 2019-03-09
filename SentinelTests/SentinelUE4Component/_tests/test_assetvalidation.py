import unittest
from SentinelConfig import configelper as helper
from Validation import assetvalidation

import SentinelTests.shared as shared
L = shared.get_logger()


class TestAssetValidation(unittest.TestCase):

    def setUp(self):
        self.run_config = helper.generate_default_config()


    def test_dostuff(self):
        assetvalidation.Validate(self.run_config).run()