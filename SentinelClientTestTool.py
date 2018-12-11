import argparse
import BaseProjectPaths
from SentinelUE4 import ue4_client_commands

import Utilities.BaseSentinelLogging as SentinelLogging
L = SentinelLogging.root_logger


def run_startup_tests(project_paths):
    ue4_client_commands.run_startup_test(project_paths)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-output_folder", "--output_folder_name", default="Default",
                        help="Overwrites the name of the output folder",)

    parser.add_argument("-run_tests", "--run_all_client_tests", action="store_true",
                        help="Runs the client _tests and extracts the output data")

    args = parser.parse_args()

    # Creating the path object based on the settings

    project_paths = BaseProjectPaths.BasePaths(output_version=args.output_folder_name, files=[])

    if args.run_all_client_tests:
        run_startup_tests(project_paths)

if __name__ == "__main__":
    main()
