import click
import utilities
import logging
import os

import commands


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
def run_action(ctx, args):
    """actions and commands"""

    if not args:
        args = "--help"

    data = utilities.convert_input_to_dict(ctx)
    cmd = utilities.get_commandline(script_name="./commands.py", script_commands=args, global_arguments=data)

    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def run_module(ctx, args):
    """modules in isolation"""
    data = utilities.convert_input_to_dict(ctx)

    if not args:
        args = "--help"

    cmd = utilities.get_commandline(script_name="./standalone.py", script_commands=args, global_arguments=data)
    utilities.run_cmd(cmd)


@cli.command()
@click.option('--project_root', default="", help="Relative path to project root")
@click.option('--engine_root', default="", help="Relative path to the engine")
@click.option('--config_root', default="", help="Path to the config file")
@click.option('--artifact_name', default="", help="Artifact Name")
@click.pass_context
def setup(ctx, project_root, engine_root, config_root, artifact_name):
    """first time environment"""

    input_arguments = [
        "--project_name="+project_root,
        "--engine_path="+engine_root,
        "--artifact_name="+artifact_name,
        "--config_path="+config_root
    ]

    global_args = utilities.convert_input_to_dict(ctx)
    generate_default_config_cmd = utilities.get_commandline("./Sentinel.py", ["run-module", "environment", "make-default-config"], global_args,input_arguments)
    utilities.run_cmd(generate_default_config_cmd)

    commands.refresh_config(ctx)



@cli.command()
@click.pass_context
def start_backend(ctx):
    """start the backend server"""
    import subprocess
    subprocess.call("python server.py")


if __name__ == "__main__":
    cli()
