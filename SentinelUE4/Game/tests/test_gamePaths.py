# coding=utf-8
from Utilities import BaseSentinelTest

from SentinelUE4 import ue4_project_info
from SentinelUE4.Game import GamePaths


class TestGamePaths(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):

        path_obj = ue4_project_info.ProjectPaths()
        build_folder_path = path_obj.get_output_data_path("Build")
        game_name = path_obj.get_project_name()

        self.game_paths = GamePaths.GamePaths(build_folder_path, game_name)


    def test_get_saved_folder_path(self):

        self.game_paths.get_saved_folder_path()

    def test_get_run_log(self):

        self.game_paths.get_log_file_path()

