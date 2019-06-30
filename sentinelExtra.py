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
@click.option('--project_name', default="", help="Name of the project")
@click.option('--engine_path', default="", help="Relative Path to the engine")
@click.option('--config_path', default="", help="Path to a custom config folder")
@click.option('--version_control_root', default="", help="Path to the version control root")
@click.option('--artifacts_root', default="", help="Path to the artifacts root")
@click.option('--cache_path', default="", help="Path to the sentinel cache")
@click.pass_context
def process_missing(ctx,
                    project_name,
                    engine_path,
                    config_path,
                    version_control_root,
                    artifacts_root,
                    cache_path):
    """Goes through the history and runs validation"""

    default_config_cmd = "python sentinel.py environment make-default-config"

    arguments = ["project_name=" + project_name,
                 "engine_path=" + engine_path,
                 "config_path=" + config_path,
                 "version_control_root=" + version_control_root,
                 "artifacts_root=" + artifacts_root,
                 "cache_path="+cache_path]

    default_config_cmd = default_config_cmd + " --" + " --".join(arguments)

    # Generate the first default config
    subprocess.run(default_config_cmd)
    subprocess.run("python sentinel.py environment generate")

    # Reading the config to initialize the vcs walker
    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    walker = GitComponent.GitRepoWalker(environment_config)

    # Generate the first default config

    for i, each_commit in enumerate(walker.commits):
        walker.clean_checkout_commit(each_commit)

        subprocess.run(default_config_cmd)
        subprocess.run("python sentinel.py environment generate")

        subprocess.run("python sentinel.py vcs refresh")

        subprocess.run("python sentinel.py environment generate")

        subprocess.run("python sentinel.py ue4 build editor")

        subprocess.run("python sentinel.py ue4 project refresh-asset-info")

        subprocess.run("python sentinel.py vcs write-history-file --commit_id=" + walker.commit_ids[i])


if __name__ == "__main__":
    cli()
