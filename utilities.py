import json
import os
import pathlib
import subprocess
import logging

from logging.config import fileConfig
fileConfig('logging_config.ini')
logger = logging.getLogger()

L = logger


def read_config(path):
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

    return cmd


def run_cmd(cmd):
    return_object = subprocess.run(cmd, shell=True)

    if not return_object.returncode == 0:
        quit(1)


def convert_parameters_to_ctx(ctx, debug, no_version, output, project_root):

    if not project_root:
        run_directory = pathlib.Path(os.getcwd())
        project_root = run_directory.parent.as_posix()

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root
    ctx.obj['SKIP_VERSION'] = str(no_version)
    ctx.obj['OUTPUT'] = str(output)
    ctx.obj['DEBUG'] = str(debug)

    return ctx


def convert_input_to_dict(ctx):
    data = {
        "--project_root": ctx.obj["PROJECT_ROOT"],
        "--no_version": ctx.obj['SKIP_VERSION'],
        "--output": ctx.obj['OUTPUT'],
        "--debug": ctx.obj['DEBUG']
    }
    return data