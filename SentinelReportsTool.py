# coding=utf-8
import argparse
import BaseProjectPaths
import SentinelReport.sentinel_generate_reports

import logging

import Utilities.BaseSentinelLogging as SentinelLogging
L = SentinelLogging.root_logger


def generate_reports(base_path_object):
    SentinelReport.sentinel_generate_reports.generate_reports(base_path_object)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-output_folder", "--output_folder_name", default="Default",
                        help="Overwrites the name of the output folder",)

    parser.add_argument("-reports", "--generate_reports", action="store_true",
                        help="Generates all reports")

    args = parser.parse_args()

    # Creating the path object based on the settings
    base_path_object = BaseProjectPaths.BasePaths(output_version=args.output_folder_name,
                                                  files=[]
                                                  )
    if args.generate_reports:
        generate_reports(base_path_object)


if __name__ == "__main__":
    main()
