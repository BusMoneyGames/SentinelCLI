# coding=utf-8
from unittest import TestCase
import logging
import os
import pprint

L = logging.getLogger(__name__)


class TestPkgLogObject(TestCase):
    def setUp(self):

        from SentinelUE4.LogParser import PkgCommandleLog
        self.pkgLogObj = PkgCommandleLog.PkgLogObject(self.get_test_data())

    def get_test_data(self):
        """
        Loads the test data file from disk
        :return:
        """

        folder_path = os.path.dirname(os.path.realpath(__file__))
        test_data_file = os.path.join(folder_path, "testdata", "T_TextureSample_pkgInfo.txt")

        L.debug(test_data_file)

        return test_data_file

    def test_get_asset_name(self):
        name = self.pkgLogObj.get_asset_name()
        print(name)

    def test__get_absolute_package_path(self):
        path = self.pkgLogObj._get_absolute_package_path()
        print(path)

    def test_get_data(self):
        data = self.pkgLogObj.get_data()
        pprint.pprint(data)

    def test_get_log_chapters(self):
        chapters = self.pkgLogObj.get_log_chapters()
        pprint.pprint(chapters)

    def test_get_package_info(self):
        package_info = self.pkgLogObj.get_package_info()

    def test_get_asset_references(self):
        asset_references = self.pkgLogObj.get_asset_references()
        pprint.pprint(asset_references)

    def test_get_asset_type(self):
        asset_type = self.pkgLogObj.get_asset_type()