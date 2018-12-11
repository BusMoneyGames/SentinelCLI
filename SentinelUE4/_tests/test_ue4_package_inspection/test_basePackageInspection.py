from Utilities import BaseSentinelTest
import SentinelUE4.ue4_package_inspection as ue4_package_inspection
import logging
from pprint import pprint

L = logging.getLogger()


class TestBasePackageInspection(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)
        self.package_inspection = ue4_package_inspection.BasePackageInspection(self.unreal_project_paths)

    def test_get_files_in_project(self):
        files = self.package_inspection.get_files_in_project()
        pprint(files)

    def test_get_file_hash_info(self):
        file_hash_obj = self.package_inspection.get_file_hash_info()

        pprint(file_hash_obj.hash_value_mapping)

    def test_get_archive_info(self):
        archive_info = self.package_inspection.get_archive_info()
        archive_info.get_missing_files()

    def test_extract_basic_package_information(self):

        self.package_inspection.extract_basic_package_information()

    def test_recover_files_from_archive(self):
        self.package_inspection.recover_files_from_archive()

