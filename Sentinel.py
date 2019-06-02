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


def get_commandline(script, arguments, data=None):
    """
    Constructs the command line that gets passed into the different sentinel commands
    :return:
    """
    cmd = "python " + script

    if data:
        pass_through_arguments = " "
        for each_data in data.keys():
            pass_through_arguments = pass_through_arguments + each_data + "=" + data[each_data]
    else:
        pass_through_arguments = ""

    if arguments:
        # Only add the pass through arguments if there is a command
        cmd = cmd + pass_through_arguments + " " + " ".join(arguments)

    return cmd


@click.group()
@click.option('--project_root', default="", help="path to the config overwrite folder")
@click.option('--debug', default=False, help="Turns on debug messages")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def cli(ctx, project_root, debug, output):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    run_directory = pathlib.Path(os.getcwd())
    project_root = run_directory.parent

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root.as_posix()


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def environment(ctx, args):
    """Local Environment Options"""

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}
    cmd = get_commandline("./SentinelConfig/SentinelConfig.py", args, data)
    subprocess.run(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def ue4(ctx, args):
    """Unreal Engine Options"""

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}

    cmd = get_commandline("./SentinelUE4Component/SentinelUE4Component.py ", args, data)
    subprocess.run(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def vcs(ctx, args):

    """Fetch information from version control"""
    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}
    cmd = get_commandline("./SentinelVCSComponent/SentinelVCSComponent.py", args, data)
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()
