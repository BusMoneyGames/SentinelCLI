# coding=utf-8
import subprocess
import os
import logging
import CONSTANTS
import shutil
import pathlib
import Editor.editorutilities as editorUtilities
L = logging.getLogger(__name__)


class BaseUnrealBuilder:
    """
    Base class for triggering builds for an unreal engine project
    """

    def __init__(self, run_config):

        """
        :param unreal_project_info:
        """

        self.run_config = run_config
        self.all_build_settings = self.run_config[CONSTANTS.UNREAL_BUILD_SETTINGS_STRUCTURE]

        # TODO Add logic to be able to switch the build settings
        self.build_settings = self.all_build_settings["win64_build_settings"]

        self.platform = self.build_settings[CONSTANTS.UNREAL_BUILD_PLATFORM_NAME]

        self.editor_util = editorUtilities.UEUtilities(run_config, self.platform)

        self.project_root_path = pathlib.Path(run_config[CONSTANTS.PROJECT_ROOT_PATH]).resolve()
        self.sentinel_project_structure = self.run_config[CONSTANTS.SENTINEL_PROJECT_STRUCTURE]

        sentinel_project_name = self.sentinel_project_structure[CONSTANTS.SENTINEL_PROJECT_NAME]
        sentinel_logs_path = self.sentinel_project_structure[CONSTANTS.SENTINEL_RAW_LOGS_PATH]

        self.log_output_folder = self.project_root_path.joinpath(sentinel_project_name,
                                                                 sentinel_logs_path)

        self.log_output_file_name = "Default_Log.log"

    def get_build_command(self):
        """
        Needs to be overwritten on child
        :return:
        """
        return ""

    def run(self):
        """
        No logic in the base class, should be overwritten on the child
        :return:
        """

        cmd = self.get_build_command()

        path = self.log_output_folder.joinpath(self.log_output_file_name)

        if not path.exists():
            os.makedirs(path.parent)

        L.info(cmd)

        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        with open(path, "w", encoding='utf-8') as fp:
            for line in popen.stdout:
                line = line.decode('utf-8').rstrip()
                print(line, flush=True)
                print(line, file=fp, flush=True)

        # Waiting for the process to close
        popen.wait()

        # quiting and returning with the correct return code
        if popen.returncode == 0:
            L.info("Command run successfully")
        else:
            import sys
            L.warning("Process exit with exit code: %s", popen.returncode)
            sys.exit(popen.returncode)


class UnrealEditorBuilder(BaseUnrealBuilder):

    """
    Handle building the unreal editor binaries for the game project
    """

    def __init__(self, unreal_project_info):
        """
        Uses the settings from the path object to compile the editor binaries for the project
        so that we can run a client build or commandlets
        :param unreal_project_info:
        """

        super().__init__(unreal_project_info)

        self.log_output_file_name = CONSTANTS.COMPILE_LOG_OUTPUT_NAME

    def get_build_command(self):
        """
        Construct the build command string
        :return: build command
        """

        project_path = "-project=" + "\"" + self.unreal_project_info.get_project_path().as_posix() + "\""

        # TODO after upgrading to 4.20 then I need to skip the project name to be able to compile the editor
        cmd_list = [self.unreal_project_info.get_ue4_UnrealBuildTool_path(),
                    #self.unreal_project_info.get_project_name(),
                    "Development",  # The editor build is always development
                    self.unreal_project_info.settings.get_build_platform(),
                    project_path,
                    ]

        # Adding the compile flags at the end of the settings
        cmd_list.extend(self.unreal_project_info.settings.get_compile_flags())

        cmd = " ".join(cmd_list)

        L.debug("Build command: %s", cmd)

        return cmd


