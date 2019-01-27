# coding=utf-8
import pathlib
import os
import CONSTANTS
import json
import logging
import random
import shutil
import datetime
import sys

L = logging.getLogger()
L.setLevel(logging.INFO)


class BasePaths:

    """
    Base paths initializes the paths within the game project and the environment.  A path object is constructed
    before any operation is started which contains settings and configurations
    """

    def __init__(self, output_version="Default", files=None):

        # Setting the output version to default
        self.output_version = output_version

        if not files:
            self.files = []

        self.project_root_folder = ""
        self.project_root_folder = self.get_project_root_folder_path()

        # Load config files
        self.settings_file_root_folder = ""
        self.settings_file_root_folder = self.get_settings_file_root()

        self._load_settings_file()
        self._load_asset_config_file()

        self.start_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.changelist_number = "Not Implemented"

        # Overwriting with files if they are set
        if files:
            self.overwrite_files_to_process(files)

        self.raw_package_info = SentinelRawPackageData(self.get_output_data_path(CONSTANTS.RAW_DATA_FOLDER_NAME))

    def delete_all_reports(self):
        L.info("Deleting all logs from: %s", self.get_sentinel_output_root_path())
        output_path = self.get_sentinel_versioned_output_path()
        L.info("Path: %s", output_path)
        try:
            shutil.rmtree(output_path)
        except Exception as ex:
            L.warning(ex)
            L.warning("Unable to remove old reports path")

    def _load_asset_config_file(self):
        asset_config_path = os.path.join(self.settings_file_root_folder, CONSTANTS.SENTINEL_ASSET_RULES)
        self.asset_rules = SentinelAssetRules(asset_config_path)

    def _load_settings_file(self):
        settings_file_path = os.path.join(self.settings_file_root_folder, CONSTANTS.SETTINGS_FILE_NAME)
        L.debug("Reading settings file from: %s", settings_file_path)
        self.settings = SentinelSettingsFile(settings_file_path, self.project_root_folder)

    def get_files_to_process(self):
        """
        Returns a list of files that should be used in the environment run,  these files can come from a few sources
        such as from the vcs,  overwritten in the sentinel settings file or just all files in the project

        The list off files is populated on init bug can be overwritten by calling overwrite_files_to_process()
        :return: list of absolute paths from within the project
        """

        full_paths = []

        for each_path in self.files:
            full_path = self.settings._convert_relative_path_to_absolute_path(each_path)
            full_paths.append(full_path)

        random.shuffle(full_paths)
        return full_paths

    def overwrite_files_to_process(self, list_of_files):
        """
        overwrites the list of files to process.
        :param list_of_files:
        :return: None
        """

        L.info("Files to process overwritten with: %", list_of_files)
        self.files = list_of_files

    def get_settings_file_root(self):

        if not self.settings_file_root_folder:
            self.settings_file_root_folder = self.recursively_search_for_file_down_a_directory(file_suffix=".json",
                                                                                        file_name="sentinel_settings")
        return self.settings_file_root_folder

    def get_raw_output_folder(self):

        path = os.path.join(self.get_output_data_path(CONSTANTS.RAW_DATA_FOLDER_NAME))

        if not os.path.exists(path):
            os.mkdir(path)

        return pathlib.Path(path)

    def get_project_root_folder_path(self):

        if not self.project_root_folder:
            self.project_root_folder = self.recursively_search_for_file_down_a_directory(file_suffix=".uproject")

        return self.project_root_folder

    @staticmethod
    def recursively_search_for_file_down_a_directory(file_suffix, file_name=""):
        """
        finds the folder path of the script
        :return: root path
        """

        script_file = pathlib.PurePath(os.path.realpath(__file__))

        # TODO fix this so that it searches for the path down until we hit the root of scripts folder

        # Walks down the folder structure looking for the uproject file to identify the root of the project
        level_to_check = len(script_file.parents) - 1
        file_path = ""

        while level_to_check >= 0:
            path_to_check = pathlib.Path(script_file.parents[level_to_check])

            for each_file in path_to_check.glob("*.*"):

                # Check if the file has the correct suffix
                if each_file.suffix == file_suffix and file_name == "":

                    # If the filename is not set then we just return the first one we find
                    if not file_name:
                        # Return the folder path
                        file_path = each_file.parents[0]
                        break

                else:
                    # If there is a file name along with the extention,  match that
                    if each_file.suffix == file_suffix and file_name.lower() in each_file.name.lower():
                        file_path = each_file.parents[0]
                        break

            level_to_check = level_to_check - 1

        if not file_path:
            L.error("Unable to find folder path")

        return file_path

    def _get_script_folder(self):

        script_file = pathlib.PurePath(os.path.realpath(__file__))
        path_obj = pathlib.Path(script_file.parents[2])

        return path_obj

    def get_reports_output_path(self):
        """
        :return: path to report output folder
        """

        return self.get_output_data_path(CONSTANTS.REPORTS_OUTPUT_FOLDER_NAME)

    def get_reports_data_root_path(self):

        path = os.path.join(self.get_reports_output_path(), CONSTANTS.REPORTS_DATA_FOLDER_NAME)

        if not os.path.exists(path):
            os.mkdir(path)

        return pathlib.Path(path)

    def get_output_data_path(self, output_folder_name):

        output_folder = os.path.join(self.get_sentinel_versioned_output_path(), output_folder_name)

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        output_folder = pathlib.Path(output_folder)

        return output_folder

    def get_web_data_directory(self):

        path = os.path.join(self.get_sentinel_versioned_output_path(), CONSTANTS.WEB_DATA_FOLDER_NAME)

        return path

    def get_web_template_folder(self):

        path = os.path.join(self._get_script_folder(), "Reports", CONSTANTS.WEB_TEMPLATE_FOLDER_PATH)

        return path

    def get_tested_data_output_directory(self):

        path = os.path.join(self.get_sentinel_versioned_output_path(), CONSTANTS.TESTED_DATA_FOLDER_NAME)

        if not os.path.exists(path):
            os.mkdir(path)

        return path

    def get_build_folder_path(self):
        build_folder = self.get_output_data_path(CONSTANTS.BUILD_FOLDER_PATH)

        if not os.path.exists(build_folder):
            os.mkdir(build_folder)

        return pathlib.Path(build_folder)

    def get_client_test_directory(self):
        build_folder = self.get_output_data_path(CONSTANTS.BUILD_FOLDER_PATH)
        path = os.path.join(build_folder, CONSTANTS.CLIENT_TEST_RESULT_FOLDER_NAME)

        if not os.path.exists(path):
            os.mkdir(path)

        return pathlib.Path(path)

    def get_sentinel_output_root_path(self):
        path = os.path.join(self.settings_file_root_folder, CONSTANTS.SENTINEL_OUTPUT_FOLDER_NAME)

        L.debug("Sentinel report root path: %s", path)

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def get_sentinel_versioned_output_path(self):

        self.get_sentinel_output_root_path()

        path = os.path.join(self.get_sentinel_output_root_path(), self.output_version)

        L.debug("Sentinel report versioned path: %s", path)

        if not os.path.exists(path):

            os.makedirs(path)

        return path

    def get_raw_data_settings_path(self, file_name):

        L.debug("file_name %s", file_name)

        raw_data_path = self.get_output_data_path(CONSTANTS.RAW_DATA_FOLDER_NAME)
        path = os.path.join(raw_data_path, file_name)
        L.debug("Path: %s", path)

        return path

    def load_raw_data_settings(self, file_name):

        L.debug("Loading settings for file: %s", file_name)
        raw_data_path = self.get_output_data_path(CONSTANTS.RAW_DATA_FOLDER_NAME)

        f = open(os.path.join(raw_data_path, file_name), "r")
        settings_json = json.load(f)
        f.close()

        return settings_json

    def load_settings(self, file_name):

        L.debug("Loading settings for file: %s", file_name)

        f = open(os.path.join(self.settings_file_root_folder, file_name), "r")
        settings_json = json.load(f)
        f.close()

        return settings_json

    def get_value_from_default_settings(self, key):
        settings = self.load_settings(CONSTANTS.SETTINGS_FILE_NAME)

        return settings[key]

    def get_upload_credential_dict(self):
        credentials = self.get_value_from_default_settings(CONSTANTS.AMAZON_CREDENTIALS_SETTINGS)

        return credentials

    def get_parsed_data_path(self):

        return self.get_output_data_path(CONSTANTS.PARSED_DATA_FOLDER_NAME)

    def get_archive_folder_path(self):

        archive_path_from_config = os.path.join(self.settings.get_archive_path(), self.settings.get_project_identifier())

        if not os.path.exists(archive_path_from_config):
            os.makedirs(archive_path_from_config)

        L.debug(archive_path_from_config)

        return pathlib.Path(archive_path_from_config)

    def _read_path_from_config(self, config_file_path):
        """
        Reads a path from the settings file and makes sure that relative paths are correctly converted based
        on the location of the settings file
        :return: path
        """

        original_working_path = os.getcwd()  # remember our original working directory

        os.chdir(self.get_project_root_folder_path())
        path = os.path.abspath(config_file_path)

        p = pathlib.PurePath(path)

        os.chdir(original_working_path)  # get back to our original working directory

        return p

    def get_files_from_path(self, path, ext=""):

        if not ext.startswith(".") and not ext == "":
            ext = "." + ext

        file_list = []
        path = pathlib.Path(path)
        for f in path.resolve().glob('**/*'):
            if f.is_file():
                # Add all files
                if not ext:
                    file_list.append(f)
                else:
                    # Only add files that have the suffix
                    if f.suffix == ext:
                        file_list.append(f)

        return file_list


