from Utilities import BaseSentinelTest
import SentinelUE4.ue4_package_inspection as ue4_package_inspection
import logging
from pprint import pprint

L = logging.getLogger()


class TestExtractedDataArchive(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)
        archive_folder_path = self.unreal_project_paths.get_archive_folder_path()

        # TODO not make this test depend on another test
        self.package_inspection = ue4_package_inspection.BasePackageInspection(self.unreal_project_paths)
        file_hash_info_obj = self.package_inspection.get_file_hash_info()

        self.archive_obj = ue4_package_inspection.ExtractedDataArchive(archive_folder_path, file_hash_info_obj.hash_value_mapping)

    def test_get_missing_files(self):
        self.archive_obj.get_missing_files()
