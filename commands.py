import click
import pathlib
import SentinelVCS.Vcs.GitComponent as GitComponent
import subprocess

import utilities
L = utilities.logger


def _run_component_cmd(cmd, args=None):

    if args is None or args == "":
        args = ""
    elif type(args) == list:
        args = "--" + " --".join(args)
    elif type(args) == str:
        # the case where the string is empty is dealt with at the top
        args = "--" + args
    elif type(args) == dict:
        args_string = ""
        for each_key in args.keys():
            args_string = args_string + each_key + "=" + args[each_key] + " "

        args = args_string
        print(args)

    component_cmd = "python sentinel.py standalone-components " + cmd + " " + args
    L.debug("cmd: %s", component_cmd)

    return_obj = subprocess.run(component_cmd)

    if not return_obj.returncode == 0:
        exit(1)


@click.group()
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', type=click.Choice(['true', 'false']), default='true', help="Skips output version")
@click.option('--debug', type=click.Choice(['true', 'false']), default='false',  help="Verbose logging")
@click.pass_context
def cli(ctx, project_root, output, no_version, debug):
    """Sentinel Commands"""

    ctx = utilities.convert_parameters_to_ctx(ctx,
                                              project_root=project_root,
                                              output=output,
                                              debug=debug,
                                              no_version=no_version)

    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "environment", "generate"], data)
    utilities.run_cmd(cmd)


@cli.command()
@click.pass_context
def build_game(ctx):
    """Create a playable version of the project"""

    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "ue4", "build", "client"], data)
    utilities.run_cmd(cmd)


@cli.command()
@click.pass_context
def build_editor(ctx):
    """Compile UE4 editor"""
    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "ue4", "build", "editor"], data)
    utilities.run_cmd(cmd)


@cli.command()
@click.pass_context
def validate_project(ctx):
    """Check settings and environment"""
    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "ue4", "build", "editor"], data)
    utilities.run_cmd(cmd)

@cli.command()
@click.pass_context
def validate_assets(ctx):
    """Checks the assets"""
    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "ue4", "project", "refresh-asset-info"], data)
    utilities.run_cmd(cmd)


@cli.command()
def run_client_test():
    """Start a game client and run automation tests"""
    pass


@cli.command()
@click.option('--project_name', default="", help="Name of the project")
@click.option('--engine_path', default="", help="Relative Path to the engine")
@click.option('--config_path', default="", help="Path to a custom config folder")
@click.option('--version_control_root', default="", help="Path to the version control root")
@click.option('--artifacts_root', default="", help="Path to the artifacts root")
@click.option('--s3_data_base_location', default="", help="path to the database location")
@click.option('--cache_path', default="", help="Path to the sentinel cache")
@click.pass_context
def process_missing(ctx,
                    project_name,
                    engine_path,
                    config_path,
                    version_control_root,
                    s3_data_base_location,
                    artifacts_root,
                    cache_path):

    """Goes through the history and runs validation"""

    arguments = ["project_name=" + project_name,
                 "engine_path=" + engine_path,
                 "config_path=" + config_path,
                 "version_control_root=" + version_control_root,
                 "s3_data_base_location=" + s3_data_base_location,
                 "artifacts_root=" + artifacts_root,
                 "cache_path="+cache_path]

    _run_component_cmd("environment make-default-config", arguments)
    _run_component_cmd("environment generate")

    # Reading the config to initialize the vcs walker
    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")

    environment_config = utilities.read_config(config_path)
    walker = GitComponent.GitRepoWalker(environment_config)

    for i, each_commit in enumerate(walker.commits):
        walker.clean_checkout_commit(each_commit)

        _run_component_cmd("environment make-default-config", arguments)
        _run_component_cmd("environment generate")
        _run_component_cmd("vcs refresh")
        _run_component_cmd("environment generate")
        _run_component_cmd("ue4 build editor")
        _run_component_cmd("ue4 project refresh-asset-info")
        _run_component_cmd("vcs write-history-file", "commit_id=" + walker.commit_ids[i])
        _run_component_cmd("python aws upload-build-data")


if __name__ == "__main__":
    cli()
