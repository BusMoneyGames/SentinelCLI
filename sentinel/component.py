import asyncio
import json
import os
from multiprocessing import Process

import sentinel.entity as entity
from sentinel.routing import Streamer


class Component(Process):
    throttle = 5

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.streamer = None
        self.host = '10.114.0.206'
        self.port = 8888
        self.message_handler = None
        self.input_queue_name = None
        self.output_queue_name = None
        self.throttle = Component.throttle

    def run(self):
        loop = asyncio.get_event_loop()
        loop.call_later(0.2, self.periodic)

        try:
            loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            pass

        loop.close()

    def periodic(self):
        loop = asyncio.get_event_loop()
        loop.call_later(0.2, self.periodic)

    async def connect_to_server(self):
        loop = asyncio.get_event_loop()
        reader, writer = await asyncio.open_connection(self.host, self.port,
                                                       loop=loop)
        self.streamer = Streamer(reader, writer)
        print(f'{self.name} connected to server')

    async def disconnect_from_server(self):
        await self.streamer.close()
        print(f'{self.name} disconnected from server')

    async def connect(self):
        """
        Connects to the server and processes all incoming messages.
        This is actually a driver that asks the assigned message handler
        to do the actual processing. The driver just unwraps and wraps the
        result in a transport message.
        Note that for each incoming message the handler can produce one or
        more outgoing messages.
        """
        await self.connect_to_server()
        await self._connect_input_queue()

        self._full_throttle()
        while True:
            request = {'cmd': 'receive', 'queue': self.input_queue_name}
            await self.streamer.send(request)
            request_reply = await self.streamer.receive()
            cmd = request_reply['cmd']
            if cmd == 'message':
                msg = json.loads(request_reply['payload'])
                await self._handle_message(msg)
                self._full_throttle()
            elif cmd == 'status':
                self._handle_status(request_reply)
            elif cmd == 'shutdown':
                # TODO: Implement component shutdown
                pass

            await self._throttle_down()

    async def _connect_input_queue(self):
        request = {
            'cmd': 'connect',
            'name': self.name,
            'queue': self.input_queue_name
        }
        await self.streamer.send(request)
        request_reply = await self.streamer.receive()
        cmd = request_reply['cmd']
        if cmd == 'status':
            self._handle_status(request_reply)

    async def _handle_message(self, msg: dict):
        self.message_handler.setup(msg)
        while True:
            result = self.message_handler.run()
            if not result:
                break
            result_reply = {
                'cmd': 'send',
                'msg_type': result['msg_type'],  # broadcast or regular
                'queue': self.output_queue_name,
                'payload': json.dumps(result)
            }
            await self.streamer.send(result_reply)
            await self.streamer.receive()  # TODO: Handle the reply

    def _handle_status(self, request_reply: dict):
        if request_reply['status'] == 'error':
            print(f'Error: {request_reply["reason"]}')

    def _full_throttle(self):
        self.throttle = Component.throttle

    async def _throttle_down(self):
        self.throttle -= 1
        if self.throttle <= 0:
            await asyncio.sleep(1)
            self.throttle = 0


class Builder(Component):
    """
    Builds the component queue specified in component_configs and starts it.
    Assumes a queue server is already running.
    """
    def __init__(self, component_configs: dict):
        super().__init__('builder')
        self._component_configs = component_configs
        self._components = {}

    def run(self):
        for name in self._component_configs:
            cfg = self._component_configs[name]
            # handler = getattr(component, cfg.class_name)
            handler = globals()[cfg['class_name']]
            count = cfg['instance_count']
            for i in range(count):
                comp_name = f'{name}-{i}'
                comp = Component(comp_name)
                comp.message_handler = handler(comp_name, cfg['config'])
                comp.input_queue_name = cfg['input_queue']
                comp.output_queue_name = cfg['output_queue']
                comp.start()
                self._components[comp_name] = comp

    def send(self, queue_name: str, msg: dict):
        """
        Inserts the message msg into the queue named queue_name.

        :str queue_name: The queue to insert into.
        :dict msg: The message to be inserted.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_send(queue_name, 'regular', msg))

    def broadcast(self, queue_name: str, msg: dict):
        """
        Broadcasts the message msg to the queue named queue_name.
        This means all the workers fetching from the queue will receive
        the message.

        :str queue_name: The queue to broadcast to.
        :dict msg: The message to be broadcast.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_send(queue_name, 'broadcast', msg))

    async def async_send(self, queue_name: str, msg_type: str, msg: dict):
        await self.connect_to_server()

        request = {
            'cmd': 'send',
            'msg_type': msg_type,
            'queue': queue_name,
            'payload': json.dumps(msg)
        }
        await self.streamer.send(request)
        await self.streamer.receive()  # TODO: Handle reply

        await self.disconnect_from_server()

    def join_all(self):
        for component in self._components:
            component.join()


