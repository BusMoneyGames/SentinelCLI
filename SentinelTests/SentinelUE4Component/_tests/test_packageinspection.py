import unittest
import logging
import Editor.packageinspection as packageinspection

from SentinelConfig import configelper as helper

L = logging.getLogger()


class TestInspectPackages(unittest.TestCase):

    def setUp(self):
        self.is_first_run = True
        L.setLevel(logging.DEBUG)

        if self.is_first_run:
            helper.clean_compile_project()
            self.is_first_run = False

        run_config = helper.generate_default_config()
        self.package_inspection = packageinspection.BasePackageInspection(run_config)

    def test_extract_basic_package_information(self):
        self.package_inspection.run(clean=True)

    def test_get_files_in_project(self):
        self.package_inspection.get_files_in_project()


class TestProcessPackageInfo(unittest.TestCase):

    def setUp(self):
        L.setLevel(logging.DEBUG)
        run_config = helper.generate_default_config()

        self.package_processor = packageinspection.ProcessPackageInfo(run_config)

    def test_convert_raw_data_to_json(self):

        self.package_processor.run()
