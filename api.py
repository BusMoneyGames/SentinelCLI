import click
import utilities
import json

L = utilities.logger


@click.group()
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', type=click.Choice(['true', 'false']), default='true', help="Skips output version")
@click.option('--debug', type=click.Choice(['true', 'false']), default='false', help="Verbose logging")
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


@cli.command()
@click.pass_context
def get_all_asset_info(ctx):

    """Create a playable version of the project"""
    data = utilities.convert_input_to_dict(ctx)
    args = ["database", "list-entries"]
    sub_command_args = ["--help"]

    cmd = utilities.get_commandline(script_name="./standalone.py", script_commands=args, global_arguments=data, sub_command_arguments=sub_command_args)

    utilities.run_cmd(cmd)

    dummy_data = {"categories": ["Blueprints",
                                 "StaticMesh",
                                 "Texture2D"],
                  "items": [{"name": "viking_blueprint",
                             "category": "Blueprints"}]
                  }

    print(json.dumps(dummy_data, indent=4))


if __name__ == "__main__":
    cli()
