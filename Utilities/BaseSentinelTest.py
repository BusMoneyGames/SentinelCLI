# coding=utf-8
import logging
import pathlib
from unittest import TestCase
import os

# TODO not make the base unit test depened on the UE4 project paths
from SentinelUE4.ue4_project_info import ProjectPaths
import BaseProjectPaths

import Utilities.BaseSentinelLogging

L = logging.getLogger()
L.setLevel(logging.DEBUG)


class SentinelBaseTest(TestCase):

    def setUp(self):
        # Initializes both path objects,  for this to work
        self.unreal_project_paths = ProjectPaths(output_version="unittest_output", files=None)
        self.sentinel_report_project_paths = BaseProjectPaths.BasePaths(output_version="unittest_output", files=None)

    @staticmethod
    def is_path_valid(path):
        path_exists = os.path.exists(path)
        L.debug("Testing path: %s exists: %s", path, path_exists)

        return path_exists

    @staticmethod
    def get_all_files_from_path(path):
        """
        Return
        :param path:
        :return:
        """
        file_list = []
        path = pathlib.Path(path)
        for each_file in path.glob('*'):
            file_list.append(each_file)

        return file_list