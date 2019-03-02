import unittest
import Editor.buildcommands as buildcommands
from SentinelConfig import configelper as helper

import logging


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)

L = logging.getLogger()
L.setLevel(logging.DEBUG)


class TestClientBuilder(unittest.TestCase):

    def setUp(self):
        helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()

        self.client_builder = buildcommands.UnrealClientBuilder(path_config)

    def test_build_client(self):
        self.client_builder.run()

    def test_get_command(self):
        cmd = self.client_builder.get_build_command()
        print(cmd)

    def test_build_server(self):
        path_config = helper.get_path_config_for_test()

        cmd = buildcommands.UnrealClientBuilder(path_config, build_config_name="server")
        cmd.run()

    def tearDown(self):
        helper.reset_ue_repo()


class TestEditorBuilder(unittest.TestCase):

    def setUp(self):
        helper.clean_compile_project()
        path_config = helper.get_path_config_for_test()
        self.editor_builder = buildcommands.UnrealEditorBuilder(path_config)

    def test_build_client(self):
        self.editor_builder.run()

    def test_get_command(self):
        cmd = self.editor_builder.get_build_command()
        print(cmd)

    def tearDown(self):
        helper.reset_ue_repo()


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

