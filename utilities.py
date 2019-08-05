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


def get_commandline(script_name,
                    script_commands,
                    global_arguments=None,
                    sub_command_arguments=None,
                    arguments_at_end=False):
    """
    Constructs the command line that gets passed into the different sentinel commands
    :return:
    """

    cmd = "python " + script_name

    # Constructing the global arguments
    if global_arguments:
        # Creates the arguments that are passed in from the root command (sentinel.py)
        pass_through_arguments = " "
        for each_data in global_arguments.keys():
            pass_through_arguments = pass_through_arguments + each_data + "=" + global_arguments[each_data] + " "
    else:
        pass_through_arguments = ""

    # Constructing the sub command arguments
    arguments = ""
    if sub_command_arguments:
        # Creates the arguments that are local to the command in the component that is being called
        arguments = " ".join(sub_command_arguments)
    sub_command_arguments = arguments

    cmd = cmd + pass_through_arguments + " ".join(script_commands)

    # Flips the arguments to go at the end
    # TODO understand why this is needed
    if arguments_at_end:
        cmd = cmd + " " + sub_command_arguments
    else:
        cmd = cmd + " " + sub_command_arguments

    L.debug(cmd)
    return cmd


def run_cmd(cmd):
    return_object = subprocess.run(cmd, shell=True)

    if not return_object.returncode == 0:
        quit(1)


def convert_parameters_to_ctx(ctx, project_root, no_version, output, debug):

    if not project_root:
        run_directory = pathlib.Path(os.getcwd())
        project_root = run_directory.parent.as_posix()

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root
    ctx.obj['SKIP_VERSION'] = str(no_version).lower()
    ctx.obj['OUTPUT'] = str(output).lower()
    ctx.obj['DEBUG'] = str(debug).lower()

    return ctx


def convert_input_to_dict(ctx):
    data = {
        "--project_root": ctx.obj["PROJECT_ROOT"],
        "--no_version": ctx.obj['SKIP_VERSION'],
        "--output": ctx.obj['OUTPUT'],
        "--debug": ctx.obj['DEBUG']
    }
    return data


def convert_input_to_string(ctx):

    dict_input = convert_input_to_dict(ctx)
    out = ""
    for each_key in dict_input.keys():
        out = out + each_key + "=" + dict_input[each_key] + " "

    return out
