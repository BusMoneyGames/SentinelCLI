from unittest import TestCase
import pathlib
import pprint

from SentinelUE4 import ue4_package_inspection
import SentinelUE4._tests as test_utilities


class TestPackageHashInfo(TestCase):
    def setUp(self):
        test_data_path = test_utilities.get_test_data_path()

        temp_archive_folder: pathlib.Path = test_data_path.joinpath("temp_archive_path")
        ue4_test_folder_directory: pathlib.Path = test_data_path.joinpath("ue4_files")

        test_files = self._get_all_files_from_directory(ue4_test_folder_directory)
        self.single_file = test_files[0]

        self.package_inspection_object = ue4_package_inspection.PackageHashInfo(test_files,
                                                                                temp_archive_folder)
    @staticmethod
    def _get_all_files_from_directory(directory: pathlib.Path):
        """
        Utility function to fetch all files in the test folder
        :param directory:
        :return:
        """

        files = []
        for e in directory.glob("*.*"):
            files.append(e)
        return files

    def test_archive_folder_path(self):
        pprint.pprint(self.package_inspection_object.archive_folder_root)

    def test_input_list_of_files(self):
        pprint.pprint(self.package_inspection_object.list_of_files)

    def test_hash_value_mappings(self):
        pprint.pprint(self.package_inspection_object.hash_value_mapping)

    def test_get_hash_from_filename(self):
        test_hash = self.package_inspection_object.get_hash_from_filename(self.single_file)
        pprint.pprint(test_hash)
