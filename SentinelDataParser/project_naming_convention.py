import BaseProjectPaths


class NamingConvention:

    def __init__(self, path_obj: BaseProjectPaths.BasePaths):
        self.path_obj = path_obj
        self.parsed_data = BaseProjectPaths.SentinelParsedData(self.path_obj.get_parsed_data_path())
        self.asset_rules = path_obj.asset_rules

    def get_categories(self):

        naming_convention_report = {}

        for each_category in self.parsed_data.get_categories():
            naming_convention_report[each_category] = []

            category_rule = self.asset_rules.get_asset_rules_for_type(each_category)
            data = self.parsed_data.get_data_by_category(each_category)

            for each_asset in data:
                asset_name = each_asset["UnrealFileName"]

                if category_rule:
                    error_message = self._check_asset_name_against_rule(asset_name, category_rule)
                    convention = category_rule["Convention"]
                    if error_message == "Valid":
                        continue
                else:
                    error_message = "No Convention Defined"
                    convention = "N/A"

                naming_convention_report[each_category].append([asset_name,
                                                                error_message,
                                                                convention,
                                                                "Rename this asset"])

        return naming_convention_report

    def get_header_from_category(self, category):
        return ["AssetName", "IsValid", "Correct Convention", "Suggested Action"]

    def _check_asset_name_against_rule(self, asset_name, rule):

        asset_split = asset_name.split("_")

        prefix = asset_split[0]
        valid_prefix = False

        for each_prefix in rule["Prefix"]:
            each_prefix = each_prefix.lower()
            if each_prefix == prefix.lower():
                valid_prefix = True
                break

        if not valid_prefix:
            return "Invalid Prefix"

        number_of_segments = len(rule["Convention"].split("_"))

        if not number_of_segments == len(asset_split):
            return "Invalid name structure"

        return "Valid"

    def get_data_from_category(self, category):

        categories = self.get_categories()

        if category in categories:
            data = categories[category]
        else:
            data = []

        return data

    def get_naming_convention_data(self):
        pass