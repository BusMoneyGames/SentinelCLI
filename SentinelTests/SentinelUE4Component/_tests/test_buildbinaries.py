import unittest
from SentinelUE4Component import SentinelUE4Component
from SentinelConfig import configelper as helper

import logging


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)

L = logging.getLogger()
L.setLevel(logging.DEBUG)


class BaseCLITestComponent(unittest.TestCase):

    def setUp(self):
        # helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()
        self.default_arguments = ["-config=" + str(path_config)]

        self.commandline_name = "SentinelUE4Component.py"

    def _get_arguments(self, additional_arguments):

        arguments = additional_arguments

        additional_arguments.extend(self.default_arguments)
        L.info("Running %s %s ", self.commandline_name, " ".join(arguments))

        return arguments


class TestSentinelUE4ComponentBuild(BaseCLITestComponent):

    def test_detailed_help(self):
        SentinelUE4Component.main(self._get_arguments(["-detailed_help"]))

    def test_build_default(self):

        SentinelUE4Component.main(self._get_arguments(["-build"]))


class TestSentinelUE4ComponentValidate(BaseCLITestComponent):

    def test_validate_default(self):
        SentinelUE4Component.main(self._get_arguments(["-validate"]))


class TestSentinelUE4ComponentRun(BaseCLITestComponent):
    def test_run_default(self):
        SentinelUE4Component.main(self._get_arguments(["-run"]))

