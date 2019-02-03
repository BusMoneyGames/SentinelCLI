import unittest
import json
import logging
import Editor.commandlets as commandlets
import pathlib
import CONSTANTS
L = logging.getLogger()


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

        L.setLevel(logging.DEBUG)

        f = open("_test_config.json")
        path_config = json.load(f)
        f.close()

        self.compile_blueprints = commandlets.CompileAllBlueprints(path_config)

    def test_get_command(self):
        command = self.compile_blueprints.get_command()
        print(command)

    def test_run(self):
        self.compile_blueprints.run()


class TestRebuildLighting(unittest.TestCase):
    def setUp(self):
        L.setLevel(logging.DEBUG)

        f = open("_test_config.json")
        path_config = json.load(f)
        f.close()

        self.rebuild_lighting = commandlets.RebuildLighting(path_config)

    def test_get_command(self):
        command = self.rebuild_lighting.get_command()
        print(command)

    def test_run(self):
        self.skipTest("Light building is broken in the engine")
        self.rebuild_lighting.run()


class TestPackageInfoCommandlet(unittest.TestCase):
    def setUp(self):
        L.setLevel(logging.DEBUG)

        f = open("_test_config.json")
        self.path_config = json.load(f)
        f.close()

        files = self._get_test_files()
        self.package_info_commandlet = commandlets.PackageInfoCommandlet(self.path_config, files)

    def _get_test_files(self):
        content_value = self.path_config[CONSTANTS.UNREAL_PROJECT_STRUCTURE][CONSTANTS.UNREAL_CONTENT_ROOT_PATH]
        project_root = pathlib.Path(self.path_config[CONSTANTS.PROJECT_ROOT_PATH]).resolve()

        content_path = project_root.joinpath(content_value)

        files = []
        for i, each_file in enumerate(content_path.glob("**/*.uasset")):
            files.append(each_file)

            if i > 5:
                break

        return files

    def test_get_command(self):
        command = self.package_info_commandlet.get_command()
        print(command)

    def test_run(self):
        self.package_info_commandlet.run()


