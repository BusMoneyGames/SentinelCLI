import unittest
import SentinelConfig.configelper as helper
import logging

L = logging.getLogger()


class BaseCLITestComponent(unittest.TestCase):

    def setUp(self):
        # helper.clean_compile_project()
        path_config = helper.generate_default_config()
        self.default_arguments = ["-config=" + str(path_config)]

    def _get_arguments(self, additional_arguments):

        arguments = additional_arguments

        additional_arguments.extend(self.default_arguments)
        L.info("Running %s %s ", " ".join(arguments))

        return arguments