class UnrealClientBuilder(BaseUnrealBuilder):
    """
    Handles making client builds of the game project that can be either archived for testing or deployed to the
    deploy location
    """

    def __init__(self, run_config, platform="Win64"):
        """
        Use the settings from the path object to build the client based on the settings in the settings folder
        :param unreal_project_info:
        """
        super().__init__(run_config)
        self.log_output_file_name = self.sentinel_project_structure[CONSTANTS.SENTINEL_DEFAULT_COOK_FILE_NAME]

        self.editor_util = editorUtilities.UEUtilities(run_config, platform)

        self.compressed_path = ""

    @staticmethod
    def _prefix_config_with_dash(list_of_strings):

        new_list = []
        for each in list_of_strings:
            new_list.append("-"+each)

        return new_list

    def get_build_command(self):
        """
        Construct the build command string
        :return: build command
        """

        project_path = self.editor_util.get_project_file_path()
        engine_path = self.editor_util.get_editor_executable_path()
        engine_root = pathlib.Path(self.run_config[CONSTANTS.ENGINE_ROOT_PATH]).resolve()

        build_command_name = self.build_settings[CONSTANTS.UNREAL_BUILD_COMMAND_NAME]
        build_config = self.build_settings[CONSTANTS.UNREAL_BUILD_CONFIGURATION]

        # self.get_cook_list_string()

        run_uat_path = engine_root.joinpath("Engine", "Build", "BatchFiles", "RunUAT.bat")

        cmd_list = [str(run_uat_path),
                    build_command_name,
                    "-project=" + str(project_path),
                    "-clientconfig=" + build_config
                    ]

        config_flags = self._prefix_config_with_dash(self.build_settings[CONSTANTS.UNREAL_BUILD_CONFIG_FLAGS])
        cmd_list.extend(config_flags)
        cmd = " ".join(cmd_list)
        L.debug(cmd)

        print(cmd)
        return cmd

    def get_cook_list_string(self):
        # all_files = self.unreal_project_info.get_all_content_files()
        all_files = []
        maps_to_package = []
        for e in all_files:

            if e.suffix == ".umap":
                lower_name = e.name.lower()
                maps_to_package.append(lower_name)
                L.debug("Adding %s to cook list", lower_name)

                # TODO Add filtering based on prefixes from the settings file
        # TODO enable the maps to package flag again
        maps_to_package_flag = "-Map=\"" + "+".join(maps_to_package) + "\""

    def run(self):
        """
        Constructs the build command and runs it
        :return: None
        """

        # Deleting the old build from the staging folder
        # old_build_path = self.unreal_project_info.get_staged_build_path()

        # if os.path.exists(old_build_path):
            # L.info("Deleting old build from path: %s", old_build_path)
            # fileutils.delete_folder(old_build_path)

        super(UnrealClientBuilder, self).run()


    def deploy_to_sentinel_reports_folder(self):
        """
        Copies the newly made build to the sentinel deploy folder
        :return: None
        """

        sentinel_reports_build_folder = self.unreal_project_info.get_output_data_path(CONSTANTS.BUILD_FOLDER_PATH)
        L.info("Deploying the build to: %s", sentinel_reports_build_folder)

        staged_build_folder = self.unreal_project_info.get_staged_build_path()
        project_name = self.unreal_project_info.get_project_name()
        zipped_build = fileutils.zip_folder(staged_build_folder, project_name + ".zip")

        target_file = sentinel_reports_build_folder.joinpath(project_name + ".zip")

        if target_file.exists():
            os.remove(target_file)

        shutil.copyfile(zipped_build, target_file.as_posix())

        # Copies the file

        return sentinel_reports_build_folder.as_posix()

    def deploy_to_configured_deploy_path(self):
        """
        Copies the newly made build to the deploy location configured in the sentinel settings file
        :return:
        """

        network_deploy_path = self.unreal_project_info.settings.get_deploy_path()
        L.debug(network_deploy_path)

        user_name = os.environ.get("USERNAME")
        L.debug("User Name: %s", user_name)

        project_name = self.unreal_project_info.get_project_name()
        L.debug("Project Name: %s", project_name)

        run_vr_path = self.unreal_project_info.get_staged_build_path().joinpath("run_vr.bat")

        f = open(run_vr_path,"w")
        f.writelines(["Vikingar.exe -vr"]) 
        f.close()

        target_path = os.path.join(network_deploy_path, user_name, project_name)
        target_path = os.path.abspath(target_path)
        L.info("Preparing to copy build to: %s", target_path)

        cmd = "robocopy /MIR " + str(self.unreal_project_info.get_staged_build_path()) + " " + target_path
        L.debug("Copy Command: %s", cmd)

        subprocess.call(cmd)
