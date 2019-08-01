
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
    """Sentinel Commands"""
    ctx = utilities.convert_parameters_to_ctx(ctx, project_root=project_root, output=output,
                                              debug=debug, no_version=no_version)

@cli.command()
@click.pass_context
def get_list_of_builds(ctx):
    L.debug("Getting list of builds ")
    """Create a playable version of the project"""
    return {"builds": ["label", "something"]}


if __name__ == "__main__":
    cli()
