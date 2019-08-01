import click
import utilities

L = utilities.logger


@click.group()
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', type=click.Choice(['True', 'False']), default='true', help="Skips output version")
@click.option('--debug', type=click.Choice(['True', 'False']), default='false',  help="Verbose logging")
@click.pass_context
def cli(ctx, project_root, output, debug, no_version):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx = utilities.convert_parameters_to_ctx(ctx, project_root, output, debug, no_version)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def environment(ctx, args):
    """Info about the local environment"""

    data = {
        "--project_root": ctx.obj["PROJECT_ROOT"],
        "--skip_version": ctx.obj['SKIP_VERSION']
    }
    cmd = utilities.get_commandline("./SentinelEnvironment/SentinelEnvironment.py", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def ue4(ctx, args):
    """Interact with UE4"""

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}

    cmd = utilities.get_commandline("./SentinelUE4/SentinelUE4.py ", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def vcs(ctx, args):

    """Interact with the Version Control System"""
    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}
    cmd = utilities.get_commandline("./SentinelVCS/SentinelVCS.py", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def commands(ctx, args):

    """ Utility commands"""

    data = {"--root": ctx.obj["PROJECT_ROOT"]}
    cmd = utilities.get_commandline("./commands.py", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def database(ctx, args):

    """Interact with the Database"""

    data = {}

    cmd = utilities.get_commandline("./SentinelDB/SentinelDB.py", args, data)
    utilities.run_cmd(cmd)


@cli.command(context_settings=dict(ignore_unknown_options=True, help_option_names=['-_h', '--_help']), )
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def aws(ctx, args):

    """ Interact with Amazon Web Services """

    data = {"--project_root": ctx.obj["PROJECT_ROOT"]}

    cmd = utilities.get_commandline("./SentinelAWS/SentinelAWS.py", args, data, arguments_at_end=False)
    utilities.run_cmd(cmd)

if __name__ == "__main__":
    cli()
