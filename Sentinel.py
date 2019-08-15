import click
import utilities
import logging
from SentinelInternalLogger.logger import L


@click.group()
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', type=click.Choice(['true', 'false']), default='false', help="Skips output version")
@click.option('--debug', type=click.Choice(['true', 'false']), default='false',  help="Verbose logging")
@click.pass_context
def cli(ctx, project_root, output, debug, no_version):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    if debug == 'true':
        L.setLevel(logging.DEBUG)

    ctx = utilities.convert_parameters_to_ctx(ctx, project_root=project_root, output=output,
                                              debug=debug, no_version=no_version)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def api(ctx, args):
    """Queries for the web server to interact with"""
    data = utilities.convert_input_to_dict(ctx)

    cmd = utilities.get_commandline("./api.py", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def commands(ctx, args):
    """Commands"""

    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline(script_name="./commands.py", script_commands=args, global_arguments=data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def standalone_components(ctx, args):
    """Interact with individual components"""
    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline(script_name="./standalone.py", script_commands=args, global_arguments=data)
    utilities.run_cmd(cmd)


@cli.command()
@click.pass_context
def setup_default_environment(ctx):
    """Create default config"""

    global_args = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline("./Sentinel.py", ["standalone-components", "environment", "make-default-config"], global_args)
    utilities.run_cmd(cmd)


if __name__ == "__main__":
    cli()
