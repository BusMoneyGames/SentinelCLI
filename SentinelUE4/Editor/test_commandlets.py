import unittest
import json
import logging
import Editor.commandlets as commandlets

L = logging.getLogger()
import pathlib


class TestResavePackages(unittest.TestCase):

    def setUp(self):
        L.setLevel(logging.DEBUG)

        f = open("_test_config.json")
        path_config = json.load(f)
        f.close()

        self.resave_packages_commandlet = commandlets.ResavePackages(path_config)

    def test_get_command(self):
        command = self.resave_packages_commandlet.get_command()
        print(command)

    def test_run(self):
        self.resave_packages_commandlet.run()


class TestCompileAllBlueprints(unittest.TestCase):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.compile_blueprints=commandlets.CompileAllBlueprints(self.unreal_project_paths)

    def test_get_command(self):
        command = self.compile_blueprints.get_command()
        print(command)

    def test_run(self):
        self.compile_blueprints.run()


class TestRebuildLighting(unittest.TestCase):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.rebuild_lighting = commandlets.RebuildLighting(self.unreal_project_paths)

    def test_get_command(self):
        command = self.rebuild_lighting.get_command()
        print(command)

    def test_run(self):
        self.rebuild_lighting.run()


class TestFillDDCCache(unittest.TestCase):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.fill_ddc_cache = commandlets.FillDDCCache(self.unreal_project_paths)

    def test_get_command(self):
        command = self.fill_ddc_cache.get_command()
        print(command)

    def test_run(self):
        self.fill_ddc_cache.run()


class TestEditorRunner(unittest.TestCase):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.editor_runner = commandlets.EditorRunner(self.unreal_project_paths, "")

    def test_get_command(self):
        command = self.editor_runner.get_command()
        print(command)

    def test_run(self):
        self.editor_runner.run()

