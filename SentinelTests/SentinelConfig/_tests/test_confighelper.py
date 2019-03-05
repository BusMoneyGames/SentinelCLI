from SentinelConfig import SentinelConfig
from SentinelTests.shared import BaseCLITestComponent
import os
import pathlib

import logging


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)

L = logging.getLogger()
L.setLevel(logging.DEBUG)


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
        print('sadfasfd')

        SentinelConfig.main(["-generate", "-path="+str(self.overwrite_config_dir)])

