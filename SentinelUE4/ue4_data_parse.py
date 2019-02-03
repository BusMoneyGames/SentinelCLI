# coding=utf-8
# Needs to be imported first to make sure the config is applied before the other imports are run

import os
import json
import logging

import CONSTANTS
from LogParser import PkgCommandleLog

L = logging.getLogger(__name__)


def convert_raw_data_to_json(base_path_object):
    """
    Goes through all the raw extracted files and extracts any data of interest out of it.  The data of interest is then
    Saved as a json file

    # Find the sentinel output folder
    # Find the test folder
    # Iterate through all the raw package data files
    # Convert each raw file to json file
    # Move files to the parsed folder

    """

    files = base_path_object.raw_package_info.get_all_default_files()

    # Parsed output folder
    parsed_folder_name = base_path_object.get_output_data_path(CONSTANTS.PARSED_DATA_FOLDER_NAME)

    # Goes through each raw file and saves it out as a json file
    for each_raw_file_path in files:
        # Create the pkg object
        each_pkg_obj = PkgCommandleLog.PkgLogObject(each_raw_file_path)
        # Gets the name of the asset
        asset_name = each_pkg_obj.get_asset_name()

        # Save single json file
        path = os.path.join(parsed_folder_name, asset_name + ".json")

        f = open(path, 'w')
        # Saves the package object data to disk
        json.dump(each_pkg_obj.get_data(), f, indent=4)
        f.close()

        L.debug("Wrote: " + str(path))


