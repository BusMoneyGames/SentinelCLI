import re


class BuildLogParser:

    def __init__(self, log_file_path):

        if log_file_path:
            f = open(log_file_path)
            self.data = f.read()
            f.close()
        else:
            self.data = ""

    def extract_errors(self):

        # Find all lines that contain errors
        warnings = []

        for m in re.finditer(r'(Warning: .*)', self.data, flags=re.MULTILINE):
            matched_string = m.group()
            warnings.append(matched_string)

        # Remove duplicates
        warnings = list(set(warnings))

        return warnings
