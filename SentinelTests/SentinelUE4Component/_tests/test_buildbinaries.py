from SentinelTests.shared import BaseCLITestComponent
from SentinelUE4Component import SentinelUE4Component

import SentinelTests.shared as shared
L = shared.get_logger()


class TestSentinelUE4ComponentBuild(BaseCLITestComponent):

    def test_detailed_help(self):
        SentinelUE4Component.main(self._get_arguments(["-detailed_help"]))

    def test_build_default(self):

        SentinelUE4Component.main(self._get_arguments(["-build", "-debug"]))


class TestSentinelUE4ComponentValidate(BaseCLITestComponent):

    def test_validate_default(self):
        SentinelUE4Component.main(self._get_arguments(["-validate"]))

    def test_validate_package_inspection(self):
        SentinelUE4Component.main(self._get_arguments(["-validate", "-validation_inspect"]))

    def test_validate_all_blueprints(self):
        SentinelUE4Component.main(self._get_arguments(["-validate", "-validation_tasks=Compile-Blueprints"]))

    def test_validate_resave_all_packages(self):
        SentinelUE4Component.main(self._get_arguments(["-validate", "-validation_tasks=Resave-All-Packages"]))

    def test_validate_resave_blueprints(self):
        SentinelUE4Component.main(self._get_arguments(["-validate", "-validation_tasks=Resave-Blueprints"]))

    def test_validate_resave_levels(self):
        SentinelUE4Component.main(self._get_arguments(["-validate", "-validation_tasks=Resave-Levels"]))


class TestSentinelUE4ComponentRun(BaseCLITestComponent):
    def test_run_default(self):
        SentinelUE4Component.main(self._get_arguments(["-run"]))

