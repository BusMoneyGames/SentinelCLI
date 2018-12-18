from Utilities import BaseSentinelTest
import logging
import SentinelUE4.Editor.commandlets as commandlets
L = logging.getLogger()

class TestResavePackages(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.resave_packages_commandlet = commandlets.ResavePackages(self.unreal_project_paths)

    def test_get_command(self):
        command = self.resave_packages_commandlet.get_command()
        print(command)

    def test_run(self):
        self.resave_packages_commandlet.run()


class TestCompileAllBlueprints(BaseSentinelTest.SentinelBaseTest):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.compile_blueprints=commandlets.CompileAllBlueprints(self.unreal_project_paths)

    def test_get_command(self):
        command = self.compile_blueprints.get_command()
        print(command)

    def test_run(self):
        self.compile_blueprints.run()


class TestRebuildLighting(BaseSentinelTest.SentinelBaseTest):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.rebuild_lighting = commandlets.RebuildLighting(self.unreal_project_paths)

    def test_get_command(self):
        command = self.rebuild_lighting.get_command()
        print(command)

    def test_run(self):
        self.rebuild_lighting.run()


class TestFillDDCCache(BaseSentinelTest.SentinelBaseTest):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.fill_ddc_cache = commandlets.FillDDCCache(self.unreal_project_paths)

    def test_get_command(self):
        command = self.fill_ddc_cache.get_command()
        print(command)

    def test_run(self):
        self.fill_ddc_cache.run()


class TestEditorRunner(BaseSentinelTest.SentinelBaseTest):
    def setUp(self):
        super().setUp()
        L.setLevel(logging.DEBUG)

        self.editor_runner = commandlets.EditorRunner(self.unreal_project_paths, "")

    def test_get_command(self):
        command = self.editor_runner.get_command()
        print(command)

    def test_run(self):
        self.editor_runner.run()

