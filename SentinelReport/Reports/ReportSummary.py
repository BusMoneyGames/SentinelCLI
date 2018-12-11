import json
import os
import pathlib
import logging

from jinja2 import Environment, FileSystemLoader, select_autoescape
from SentinelReport.Reports import REPORT_CONSTANTS

L = logging.getLogger()


class ReportSummary:

    def __init__(self):

        self.page_type = ""
        self.summary_description = ""
        self.number_of_entries = 0
        self.entries_descriptions = ""
        self.graphics_adapter = ""
        self.engine_version = ""
        self.build_config = ""
        self.icon = ""

        self.data = {}

    def add_value(self, key, value):

        self.data[key] = value

    def get_value(self, key):

        # Makes sure that the build in values have been added to the dict if someone tries to get values out of it
        self._refresh_data()

        if key in self.data:
            return self.data[key]
        else:
            L.warning("%s is not configured", key)
            return "No Value Configured"

    def _refresh_data(self):
        if self.page_type:
            self.data["page_type"] = self.page_type

        if self.icon:
            self.data["page_icon"] = "Data/" + self.icon
        else:
            self.data["page_icon"] = REPORT_CONSTANTS.DEFAULT_ICON

        # Graphics adapter
        if self.graphics_adapter:
            self.data["graphics_adapter"] = self.graphics_adapter
        else:
            self.data["graphics_adapter"] = "Unknown Graphics Adapter"

        # Graphics adapter
        if self.engine_version:
            self.data["engine_version"] = self.engine_version
        else:
            self.data["engine_version"] = "Unknown Engine Version"

        # Graphics adapter
        if self.build_config:
            self.data["build_config"] = self.build_config
        else:
            self.data["build_config"] = "Unknown Engine Config"

    def get_dict(self):
        self._refresh_data()

        return self.data


class BaseReport:
    """
    Handles writing html reports and moving around data related to that
    """

    def __init__(self,
                 output_folder_path,
                 template,
                 output_file_name):

        self.output_folder_path = output_folder_path
        self.report_name = output_file_name

        if not self.report_name.endswith(".html"):
            self.report_name = self.report_name + ".html"

        # Prepare the input data
        self.show_on_dashboard = True

        # Init the data structures
        self.links = []
        self.info_cards = []
        self.page_info = {}
        self.extra_data = {}
        self.client_results = []

        # Initialize an empty Page summary
        self.summary = ReportSummary()
        self.add_shared_values_to_summary()

        self.report = pathlib.Path(self.output_folder_path, self.report_name)

        base_report_root = self._get_templates_root()
        env = Environment(
            loader=FileSystemLoader(base_report_root.as_posix()),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.template = env.get_template(template)

    def add_shared_values_to_summary(self):
        self.summary.add_value("run_name", "Not Implemented")
        self.summary.add_value("report_time", "Not Implemented")
        self.summary.add_value("version_control_changelist", "Not Implemented")

    def construct_data_dict(self):
        """
        Initializes the structure that the html file reads
        :return:
        """

        relative_path_root = "base_report"

        report_data = \
            {"global": {"summary": self.summary.get_dict()},
             "infobox": self.page_info,
             "navigation": [],
             "content": {
                 "example_header": [],
                 "example_entries": [],
                 "links": self.links
             },
             "client_results": self.client_results,
             "root": relative_path_root,
             "extra": self.extra_data
             }

        return report_data

    @staticmethod
    def _get_templates_root():
        """
        Get path to the html templates used by the html template generation
        :return:
        """

        reports_folder_root = pathlib.Path(os.path.dirname(__file__))
        base_report_root = reports_folder_root.joinpath("base_report", 'templates')

        return base_report_root

    def write_report(self):
        """
        Write the report to disk and copies all
        :return:
        """
        data = self.construct_data_dict()

        self.save_report_data_as_json(data)
        a = self.template.render(data=data)

        L.debug("Writing report to: %s", self.report)

        f = open(self.report, "w")
        f.writelines(a)
        f.close()

        return self.report

    def get_card_data(self):

        """
        Get the information from the report that will be used on the index page
        :return:
        """

        L.debug("Get Card data for: %s", self.report_name)

        default_panel = {"header": self.summary.get_value("page_title"),
                         "number": 0,
                         "category": self.summary.page_type,
                         "text": self.summary.get_value("page_description"),
                         "path_to_page": self.report_name,
                         "icon": self.summary.get_value("page_icon")
                         }

        return default_panel

    def get_report_relative_path(self):

        relative_path = self.report.relative_to(self.output_folder_path)
        return relative_path

    def add_content_link(self, label, link):
        self.links.append({"label": label, "link": str(link)})

    def save_report_data_as_json(self, data):

        json_path = pathlib.Path(self.output_folder_path, self.report_name).with_suffix(".json")
        f = open(json_path, "w")
        json.dump(data, f, indent=4)
        f.close()

        L.debug("Saved data as json file: %s", json_path)


class BaseLogDisplay(BaseReport):

    def __init__(self, output_directory,
                 output_file_name):

        """
        The data dict needs to be structured like this:

        Category {header:[], values:[[]]}

        """

        super().__init__(output_directory,
                         "log_template"
                         ".html",
                         output_file_name)

        self.summary.page_type = "Build Info"
        self.summary.add_value("page_title", "Build Log")

    def add_log_lines(self, lines):
        self.extra_data["loglines"] = lines


class BaseDataTablePage(BaseReport):

    def __init__(self, output_directory,
                 output_file_name):

        """
        The data dict needs to be structured like this:

        Category {header:[], values:[[]]}

        """

        super().__init__(output_directory,
                         "datatable_template.html",
                         output_file_name)

        self.summary.page_type = "Project Info"
        self.summary.add_value("page_title", "Naming Convention Report")

    def add_table(self, table_title, header, values_list):

        self.extra_data[table_title] = {"header": header, "entries": values_list}


class BaseOverviewPage(BaseReport):

    def __init__(self, output_directory,
                 output_file_name):

        super().__init__(output_directory,
                         "index_template.html",
                         output_file_name)

    def link_to_page(self, page_to_link):

        # Fetch the panel info from the raw page
        panel_info = page_to_link.get_card_data()

        category = page_to_link.summary.get_value("page_type")

        if category in self.page_info:
            self.page_info[category].append(panel_info)
        else:
            self.page_info[category] = [panel_info]


class ClientTestOverviewPage(BaseReport):

    def __init__(self, base_environment_object, output_file_name):

        super().__init__(base_environment_object,
                         "screenshot_template.html",
                         output_file_name)

    def configure_card(self, page_title):
        self.summary.page_type = "Client Tests"
        self.summary.add_value("page_title", page_title)


class AssetOverviewPage(BaseOverviewPage):

    def __init__(self, base_environment_object, output_file_name):

        super().__init__(base_environment_object,
                         output_file_name)