class SentinelParsedData:

    def __init__(self, path_to_parsed_data):
        self.path_to_parsed_data = path_to_parsed_data

        self._parsed_files = []

    def get_parsed_files(self):
        """

        :return:
        """
        if self._parsed_files:
            return self._parsed_files

        for each_folder in self.path_to_parsed_data.glob('**/*'):
            self._parsed_files.append(each_folder)

        return self._parsed_files

    def get_categories(self):
        asset_type_list = []
        for each_file in self.get_parsed_files():
            asset_type = self._get_file_type(each_file)

            if asset_type not in asset_type_list:
                asset_type_list.append(asset_type)

        return asset_type_list

    def get_data_by_category(self, category):

        parsed_files = self.get_parsed_files()

        data_list = []
        for each_parsed_file in parsed_files:
            if category == self._get_file_type(each_parsed_file):
                data = self._read_json_file(each_parsed_file)
                data_list.append(data)

        return data_list

    def _read_json_file(self, path):

        f = open(path, "r")
        json_data = json.load(f)
        f.close()

        return json_data

    def _get_file_type(self, path):
        asset_type = ""
        data = self._read_json_file(path)
        if "AssetType" in data:
            asset_type = data["AssetType"]

        if not asset_type:
            L.warning("Unable to determine the asset type from %s ", path)

        return asset_type

