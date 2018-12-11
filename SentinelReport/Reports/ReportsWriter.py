import os
import pathlib
import shutil
import logging

# TODO Fix this import problem,  the reports should not be in the summary folder
from SentinelReport.Reports.ReportSummary import BaseOverviewPage, BaseDataTablePage, BaseLogDisplay, ClientTestOverviewPage

L = logging.getLogger()


class ReportsManager:

    """
    Handles generating the reports and linking htem
    """

    def __init__(self, base_environment_object):

        self.report_generators = []
        self.reports = []

        self.base_environment_object = base_environment_object
        self.output_folder_path = self.base_environment_object.get_reports_output_path()

    def add_report(self, report):

        self.reports.append(report)

    def _init_reports(self):

        for each_generator in self.report_generators:
            self.reports.extend(each_generator.get_reports())

    def add_index_page(self):
        L.info("Starting Index Page")
        report = BaseOverviewPage(self.output_folder_path, output_file_name="index.html")

        L.info("Finished Index page\n")
        return report

    @staticmethod
    def _copy_report_support_files(output_folder_path):

        """
        Copies the js, css or any files that are referenced in the reports to the output folder
        :return:
        """

        # Find the directory of the base report files
        reports_folder_root = pathlib.Path(os.path.dirname(__file__))
        base_report_root = reports_folder_root.joinpath("base_report")

        if output_folder_path.exists():
            shutil.rmtree(output_folder_path)

        shutil.copytree(base_report_root, output_folder_path)

        return base_report_root

    def write_all_reports(self):
        """
        Writes all reports to the output folder and copies the required files
        :return:
        """

        self._init_reports()
        self._copy_report_support_files(self.output_folder_path.joinpath("base_report"))

        # The index page needs information from most other pages so its dealt with as a special case
        index_page = self.add_index_page()

        # All the reports are ready and we inject the data that connects them such as an overview on the index page
        # and the navigation bar and links

        for each_raw_report in self.reports:
            if each_raw_report.show_on_dashboard:
                # Adding the panel information for each page
                index_page.link_to_page(each_raw_report)

        # Finally write the reports
        for each_report in self.reports:
            each_report.write_report()

        index_page.write_report()


