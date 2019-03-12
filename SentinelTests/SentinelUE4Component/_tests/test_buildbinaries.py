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


class TestSentinelUE4ComponentRun(BaseCLITestComponent):
    def test_run_default(self):
        SentinelUE4Component.main(self._get_arguments(["-run"]))

