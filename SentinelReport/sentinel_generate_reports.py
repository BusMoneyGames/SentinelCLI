import BaseProjectPaths
import SentinelDataParser.project_naming_convention as project_naming_convention
import SentinelDataParser.build_log_parser as build_log_parser
import pathlib
import shutil
import os
from SentinelUE4.Game.ClientOutput import ClientRunProcessor

from SentinelReport.Reports import ReportsWriter


def move_screenshots_to_relative_path(report_root, list_of_screenshots):

    img_folder = report_root.joinpath("img")
    relative_paths = []

    if not img_folder.exists():
        os.makedirs(img_folder)

    for each_screenshot in list_of_screenshots:
        each_screenshot = pathlib.Path(each_screenshot)
        screenshot_path = img_folder.joinpath(each_screenshot.name)
        shutil.copy(each_screenshot, screenshot_path)

        relative_path = screenshot_path.relative_to(report_root)
        relative_paths.append(relative_path.as_posix())

    return relative_paths

def generate_client_run_reports(base_path_object: BaseProjectPaths.BasePaths):
    reports = []

    # Client run tests
    client_test_dir = base_path_object.get_client_test_directory()

    for each_client_test in client_test_dir.glob('*'):

        # Each test output folder
        if each_client_test.is_dir():

            reports_root_folder = base_path_object.get_reports_output_path()
            output_file_name = each_client_test.name
            client_test_report = ReportsWriter.ClientTestOverviewPage(reports_root_folder,
                                                                      output_file_name)

            client_test_report.configure_card(each_client_test.name)
            client_tests = ClientRunProcessor.ClientRunProcessor(each_client_test)
            test_obj = client_tests.get_graphic_test_objects()

            # Each part of the test
            for each_test_entry in test_obj:

                gpu_stats = each_test_entry.get_gpu_frame_overview()
                relative_paths = move_screenshots_to_relative_path(reports_root_folder,
                                                                   each_test_entry.screenshot_paths)

                dummy_test_result = {"frame_overview": {"Milliseconds": gpu_stats["Milliseconds"],
                                                        "Triangles": gpu_stats["Triangles"],
                                                        "Draws": gpu_stats["Draws"]},
                                     "name": each_test_entry.base_name,
                                     "images": relative_paths,
                                     "type_name": each_test_entry.screenshot_types,
                                     "gpu_overview": [["Value 1", "Value 2", "Value 3", "Value 4"],
                                                      ["Value 1", "Value 2", "Value 3", "Value 4"]],
                                     "gpu_data": each_test_entry.raw_gpu_data,
                                     }
                client_test_report.client_results.append(dummy_test_result)

            reports.append(client_test_report)

    return reports


def generate_reports(base_path_object: BaseProjectPaths.BasePaths):

    """
    Generates the naming convention report
    :return:
    """

    report_gen = ReportsWriter.ReportsManager(base_path_object)
    naming_convention_obj = project_naming_convention.NamingConvention(base_path_object)

    cook_log_obj = build_log_parser.CookLogParser(base_path_object)
    data = naming_convention_obj.get_categories()

    reports_root_folder = base_path_object.get_reports_output_path()
    naming_convention_report = ReportsWriter.BaseDataTablePage(reports_root_folder, "naming_convention")
    log_file_report = ReportsWriter.BaseLogDisplay(reports_root_folder, "cook_log")

    # Cook log
    lines = cook_log_obj.get_warnings()
    log_file_report.add_log_lines(lines)

    # client test report

    for each_category in data:
        header = naming_convention_obj.get_header_from_category(each_category)
        category_entries = naming_convention_obj.get_data_from_category(each_category)
        naming_convention_report.add_table(each_category, header, category_entries)

    report_gen.add_report(log_file_report)
    report_gen.add_report(naming_convention_report)

    client_reports = generate_client_run_reports(base_path_object)
    for each_report in client_reports:
        report_gen.add_report(each_report)

    report_gen.write_all_reports()
