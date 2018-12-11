from Utilities import BaseSentinelTest
import SentinelUnrealTool
import SentinelReportsTool


class TestSentinelUnrealTool(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        # Clear the archive folder
        # Delete the sentinel reports folder
        # Hard reset and clean the git project
        super().setUp()

    def test_build_game(self):
        SentinelUnrealTool.compile_editor(self.unreal_project_paths)
        SentinelUnrealTool.build_game(self.unreal_project_paths, should_deploy=False, should_store_build=False)

    def test_build_game_and_store(self):
        SentinelUnrealTool.compile_editor(self.unreal_project_paths)
        SentinelUnrealTool.build_game(self.unreal_project_paths, should_deploy=False, should_store_build=True)

    def test_extract_package(self):
        SentinelUnrealTool.extract_package_info(self.unreal_project_paths)

    def test_parse_package_info(self):
        SentinelUnrealTool.parse_package_info(self.unreal_project_paths)

    def test_compile_editor(self):
        SentinelUnrealTool.compile_editor(self.unreal_project_paths)

    def test_resave_packages_commandlet(self):
        SentinelUnrealTool.resave_packages_commandlet(self.unreal_project_paths)

    def test_compile_blueprints_commandlet(self):
        SentinelUnrealTool.compile_blueprints_commandlet(self.unreal_project_paths)

    def test_resave_blueprints_commandlet(self):
        SentinelUnrealTool.resave_blueprints_commandlet(self.unreal_project_paths)


class TestSentinelReportsTool(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        # Clear the archive folder
        # Delete the sentinel reports folder
        # Hard reset and clean the git project
        super().setUp()

    def test_generate_reports(self):
        SentinelReportsTool.generate_reports(self.sentinel_report_project_paths)
