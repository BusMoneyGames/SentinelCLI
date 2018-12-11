import argparse
import BaseProjectPaths
from Utilities import S3

import Utilities.BaseSentinelLogging as SentinelLogging
L = SentinelLogging.root_logger

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-output_folder", "--output_folder_name", default="Default",
                        help="Overwrites the name of the output folder",)

    parser.add_argument("-upload_reports", "--upload_reports_to_web", action="store_true",
                        help="Uploads reports to the web")


    args = parser.parse_args()

    # Creating the path object based on the settings

    project_paths = BaseProjectPaths.BasePaths(output_version=args.output_folder_name, files=[])
    if args.upload_reports_to_web:
        S3.upload_reports(project_paths)


if __name__ == "__main__":
    main()
