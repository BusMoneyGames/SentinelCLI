import unittest
import json
from Editor.ue4_package_inspection import BasePackageInspection


class TestExtractPackages(unittest.TestCase):

    def setUp(self):
        f = open("../_test_config.json")
        self.path_config = json.load(f)
        f.close()

        self.package_inspection = BasePackageInspection(self.path_config)

    def test_extract_all_packages(self):
        self.package_inspection.extract_basic_package_information()


