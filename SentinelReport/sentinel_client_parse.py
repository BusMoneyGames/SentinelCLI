import os
import shutil
import logging

import CONSTANTS
from SentinelUE4.Game import GamePaths

from Utilities import fileutils as fileutils

L = logging.getLogger()


def save_client_run_data(path_obj):

    build_folder_path = path_obj.get_output_data_path(CONSTANTS.BUILD_FOLDER_PATH)
    output_path = path_obj.get_output_data_path(CONSTANTS.CLIENT_TEST_RESULT_FOLDER_NAME)
    raw_client_output_folder_path = path_obj.get_output_data_path(CONSTANTS.CLIENT_RAW_OUTPUT_FOLDER_NAME)

    L.info("Output Folder Path: %s", output_path)
    game_name = path_obj.get_project_name()
    game_paths = GamePaths.GamePaths(build_folder_path, game_name)

    # Copy the test output to the raw client data folder so it can be processed
    raw_client_path = os.path.join(raw_client_output_folder_path, game_name)

    if os.path.exists(raw_client_path):
        L.info("Deleting: %s", raw_client_path)
        shutil.rmtree(raw_client_path)

    shutil.copytree(game_paths.get_saved_folder_path(), raw_client_path)

    return


def copy_and_compress_screenshots(target_folder, source_folder_root):

    output_folder = target_folder
    saved_folder_path = source_folder_root
    list_of_png_files = fileutils.get_all_file_paths_of_type_in_directory(saved_folder_path, ".png")

    L.info("Found %s screenshots", str(len(list_of_png_files)))

    L.info("Starting image compression")

    compressed_files = fileutils.compress_png_to_jpg(list_of_png_files)
    flat_screenshot_directiory = os.path.join(output_folder, "img")

    if not os.path.exists(flat_screenshot_directiory):
        os.makedirs(flat_screenshot_directiory)

    for each_compressed_file in compressed_files:
        screenshot_name = os.path.basename(each_compressed_file)
        shutil.move(each_compressed_file, os.path.join(flat_screenshot_directiory, screenshot_name))

