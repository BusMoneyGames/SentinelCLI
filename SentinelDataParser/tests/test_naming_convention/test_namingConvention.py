from Utilities import BaseSentinelTest
from SentinelDataParser import project_naming_convention
import pprint

class TestNamingConvention(BaseSentinelTest.SentinelBaseTest):

    def setUp(self):
        super().setUp()
        self.naming_convention = project_naming_convention.NamingConvention(self.sentinel_report_project_paths)

    def test_get_categories(self):
        data = self.naming_convention.get_categories()
        pprint.pprint(data)

    def test_get_naming_convention_data(self):
        self.naming_convention.get_naming_convention_data()

    def test__check_asset_name_against_rule(self):

        test_convention = {'Type': 'AnimSequence',
                           'Convention': '[Prefix]_[AssetName][Iterator]',
                           'Prefix': ['Anim'], 'Postfix': ['']}

        test_asset_name = "Anim_TestName01"

        test_result = self.naming_convention._check_asset_name_against_rule(test_asset_name, test_convention)
        print(test_result)
