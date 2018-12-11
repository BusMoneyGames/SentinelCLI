# coding=utf-8
import argparse

import SentinelUE4.ue4_package_inspection
from SentinelUE4 import ue4_project_info
from SentinelUE4 import ue4_engine_commands
from SentinelUE4 import ue4_data_parse
from SentinelUE4.Editor import buildcommands, commandlets

import Utilities.BaseSentinelLogging as SentinelLogging
L = SentinelLogging.root_logger


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-files", "--project_file_paths", nargs='+')

    parser.add_argument("-output_folder", "--output_folder_name", default="Default",
                        help="Overwrites the name of the output folder",)

    parser.add_argument("-package_info", "--extract_package_info", action="store_true",
                        help="Extract from client")

    parser.add_argument("-parse_info", "--parse_package_info", action="store_true",
                        help="Extract from client")

    parser.add_argument("-b", "--build_game", action="store_true",
                        help="Compiles and cooks a build")

    parser.add_argument("-c", "--compile_editor", action="store_true",
                        help="Compiles and cooks a build")

    parser.add_argument("-d", "--deploy", action="store_true",
                        help="Deploys a build to the configured location")

    parser.add_argument("-store_build", "--store_build_for_testings", action="store_true",
                        help="Moves the build into the testing folder for more _tests")

    parser.add_argument("-resave_packages", "--resave_packages_commandlet", action="store_true",
                        help="resaves the packages in the project based on the settings in the sentinel config file")

    parser.add_argument("-check_blueprints", "--compile_blueprints_commandlet", action="store_true",
                        help="Compiles the blueprints in the project and outputs a report")

    parser.add_argument("-resave_blueprints", "--resave_blueprints_commandlet", action="store_true",
                        help="Compiles the blueprints in the project and outputs a report")

    parser.add_argument("-rebuild_lighting", "--rebuild_lighting_commandlet", action="store_true",
                        help="Compiles the blueprints in the project and outputs a report")

    parser.add_argument("-generate_built_data", "--generate_built_data_commandlet", action="store_true",
                        help="Compiles the blueprints in the project and outputs a report")

    parser.add_argument("-fill_ddc", "--fill_ddc_cache", action="store_true",
                        help="Compiles the blueprints in the project and outputs a report")

    args = parser.parse_args()

    # Creating the path object based on the settings
    unreal_project_info = ue4_project_info.ProjectPaths(output_version=args.output_folder_name,
                                                        files=args.project_file_paths
                                                        )

    if args.build_game:
        build_game(unreal_project_info, args.deploy, args.store_build_for_testings)

    if args.extract_package_info:
        extract_package_info(unreal_project_info)

    if args.parse_package_info:
        parse_package_info(unreal_project_info)

    if args.compile_editor:
        compile_editor(unreal_project_info)

    if args.resave_packages_commandlet:
        resave_packages_commandlet(unreal_project_info)

    if args.compile_blueprints_commandlet:
        compile_blueprints_commandlet(unreal_project_info)

    if args.resave_blueprints_commandlet:
        resave_blueprints_commandlet(unreal_project_info)

    if args.rebuild_lighting_commandlet:
        rebuild_lighting_commandlet(unreal_project_info)

    if args.generate_built_data_commandlet:
        generate_build_data_commandlet(unreal_project_info)

    if args.fill_ddc_cache:
        fill_ddc_cache(unreal_project_info)


def fill_ddc_cache(unreal_project_info):

    cmd = commandlets.FillDDCCache(unreal_project_info)
    cmd.run()

def generate_build_data_commandlet(unreal_project_info):
    L.info("Generating built data")
    cmd = commandlets.GenerateBuiltData(unreal_project_info)
    cmd.run()


def rebuild_lighting_commandlet(unreal_project_info):
    L.info("Starting Rebuild lighting commandlet")
    cmd = commandlets.RebuildLighting(unreal_project_info)
    cmd.run()


def resave_blueprints_commandlet(unreal_project_info):
    L.info("Starting Resave all blueprints commandlet")
    cmd = commandlets.ResaveAllBlueprints(unreal_project_info)
    cmd.run()


def compile_blueprints_commandlet(unreal_project_info):
    L.info("Starting checking blueprints commandlet")
    cmd = commandlets.CompileAllBlueprints(unreal_project_info)
    cmd.run()


def resave_packages_commandlet(unreal_project_info):
    L.info("Starting resave packages commandlet")
    cmd = commandlets.ResavePackages(unreal_project_info)
    cmd.run()


def compile_editor(unreal_project_info):
    L.info("Starting binaries compile")
    editor_compiler = buildcommands.UnrealEditorBuilder(unreal_project_info)
    editor_compiler.run()


def parse_package_info(unreal_project_info):
    L.info("Running Parse Package Info")
    ue4_data_parse.convert_raw_data_to_json(unreal_project_info)


def extract_package_info(unreal_project_info):
    L.info("Running Extract Package Info")
    package_inspection = SentinelUE4.ue4_package_inspection.BasePackageInspection(unreal_project_info)
    package_inspection.extract_basic_package_information()


def build_game(unreal_project_info, should_deploy, should_store_build):
    L.info("Running Build Game")
    # By default we don't compress the build unless another flag is passed in
    build_obj = ue4_engine_commands.build_game_client(unreal_project_info)
    if should_deploy:
        # Deploy the build to the configured location
        build_obj.deploy_to_configured_deploy_path()
    else:
        # Copies the build to the sentinel output folder for testing
        if should_store_build:
            L.info("Moving build to sentinel folder...")
            build_obj.deploy_to_sentinel_reports_folder()


if __name__ == "__main__":
    main()
