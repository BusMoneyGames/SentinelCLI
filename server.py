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


def error(err):
    return {'error': err}


@api.resource('/command/<string:command>')
class RunCommand(Resource):
    def post(self, command):

        if command not in commands:
            return error(f'Invalid command: "{command}"')

        print('Should run sentinel command:', command)

        try:
            # output = subprocess.check_output(['python', 'modo.py', 'rexec', command]).decode("utf-8")

            output = f'Some text that should be returned\nWow this is some good text\nThis is good\nVery good\nYes\nThe command executed was: {command}'

            return {'output': output}
        except:
            # TODO log/display exception
            return error('Unexpected error')


@api.resource('/command')
class Command(Resource):
    def get(self):
        try:
            output = subprocess.check_output(
                ['python', './SentinelConfig/SentinelConfig.py', '-h']).decode("utf-8")

            return {'output': output}
        except:
            # TODO log/display exception
            return error('Unexpected error')


if __name__ == '__main__':
    app.run(debug=args.debug, port=args.port)
