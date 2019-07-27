import click
import logging
import pathlib
import os
import json
import subprocess

from logging.config import fileConfig
fileConfig('logging_config.ini')
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


def get_commandline(script, global_argument, data=None, arguments_at_end=False):
    """
    Constructs the command line that gets passed into the different sentinel commands
    :return:
    """
    cmd = "python " + script

    if data:
        pass_through_arguments = " "

        for each_data in data.keys():
            pass_through_arguments = pass_through_arguments + each_data + "=" + data[each_data] + " "

    else:
        pass_through_arguments = ""

    if global_argument:
        # Only add the pass through arguments if there is a command
        # cmd = cmd + pass_through_arguments + " " + " ".join(arguments)
        arguments = " ".join(global_argument)

        # Flips the arguments to go at the end
        # TODO understand why this is needed
        if arguments_at_end:
            cmd = cmd + " " + arguments + pass_through_arguments
        else:
           cmd = cmd + pass_through_arguments + " " + arguments

    # print(cmd)

    return cmd


def _run_cmd(cmd):
    return_object = subprocess.run(cmd, shell=True)

    if not return_object.returncode == 0:
        quit(1)


@click.group()
@click.option('--root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', is_flag=True, default=True, help="Skips output version")
@click.option('--debug', is_flag=True, default=False, help="Verbose logging")
@click.pass_context
def cli(ctx, root, debug, output, no_version):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    run_directory = pathlib.Path(os.getcwd())
    project_root = run_directory.parent

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root.as_posix()
    ctx.obj['SKIP_VERSION'] = str(no_version)

    if debug:
        L.setLevel(logging.DEBUG)
        L.debug("Running in debug mode")


@cli.group()
@click.pass_context
def standalone_components(ctx):
    """Interact with individual components"""
    pass


@standalone_components.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def environment(ctx, args):
    """Info about the local environment"""

    data = {
        "--project_root": ctx.obj["PROJECT_ROOT"],
        "--skip_version": ctx.obj['SKIP_VERSION']
    }
    cmd = get_commandline("./SentinelEnvironment/SentinelEnvironment.py", args, data)
    _run_cmd(cmd)


@standalone_components.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def ue4(ctx, args):
    """Interact with UE4"""

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}

    cmd = get_commandline("./SentinelUE4/SentinelUE4.py ", args, data)
    _run_cmd(cmd)


@standalone_components.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def vcs(ctx, args):

    """Interact with the Version Control System"""
    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}
    cmd = get_commandline("./SentinelVCS/SentinelVCS.py", args, data)
    _run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def commands(ctx, args):

    """ Utility commands"""

    data = {"--root": ctx.obj["PROJECT_ROOT"]}
    cmd = get_commandline("./commands.py", args, data)
    _run_cmd(cmd)


@standalone_components.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def database(ctx, args):

    """Interact with the Database"""

    data = {}

    cmd = get_commandline("./SentinelDB/SentinelDB.py", args, data)
    _run_cmd(cmd)


@standalone_components.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def aws(ctx, args):

    """ Interact with Amazon Web Services """

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}

    cmd = get_commandline("./SentinelAWS/SentinelAWS.py", args, data, arguments_at_end=False)
    _run_cmd(cmd)


if __name__ == "__main__":
    cli()
