import subprocess
from argparse import ArgumentParser
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

parser = ArgumentParser()
parser.add_argument('--debug', '-D', action='store_true',
                    help='Run in debug mode')
parser.add_argument('--port', '-P', default=7000,
                    type=int, help='The port to run on')

args = parser.parse_args()

app = Flask('sentinel')
api = Api(app)
CORS(app)

commands = ['start', 'restart', 'kill', 'list']

ue4Component = [
    'python', './SentinelUE4Component/SentinelUE4Component.py']

sentinelConfig = [
    'python', './SentinelConfig/SentinelConfig.py']


def error(err):
    return {'error': err}


@api.resource('/command/<string:command>')
class RunCommand(Resource):
    def get(self, command):
        try:
            output = subprocess.check_output(
                ue4Component + [command]).decode("utf-8")

            return {'output': output}
        except:
            # TODO log/display exception
            return error('Unexpected error')

    def post(self, command):

        # if command not in commands:
        #     return error(f'Invalid command: "{command}"')

        print('Should run sentinel command:', command)

        commandSplit = command.split(' ')

        print(ue4Component + commandSplit)

        try:
            output = subprocess.check_output(
                ue4Component + commandSplit).decode("utf-8")

            return {'output': output}
        except:
            # TODO log/display exception
            return error('Unexpected error')


@api.resource('/command')
class Command(Resource):
    def get(self):
        try:
            output = subprocess.check_output(
                sentinelConfig + ['-h']).decode("utf-8")

            return {'output': output}
        except:
            # TODO log/display exception
            return error('Unexpected error')


if __name__ == '__main__':
    app.run(debug=args.debug, port=args.port)
