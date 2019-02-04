import CONSTANTS
import sys
import pathlib


class UEUtilities:

    def __init__(self, run_config, platform="Win64"):
        self.platform = platform
        self.run_config = run_config

        self.ue_structure = self.run_config[CONSTANTS.UNREAL_ENGINE_STRUCTURE]
        self.engine_root_path = pathlib.Path(self.run_config[CONSTANTS.ENGINE_ROOT_PATH]).resolve()
        self.project_root_path = pathlib.Path(self.run_config[CONSTANTS.PROJECT_ROOT_PATH]).resolve()

    def get_editor_executable_path(self):

        file_name = self.ue_structure[CONSTANTS.UNREAL_ENGINE_WIN64_CMD_EXE] + self._get_executable_ext()

        executable = self.engine_root_path.joinpath(self.ue_structure[CONSTANTS.UNREAL_ENGINE_BINARIES_ROOT],
                                                    self.platform,
                                                    file_name
                                                    )
        return executable

    def get_unreal_build_tool_path(self):

        engine_root_folder = pathlib.Path(self.run_config[CONSTANTS.ENGINE_ROOT_PATH]).resolve()
        engine_root_folder = engine_root_folder.joinpath("Engine")

        file_name = self.ue_structure[CONSTANTS.UNREAL_ENGINE_UBT_EXE] + self._get_executable_ext()
        executable = self.engine_root_path.joinpath(engine_root_folder,
                                                    file_name
                                                    )

        return executable

    def _get_executable_ext(self):
        if self.platform == "Win64":
            return ".exe"
        else:
            sys.exit(1)

    def get_project_file_path(self):
        uproject_files = []
        for each_file in self.project_root_path.glob("*.uproject"):
            uproject_files.append(each_file)

        if not len(uproject_files) == 1:
            sys.exit(1)

        project_file_path = uproject_files[0]

        return project_file_path

    def get_all_content_files(self):
        content_value = self.run_config[CONSTANTS.UNREAL_PROJECT_STRUCTURE][CONSTANTS.UNREAL_CONTENT_ROOT_PATH]
        project_root = pathlib.Path(self.run_config[CONSTANTS.PROJECT_ROOT_PATH]).resolve()

        content_path = project_root.joinpath(content_value)

        files = []
        for i, each_file in enumerate(content_path.glob("**/*.uasset")):
            files.append(each_file)

        return files
