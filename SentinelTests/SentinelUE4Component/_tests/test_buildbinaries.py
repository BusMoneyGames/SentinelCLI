import unittest
import Editor.buildcommands as buildcommands
from SentinelUE4Component import SentinelUE4Component
from SentinelConfig import configelper as helper

import logging


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)

L = logging.getLogger()
L.setLevel(logging.DEBUG)


class TestSentinelUE4ComponentBuild(unittest.TestCase):

    def setUp(self):
        # helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()
        self.default_arguments = ["-config=" + str(path_config)]

        self.commandline_name = "SentinelUE4Component.py"

    def test_help(self):
        SentinelUE4Component.main(["-h"])

    def test_build_default(self):

        arguments = ["-build"]
        arguments.extend(self.default_arguments)
        L.info("Running %s %s ", self.commandline_name, " ".join(arguments))
        SentinelUE4Component.main(arguments)


class TestSentinelUE4ComponentVerify(unittest.TestCase):
    def setUp(self):
        # helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()
        self.default_arguments = ["-config=" + str(path_config)]

        self.commandline_name = "SentinelUE4Component.py"

    def test_verify_default(self):
        arguments = ["-verify"]
        arguments.extend(self.default_arguments)
        L.info("Running %s %s ", self.commandline_name, " ".join(arguments))
        SentinelUE4Component.main(arguments)


class TestSentinelUE4ComponentRun(unittest.TestCase):
    def setUp(self):
        # helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()
        self.default_arguments = ["-config=" + str(path_config)]

        self.commandline_name = "SentinelUE4Component.py"

    def test_verify_default(self):
        arguments = ["-run"]
        arguments.extend(self.default_arguments)
        L.info("Running %s %s ", self.commandline_name, " ".join(arguments))
        SentinelUE4Component.main(arguments)


class TestBuildShaderCompiler(unittest.TestCase):

    def setUp(self):
        self.path_config = helper.get_path_config_for_test()
        self.shader_compile_builder = buildcommands.EditorComponentBuilder(self.path_config)

    def test_shader_compiler_builder(self):
        cmd = self.shader_compile_builder = buildcommands.EditorComponentBuilder(self.path_config,
                                                                                 component_name="ShaderCompileWorker")
        cmd.run()

    def test_lightmass_builder(self):
        cmd = self.shader_compile_builder = buildcommands.EditorComponentBuilder(self.path_config,
                                                                                 component_name="UnrealLightmass")
        cmd.run()

