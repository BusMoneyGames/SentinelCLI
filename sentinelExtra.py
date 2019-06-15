import logging
import click
import json
import pathlib
import SentinelVCSComponent.Vcs.GitComponent as GitComponent
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
@click.option('--project_root', default="", help="path to the config overwrite folder")
@click.option('--debug', default=False, help="Turns on debug messages")
@click.pass_context
def cli(ctx, project_root, debug):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root

    if debug:
        L.setLevel(logging.DEBUG)
        message_format = '%(levelname)s - %(message)s '
    else:
        message_format = '%(levelname)s %(message)s '
        L.setLevel(logging.ERROR)

    logging.basicConfig(format=message_format)


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def process_missing(ctx, output):
    """Goes through the history and runs validation"""
    project_root = pathlib.Path(ctx.obj['PROJECT_ROOT'])
    write_default_config(project_root)

    subprocess.run("python sentinel.py environment generate")

    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    walker = GitComponent.GitRepoWalker(environment_config)

    for each_commit in walker.commits:
        walker.clean_checkout_commit(each_commit)
        write_default_config(project_root)

        subprocess.run("python sentinel.py environment generate")

        subprocess.run("python sentinel.py vcs refresh")

        subprocess.run("python sentinel.py environment generate")

        subprocess.run("python sentinel.py ue4 build editor")

        subprocess.run("python sentinel.py ue4 project refresh-asset-info")

        print(each_commit)


def write_default_config(project_root):

    generated_config = pathlib.Path(project_root).joinpath("_sentinel_root.json")

    config = {"project_root_path": "SentinelUE4",
              "engine_root_path": "UnrealEngine",
              "sentinel_config_root_path": "SentinelConfig",
              "version_control_root": "",
              "sentinel_artifacts_path": "../SentinelArtifacts",
              "sentinel_cache_path": "_SentinelCache"}

    f = open(generated_config, "w")
    f.write(json.dumps(config, indent=4))
    f.close()


if __name__ == "__main__":
    cli()
