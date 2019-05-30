import click
import logging
import pathlib
import os
import json
import subprocess

L = logging.getLogger()


def _read_config(path):
    """Reads the assembled config"""

    L.debug("Reading config from: %s - Exists: %s", path, path.exists())

    if path.exists():
        f = open(path, "r")
        config = json.load(f)
        f.close()

        return config
    else:
        L.error("Unable to find generated config at: %s ", path)
        quit(1)


@click.group()
@click.option('--path', default="", help="path to the config overwrite folder")
@click.option('--debug', default=False, help="Turns on debug messages")
@click.pass_context
def cli(ctx, path, debug):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    if debug:
        L.setLevel(logging.DEBUG)
        message_format = '%(levelname)s - %(message)s '
    else:
        message_format = '%(levelname)s %(message)s '
        L.setLevel(logging.ERROR)

    logging.basicConfig(format=message_format)
    run_directory = pathlib.Path(os.getcwd())

    if path:
        custom_path = pathlib.Path(path)
        if custom_path.absolute():
            config_file_root_dir = path
        else:
            config_file_root_dir = run_directory.joinpath(path)
    else:
        # Default is one level up from current directory
        config_file_root_dir = run_directory.parent

    config_file_path = config_file_root_dir.joinpath("_sentinel_root.json")
    L.debug("Reading config file from: %s Exists: %s", config_file_path, config_file_path.exists())

    ctx.ensure_object(dict)
    ctx.obj['CONFIG_ROOT'] = path
    ctx.obj['GENERATED_CONFIG_PATH'] = config_file_path
    ctx.obj['RUN_CONFIG'] = _read_config(config_file_path)


@cli.command()
@click.argument('args', nargs=-1)
@click.pass_context
def environment(ctx, args):
    """Local Environment Options"""
    subprocess.run("python ./SentinelConfig/SentinelConfig.py " + " ".join(args))


@cli.command()
@click.argument('args', nargs=-1)
@click.pass_context
def ue4(ctx, args):
    """Unreal Engine Options"""
    subprocess.run("python ./SentinelUE4Component/SentinelUE4Component.py " + " ".join(args))


@cli.group()
def vcs():
    """Fetch information from version control"""


if __name__ == "__main__":
    cli()
