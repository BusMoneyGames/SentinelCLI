import BaseProjectPaths
import CONSTANTS


class CookLogParser:

    def __init__(self, path_obj: BaseProjectPaths.BasePaths):
        self.path_obj = path_obj

        path_obj.get_build_folder_path()
        build_folder_path = self.path_obj.get_build_folder_path()
        self.cook_log_path= build_folder_path.joinpath(CONSTANTS.COOK_LOG_OUTPUT_NAME)

    def get_warnings(self):
        lines = self.get_log_lines()

        warnings = []
        for each_line in lines:
            each_line = each_line.replace("\n", "")

            if "warning:" in each_line.lower():
                warnings.append(each_line)

        return warnings

    def get_log_lines(self):

        f = open(self.cook_log_path, "r")
        lines = f.readlines()
        f.close()

        return lines
