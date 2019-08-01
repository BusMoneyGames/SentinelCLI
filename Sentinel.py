import click
import logging

from logging.config import fileConfig

import utilities
L = utilities.logger


@click.group()
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', is_flag=True, default=True, help="Skips output version")
@click.option('--debug', is_flag=True, default=False, help="Verbose logging")
@click.pass_context
def cli(ctx, project_root, output, debug, no_version):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx = utilities.convert_parameters_to_ctx(ctx, debug, no_version, output, project_root)

    if debug:
        L.setLevel(logging.DEBUG)
        L.debug("Running in debug mode")


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def api(ctx, args):
    """Queries for the web server to interact with"""
    data = utilities.convert_input_to_dict(ctx)

    cmd = utilities.get_commandline("./api.py", args, data)
    L.debug(cmd)

    utilities.run_cmd(cmd)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def commands(ctx, args):
    """Commands"""

    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./commands.py", args, data)
    L.debug(cmd)

    utilities.run_cmd(cmd)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def standalone_components(ctx, args):
    """Interact with individual components"""
    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./standalone.py", args, data)
    L.debug(cmd)

    utilities.run_cmd(cmd)


if __name__ == "__main__":
    cli()
