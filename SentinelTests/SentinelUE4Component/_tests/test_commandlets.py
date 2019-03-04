import unittest
import Editor.commandlets as commandlets
from SentinelConfig import configelper as helper, CONSTANTS

import logging


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)

L = logging.getLogger()
L.setLevel(logging.DEBUG)


class TestDefaultCommandlets(unittest.TestCase):

    def setUp(self):
        helper.clean_compile_project()
        L.debug("Iterates through all the default commandlets and runs them")
        self.run_config = helper.generate_default_config()
        self.commandlets = dict(self.run_config[CONSTANTS.COMMANDLET_SETTINGS])

    def test_runAll(self):

        L.debug("Found %s commandlets", len(self.commandlets.keys()))
        L.debug("\n".join(self.commandlets.keys()))

        for each_commandlet in self.commandlets.keys():
            L.info(self.commandlets[each_commandlet])

    def test_compileblueprints(self):

        cmd = commandlets.BaseUE4Commandlet(run_config=self.run_config, commandlet_name="Compile-Blueprints")
        cmd.run()

    def test_resaveAllPackages(self):

        cmd = commandlets.BaseUE4Commandlet(run_config=self.run_config, commandlet_name="Resave-All-Packages")
        cmd.run()

    def test_resaveBlueprints(self):

        cmd = commandlets.BaseUE4Commandlet(run_config=self.run_config, commandlet_name="Resave-Blueprints")
        cmd.run()

    def test_resaveLevels(self):

        cmd = commandlets.BaseUE4Commandlet(run_config=self.run_config, commandlet_name="Resave-Levels")
        cmd.run()

    def tearDown(self):
        helper.reset_ue_repo()