class SentinelRawPackageData:

    def __init__(self, path_to_raw_folder):
        self.path_to_raw_folder = pathlib.Path(path_to_raw_folder)

    def get_all_default_files(self):
        """

        :return: all folders that end with Default.Log
        """

        default_files = []
        for each_folder in self.path_to_raw_folder.glob('*/*_Default.log'):
            default_files.append(each_folder)

        return default_files


class SentinelSettingsFile:

    def __init__(self, settings_file_path, project_root_path):

        f = open(settings_file_path, "r")
        self.data = json.load(f)
        L.info("Read settings file from: " + settings_file_path)
        f.close()

        self.project_root_path = project_root_path

    def get_project_identifier(self):
        value = self._get_value_from_data("project_identifier")
        L.debug(value)

        return value

    def get_upload_credential_dict(self):
        return self._get_value_from_data(CONSTANTS.AMAZON_CREDENTIALS_SETTINGS)

    def get_archive_path(self):
        env_path = self._check_for_env_variable(CONSTANTS.ENV_ARCHIVE_PATH_PREFIX)

        if env_path:
            path = pathlib.Path(env_path)
        else:
            config_path = self._get_value_from_data("archive_path")
            path = self._convert_relative_path_to_absolute_path(config_path)
            path = pathlib.Path(path)

        if not path.exists():
            L.debug("Creating new folder for %s", path.as_posix())
            os.makedirs(path)

        return path

    def get_deploy_path(self):
        path = self._get_value_from_data("deploy_path")
        abs_path = self._convert_relative_path_to_absolute_path(path)
        L.debug(abs_path)

        return abs_path

    def get_build_settings(self):
        value = self._get_value_from_data("build_settings")
        L.debug(value)

        return value

    def get_engine_path(self):
        # First check if we have an environment variable configured for the engine path
        env_variable_path = self._check_for_env_variable(CONSTANTS.ENV_ENGINE_PATH_PREFIX)
        L.debug("environment variable path: %s", env_variable_path)

        # Check for default engine path
        default_engine_path = pathlib.Path(self.project_root_path).joinpath("UnrealEngine")
        L.debug("Default Engine Path: %s", default_engine_path)

        if env_variable_path:
            path = pathlib.Path(env_variable_path)
            L.info("Engine found at config variable")
        elif default_engine_path.exists():
            path = default_engine_path.joinpath("Engine")
            L.info("Engine found at default path")
        else:
            # Check if there is a hardcoded path in config file
            engine_path = self._get_value_from_data("engine_path")
            path = self._convert_relative_path_to_absolute_path(engine_path)
            path = pathlib.Path(path)

        if path.exists():
            L.info("Found Unreal Engine path at %s", path.as_posix())
        else:
            L.info("Unable to find unreal engine path.. ")
            L.error("Exiting...")
            sys.exit(3)

        return path

    def _check_for_env_variable(self, prefix):
        project_identifier = self.get_project_identifier()
        env_variable_name = prefix + project_identifier.upper()
        L.info("Searching for env variable: %s", env_variable_name)
        value = os.environ.get(env_variable_name)

        if value:
            L.info("Found %s", value)
            return value
        else:
            L.info("No environment variable configured")
            return None

    def get_should_compile(self):
        build_settings = self.get_build_settings()
        value = self._get_value_from_data("should_compile", build_settings)
        value = bool(value)

        return value

    def get_compile_flags(self):
        build_settings = self.get_build_settings()
        value = self._get_value_from_data("compile_flags", build_settings)

        return self._add_dash_infront_of_flag(value)

    def get_build_configuration(self):

        build_settings = self.get_build_settings()
        value = self._get_value_from_data("build_configuration", build_settings)

        return value

    def get_build_platform(self):

        build_settings = self.get_build_settings()
        value = self._get_value_from_data("build_platform", build_settings)

        return value

    def get_build_command(self):

        build_settings = self.get_build_settings()
        value = self._get_value_from_data("build_command", build_settings)

        return value

    def get_commandlet_settings(self, commandlet_name):
        build_settings = self.get_build_settings()
        all_commandlets = self._get_value_from_data('commandlets', build_settings)

        if commandlet_name in all_commandlets:
            return all_commandlets[commandlet_name]
        else:
            L.warning("No Commandlet config found for: " + commandlet_name)

    def get_build_flags(self):
        build_settings = self.get_build_settings()
        value = self._get_value_from_data("build_flags", build_settings)

        return self._add_dash_infront_of_flag(value)

    def get_include_maps_with_prefix(self):

        build_settings = self.get_build_settings()
        value = self._get_value_from_data("include_maps_with_prefix", build_settings)

        return value

    def get_client_settings(self):
        value = self._get_value_from_data("client_settings")
        L.debug(value)

        return value

    def get_client_test_extra_settings(self):

        client_settings = self.get_client_settings()
        value = self._get_value_from_data("test_config", client_settings)

        return value

    def get_client_extra_settings_for_test(self, test_name):

        all_test_configs = self.get_client_test_extra_settings()

        extra_settings = {}
        for each_extra_settings in all_test_configs:
            if "name" in each_extra_settings:
                name = each_extra_settings["name"]

            if test_name == name:

                extra_settings = each_extra_settings
                break

        return extra_settings

    def get_client_tests_to_run(self):
        client_settings = self.get_client_settings()

        value = self._get_value_from_data("tests_to_run", client_settings)

        return value

    def _convert_relative_path_to_absolute_path(self, relative_path):

        original_path = os.getcwd()

        os.chdir(self.project_root_path)
        abspath = os.path.abspath(relative_path)
        os.chdir(original_path)

        return abspath

    def _get_value_from_data(self, key, data=None):

        if not data:
            data = self.data

        if key in data:
            L.debug("Reading %s from config file", str(data[key]))
            return data[key]
        else:
            L.error("Unable to find %s in config", key)
            return ""

    def _add_dash_infront_of_flag(self, list_of_flags):
        flags = []
        for each_compile_flag in list_of_flags:
            flags.append("-" + each_compile_flag)

        return flags


class SentinelAssetRules:

    def __init__(self, settings_file_path):
        try:
            f = open(settings_file_path, "r")
            self.data = json.load(f)
            L.debug("Read settings file from")
            f.close()
            self.asset_rules_dict = self.data["AssetRules"]
        except:
            self.data = {}

            self.asset_rules_dict = {}

    def get_asset_rules_for_type(self, asset_type):

        """
        Iterate through the list of available types and matches the type with the input asset type
        :param asset_type:
        :return: asset rule dict
        """

        for each_asset_rule in self.asset_rules_dict:
            if each_asset_rule["Type"].lower() == asset_type.lower():
                return each_asset_rule

    def has_subtype(self, asset_type):

        asset_rules = self.get_asset_rules_for_type(asset_type)

        if "Subtypes" in asset_rules:
            return True
        else:
            return False

    def get_subtypes(self, asset_type):

        """
        Fetch the subtypes for the asset
        :param asset_type:
        :return:
        """

        asset_rules = self.get_asset_rules_for_type(asset_type)
        subtypes = asset_rules["Subtypes"]

        return subtypes