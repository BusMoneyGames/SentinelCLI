from SentinelConfig import SentinelConfig
from SentinelTests.shared import BaseCLITestComponent
import os
import pathlib

import SentinelTests.shared as shared
L = shared.get_logger()


class TestSentinelConfig(BaseCLITestComponent):

    def setUp(self):
        script_file = pathlib.PurePath(os.path.realpath(__file__))
        self.overwrite_config_dir = script_file.parent.joinpath("overwrite_config")

    def test_detailed_help(self):
        SentinelConfig.main(self._get_arguments(["-h"]))

    def test_default(self):

        SentinelConfig.main(["-generate"])

    def _get_arguments(self, additional_arguments):
        return []

    def test_generate_overwrite(self):

        print(self.overwrite_config_dir)

        SentinelConfig.main(["-generate", "-path="+str(self.overwrite_config_dir)])

