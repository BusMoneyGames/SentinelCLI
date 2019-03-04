from SentinelConfig import SentinelConfig
from SentinelTests.shared import BaseCLITestComponent


class TestSentinelConfig(BaseCLITestComponent):

    def test_detailed_help(self):
        SentinelConfig.main(self._get_arguments(["-h"]))

    def test_default(self):

        SentinelConfig.main(["-default"])

    def _get_arguments(self, additional_arguments):
        return []

