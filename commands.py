import logging
import click
import os
import json
import pathlib
import SentinelVCS.Vcs.GitComponent as GitComponent
import subprocess

from logging.config import fileConfig
fileConfig('logging_config.ini')
L = logging.getLogger()


def _read_config(path):
    """Reads the assembled config"""

    L.debug("Config path: %s - Exists: %s", path, path.exists())

    if path.exists():
        f = open(path, "r")
        config = json.load(f)
        f.close()

        return config
    else:
        L.error("No config found: %s ", path)
        quit(1)


def _run_component_cmd(cmd, args=None):

    if args is None or args == "":
        args = ""
    elif type(args) == list:
        args = "--" + " --".join(args)
    elif type(args) == str:
        # the case where the string is empty is dealt with at the top
        args = "--" + args

    component_cmd = "python sentinel.py standalone-components " + cmd + " " + args
    L.debug("Running cmd: %s", component_cmd)

    subprocess.run(component_cmd)


@click.group()
@click.option('--root', default="", help="Path to the config overwrite folder")
@click.pass_context
def cli(ctx, root):
    """Sentinel Commands"""
    L.debug("This is happening")
    run_directory = pathlib.Path(os.getcwd())
    project_root = run_directory.parent

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root.as_posix()

    L.debug("project root path: %s", project_root.as_posix())


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
    # default_config_cmd = default_config_cmd + " --" + " --".join(arguments)

    # Generate the first default config
    # subprocess.run(default_config_cmd)

    # Reading the config to initialize the vcs walker
    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")

    environment_config = _read_config(config_path)
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
