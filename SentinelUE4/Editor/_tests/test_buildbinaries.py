import unittest
import json
import Editor.buildcommands as buildcommands


class TestClientBuilder(unittest.TestCase):

    def setUp(self):
        f = open("../../_test_config.json")
        path_config = json.load(f)
        f.close()

        self.client_builder = buildcommands.UnrealClientBuilder(path_config)

    def test_build_client(self):
        self.client_builder.run()

    def test_get_command(self):
        self.client_builder.get_build_command()


class TestEditorBuilder(unittest.TestCase):

    def setUp(self):
        f = open("../../_test_config.json")
        path_config = json.load(f)
        f.close()

        self.editor_builder = buildcommands.UnrealEditorBuilder(path_config)

    def test_build_client(self):
        self.editor_builder.run()

    def test_get_command(self):
        self.editor_builder.get_build_command()


