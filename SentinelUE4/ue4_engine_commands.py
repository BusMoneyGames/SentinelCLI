# coding=utf-8
import logging

# Needs to be imported first to make sure the config is applied before the other imports are run
from SentinelUE4.Editor import buildcommands

L = logging.getLogger(__name__)


def build_game_client(unreal_project_info):

    """
    Prepares the environment for a build and builds the client.
    :param unreal_project_info:
    :return: build object containing information about the build
    """

    L.info("Preparing to start a client build")
    # TODO make the build editor and client syntax be consistent ( now its build() and run()

    # Builds the editor if its needed
    if unreal_project_info.settings.get_should_compile():
        L.info("Compiling Editor Binaries")
        editor_build_obj = buildcommands.UnrealEditorBuilder(unreal_project_info)
        editor_build_obj.run()

    # Create the client build command
    build_obj = buildcommands.UnrealClientBuilder(unreal_project_info)
    build_obj.run()

    L.info("Client Build Finished")

    return build_obj