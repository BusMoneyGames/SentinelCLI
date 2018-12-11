# coding=utf-8
import cx_Freeze
import os
import pathlib

home = str(pathlib.Path.home())

script_file = pathlib.PurePath(os.path.realpath(__file__))
bin_scripts = script_file.parent.joinpath("bin")

build_folder = script_file.parent.joinpath("SentinelTool")

base = None

os.environ['TCL_LIBRARY'] = os.path.normpath(home + '/AppData/Local/Programs/Python/Python36/tcl/tcl8.6')
os.environ['TK_LIBRARY'] = os.path.normpath(home + '/AppData/Local/Programs/Python/Python36/tcl/tk8.6')

executables = [
               cx_Freeze.Executable("SentinelUnrealTool.py", base=None),
               cx_Freeze.Executable("SentinelReportsTool.py", base=None),
               cx_Freeze.Executable("SentinelUpload.py", base=None),
               cx_Freeze.Executable("SentinelMessaging.py", base=None),
               cx_Freeze.Executable("SentinelClientTestTool.py", base=None)]

includes = ["ConfigParser",
            "html.parser",
            "boto3.s3.inject",
            "asyncio",
            "pkg_resources._vendor",
            "requests",
            "idna"
            ]

buildOptions = dict(packages=includes,
                    include_files=[bin_scripts],
                    build_exe=build_folder
                    )

cx_Freeze.setup(
    name="Sentinel",
    options=dict(build_exe=buildOptions),
    version="0.01",
    descriptions="Trying to get this to work",
    executables=executables
)