class MessageHandler:
    def __init__(self, name: str, config: dict):
        self.name = name
        self._config = config  # TODO: Pick common config from the dict
        self._eos_names = set()

    def _check_eos(self, msg: dict) -> bool:
        """
        If configured to sync EOSs' checks if all EOS have been received.

        :dict msg: The supposed end of stream message.
        :return: True if all EOSs' have been received, False otherwise.
        """
        if not msg:
            return False
        if 'sync_eos' not in self._config:
            return False
        if not self._config['sync_eos']:
            return False
        if 'sync_eos_count' not in self._config:
            return False

        self._eos_names.add(msg['from'])

        return len(self._eos_names) == self._config['sync_eos_count']

    def _is_eos(self, msg: dict) -> bool:
        if msg:
            return 'end_of_stream' in msg

    def _label_as_broadcast(self, msg: dict):
        # TODO: prefix these special message keys
        msg['msg_type'] = 'broadcast'
        msg['from'] = self.name


# Worker components

class Printer(MessageHandler):
    """
    Prints all received messages on stdout.
    Forwards end of stream messages.
    Only used for testing.
    """
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self._msg = None

    def setup(self, msg: dict):
        self._msg = msg
        print(f'{self.name} received {msg}')

    def run(self):
        if self._check_eos(self._msg):
            print(f'{self.name} received all end of stream messages')
        elif self._is_eos(self._msg):
            # Forward the EOS as a broadcast
            eos = self._msg
            self._label_as_broadcast(eos)
            self._msg = None
            return eos

        return None


class DirectoryLister(MessageHandler):
    """
    Recursively reads all files with the given extension from the directory
    specified in the input message and sends each filename in a separate
    message to the output queue.
    """
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self._filenames: iter = None  # The directory filename iterator

    def setup(self, msg: dict):
        extension = msg['extension']
        path = os.path.join(os.path.normpath(msg['directory']))

        f = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ext == extension:
                    f.append(os.path.join(root, filename))
        self._filenames = iter(f)

    def run(self):
        try:
            return {'msg_type': 'regular', 'filename': next(self._filenames)}
        except StopIteration:
            return None


class AssetCreator(MessageHandler):
    """
    Creates an asset for the passed in asset if the asset does not exist.
    Outputs the asset id.
    """
    pass


class AssetChangeDetector(MessageHandler):
    """
    Forwards only those assets that have changed.
    """
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.filename: str = None

    def setup(self, msg: dict):
        self.filename = msg['filename']

    def run(self):
        asset = entity.Asset()
        asset.filename = self.filename
        asset.load_by_filename()

        last_hash = asset.get_hash()
        asset.generate_and_save_hash()
        current_hash = asset.get_hash()

        result = None
        if last_hash != current_hash:
            result = {'msg_type': 'regular', 'filename': self.filename}

        return result


class Grouper(MessageHandler):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.group_size = config['group_size']
        self.max_stream_end_count: int = config['stream_end_count']
        self.stream_end_count: int = 0
        self.group: list = []

    def setup(self, msg: dict):
        if 'stream_end' in msg:
            self.stream_end_count += 1
        else:
            self.group.append(msg)

    def run(self):
        result = None
        if (self.stream_end_count == self.max_stream_end_count
                or len(self.group) == self.group_size):
            result = {'msg_type': 'regular', 'group': self.group}
            self.stream_end_count = 0
            self.group = []
        return result


class UEMetadataExtractor(MessageHandler):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)

    def setup(self, msg: dict):
        pass

    def run(self):
        result = None
        return result

