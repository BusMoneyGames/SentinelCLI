import subprocess
import json
from argparse import ArgumentParser
from flask import Flask, request
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

sentinelPy = ['python', 'Sentinel.py']

ue4Component = [
    'python', './SentinelUE4Component/SentinelUE4Component.py']

sentinelConfig = [
    'python', './SentinelConfig/SentinelConfig.py']

configFileBasePath = './SentinelConfig/defaultConfig'
configFileTypes = {
    'build': 'buildconfigs'
}


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
        except Exception as e:
            # TODO log/display exception
            print(e)
            return error('Unexpected error')


@api.resource('/command')
class Command(Resource):
    def get(self):
        try:
            output = subprocess.check_output(
                sentinelConfig + ['-h']).decode("utf-8")

            return {'output': output}
        except Exception as e:
            # TODO log/display exception
            print(e)
            return error('Unexpected error')


@api.resource('/config/<string:config>')
class Config(Resource):
    def get(self, config):
        configType = request.args['type']

        if configType not in configFileTypes:
            return error('Invalid config file type')

        try:
            with open(f'{configFileBasePath}/{configFileTypes[configType]}/{config}.json') as configFile:
                data = json.load(configFile)

                return {'output': data}
        except Exception as e:
            # TODO log/display exception
            print(e)
            return error('Unexpected error')

    def put(self, config):
        configType = request.args['type']

        if configType not in configFileTypes:
            return error('Invalid config file type')

        body = request.get_json()

        if body is None:
            return error('Failed to parse JSON body')

        try:
            with open(f'{configFileBasePath}/{configFileTypes[configType]}/{config}.json', 'r+') as configFile:
                data = json.load(configFile)

                data.update(body)

                configFile.seek(0)
                configFile.write(json.dumps(data, indent=2))
                configFile.truncate()

                return {'success': True}
        except Exception as e:
            # TODO log/display exception
            print(e)
            return error('Unexpected error')


@api.resource('/sentinel')
class RunSentinel(Resource):
    def post(self):
        try:
            body = request.get_json()

            command = body["command"]

            cmd = sentinelPy + command.split(" ")
            output = subprocess.check_output(cmd).decode("utf-8")

            json_output = json.loads(output)
            return json_output

        except Exception as e:
            print(e)
            # TODO log/display exception
            return error('Unexpected error')


if __name__ == '__main__':
    app.run(debug=args.debug, port=args.port)
