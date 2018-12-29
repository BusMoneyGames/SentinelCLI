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
        self.output_queue_names = {}
        self.throttle = Component.throttle

    def run(self):
        loop = asyncio.get_event_loop()
        loop.call_later(0.2, self.periodic)

        try:
            loop.run_until_complete(self.connect())
        except (KeyboardInterrupt, ConnectionResetError):
            # This is a bit brute force way to shut down, but has to do for now.
            pass

        loop.close()

    def periodic(self):
        loop = asyncio.get_event_loop()
        loop.call_later(0.2, self.periodic)

    async def connect_to_server(self):
        loop = asyncio.get_event_loop()
        reader, writer = await asyncio.open_connection(self.host, self.port,
                                                       loop=loop)
        self.streamer = Streamer(self.name, reader, writer)
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
            local_queue_name, result = self.message_handler.run()
            if not result:
                break
            # if local_queue_name and not result:
            #     continue
            # if not (local_queue_name and result):
            #     break
            result_reply = {
                'cmd': 'send',
                'msg_type': result['msg_type'],  # broadcast or regular
                'queue': self.output_queue_names[local_queue_name],
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
            await asyncio.sleep(0.2)
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

    async def run(self):
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
                outputs = cfg['output_queues']
                for local_name, queue_name in outputs.items():
                    comp.output_queue_names[local_name] = queue_name
                comp.start()
                self._components[comp_name] = comp

    def send(self, queue_name: str, msg: dict):
        """
        Inserts the message msg into the queue named queue_name.

        :str queue_name: The queue to insert into.
        :dict msg: The message to be inserted.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_send(queue_name, 'regular', msg))

    def wait_for_message(self, queue_name: str, msg: dict):
        """
        Waits for a message like msg to arrive on the queue name queue_name.

        :str queue_name: The queue to wait on.
        :dict msg: The message to wait for.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_wait_for(queue_name, msg))

    def broadcast(self, queue_name: str, msg: dict):
        """
        Broadcasts the message msg to the queue named queue_name.
        This means all the workers fetching from the queue will receive
        the message.

        :str queue_name: The queue to broadcast to.
        :dict msg: The message to be broadcast.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_send(queue_name, 'broadcast', msg))

    def join_all(self):
        for component in self._components:
            component.join()

    async def _async_send(self, queue_name: str, msg_type: str, msg: dict):
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

    async def _async_wait_for(self, queue_name: str, msg: dict):
        await self.connect_to_server()

        while True:
            request = {'cmd': 'receive', 'queue': queue_name}
            await self.streamer.send(request)
            reply = await self.streamer.receive()
            cmd = reply['cmd']
            if cmd == 'message':
                payload = reply['payload']
                if payload:
                    recv_msg = json.loads(reply['payload'])
                    if recv_msg == msg:
                        break
            await asyncio.sleep(0.5)

        await self.disconnect_from_server()


class MessageHandler:
    def __init__(self, name: str, config: dict):
        self.name = name
        self._msg = None  # The current message being processes
        self._eos_names = set()
        self._eos_done = False
        self._sync_eos = False
        if 'sync_eos' in config:
            self._sync_eos = config['sync_eos']
        self._sync_eos_count = None
        if 'sync_eos_count' in config:
            self._sync_eos_count = config['sync_eos_count']

    def setup(self, msg: dict):
        self._msg = msg
        self._eos_done = False

    def run(self):
        all_eos_received = False
        if not self._msg:
            return 'default', None
        elif self._eos_received():
            if self._check_eos_count():
                # Sync EOS case (sync_eos = True)
                # All end of stream (EOS) messages received
                if self._sync_eos and not self._eos_done:
                    # The handler still has some processing to do
                    all_eos_received = True
                elif self._eos_done:
                    # Clear the message and forward the EOS as a broadcast
                    eos = self._reset_and_create_broadcast()
                    return 'default', eos
            else:
                # Non-sync EOS case (sync_eos = False or absent)
                # Clear the message and forward the EOS as a broadcast
                eos = self._reset_and_create_broadcast()
                return 'default', eos

        return self.process_message(all_eos_received)

    def process_message(self, all_eos_received):
        raise NotImplementedError("You need to override this method")

    def _check_eos_count(self) -> bool:
        """
        If configured to sync EOSs' checks if all EOS have been received.
        For example, there might be two components before this one in the
        pipeline and we have to wait for each of them to send us their EOS.

        :dict msg: The supposed end of stream message.
        :return: True if all EOSs' have been received, False otherwise.
        """
        if not self._msg:
            return False
        if not self._sync_eos:
            return False
        if not self._sync_eos_count:
            return False

        self._eos_names.add(self._msg['from'])

        return len(self._eos_names) == self._sync_eos_count

    def _eos_received(self) -> bool:
        if self._msg:
            return 'end_of_stream' in self._msg

    def _label_message_as_broadcast(self, msg: dict):
        # TODO: prefix these special message keys
        msg['msg_type'] = 'broadcast'
        msg['from'] = self.name

    def _reset_and_create_broadcast(self):
        eos = self._msg
        self._label_message_as_broadcast(eos)
        self._msg = None
        return eos


# Worker components

class Printer(MessageHandler):
    """
    Prints all received messages on stdout.
    Forwards end of stream messages.
    Only used for testing.
    """
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self._eos_done_count = 0

    def setup(self, msg: dict):
        super().setup(msg)
        print(f'{self.name} received {msg}')

    def run(self):
        if self._check_eos_count():
            # All end of stream (EOS) messages received
            self._eos_done = True
            self._eos_done_count += 1
            result = None
            if self._eos_done_count == 1:
                print(f'{self.name} received all end of stream messages')
                result = {'msg_type': 'regular', 'done': True}
            return 'default', result
        elif self._eos_received():
            # Clear message and forward the EOS as a broadcast
            print(f'{self.name} received an end of stream message')
            eos = self._reset_and_create_broadcast()
            return 'default', eos

        return 'default', None

    def process_message(self, all_eos_received):
        # No need for this here because run is overridden
        pass


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
        super().setup(msg)

        extension = msg['extension']
        path = os.path.join(os.path.normpath(msg['directory']))

        f = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ext == extension:
                    f.append(os.path.join(root, filename))
        self._filenames = iter(f)

    def process_message(self, all_eos_received):
        # TODO: Send EOS when done
        try:
            return 'default', {'msg_type': 'regular',
                               'filename': next(self._filenames)}
        except StopIteration:
            return 'default', None


class AssetCreator(MessageHandler):
    """
    Creates an asset for the passed in asset filename if the asset does not
    exist.
    Outputs the asset id.
    """
    def process_message(self, all_eos_received):
        asset = entity.Asset()
        asset.filename = self._msg['filename']
        asset.processing_state_id = entity.ProcessingState.PENDING
        asset.save()

        return 'default', {'msg_type': 'regular', 'asset_id': asset.id}


class AssetChangeDetector(MessageHandler):
    """
    Forwards only those assets that have changed.
    """
    def process_message(self, all_eos_received):
        asset = entity.Asset()
        asset.id = self._msg['asset_id']
        asset.load()

        last_hash = asset.get_hash()
        asset.generate_and_save_hash()
        current_hash = asset.get_hash()

        result = None
        if last_hash != current_hash:
            result = {'msg_type': 'regular', 'asset_id': asset.id}

        return 'default', result


class AssetTypeChecker(MessageHandler):
    """
    Checks if an asset has a type or not.
    Forwards an asset with a type to the with_type queue.
    Forwards an asset with no type to the without_type queue.
    """
    def process_message(self, all_eos_received):
        asset = entity.Asset()
        asset.id = self._msg['asset_id']
        asset.load()

        queue = 'without_type'
        result = result = {'msg_type': 'regular', 'asset_id': asset.id}
        if asset.type_id:
            queue = 'with_type'

        return queue, result


class AssetGrouper(MessageHandler):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.group_size = config['group_size']
        self.group_by = None
        if 'group_by' in config:
            self.group_by = config['group_by']
        self.groups: dict = {}

    # def setup(self, msg: dict):
    #     if 'stream_end' in msg:
    #         self.stream_end_count += 1
    #     else:
    #         self.group.append(msg)

    def process_message(self, all_eos_received):
        result = None

        group = []
        group_name = 'default'

        if all_eos_received:
            if len(self.groups) > 0:
                group_name, group = self.groups.popitem()
            self._eos_done = len(self.groups) == 0
        else:
            asset = entity.Asset()
            asset.id = self._msg['asset_id']
            asset.load()

            if self.group_by:
                group_name = getattr(asset, self.group_by)

            if group_name not in self.groups:
                self.groups[group_name] = []
            self.groups[group_name].append(self._msg)

            if len(self.groups[group_name]) == self.group_size:
                group = self.groups[group_name]
                del self.groups[group_name]

        if len(group) > 0:
            result = {
                'msg_type': 'regular',
                'group_name': group_name,
                'group': group}

        return 'default', result


class UEMetadataExtractor(MessageHandler):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)

