import asyncio
import sys
import json
from multiprocessing import Process


class QueueNotFoundError(Exception):
    pass


class Streamer:

    version = b'\x01'
    version_size = 1
    length_size = 4

    def __init__(self, conn_id, reader, writer):
        self.conn_id = conn_id
        self.reader = reader
        self.writer = writer

    async def receive(self) -> dict:
        # Protocol version
        version = await self.reader.readexactly(Streamer.version_size)
        # print('streamer: version: {}'.format(version))

        # Message length
        length = await self.reader.readexactly(Streamer.length_size)
        length = int.from_bytes(length, byteorder='big')
        # print('streamer: receiving {} bytes'.format(length))

        # Message data
        data = await self.reader.readexactly(length)
        message = json.loads(data.decode())
        # print(f'streamer (conn_id = {self.conn_id}): received message {message}')

        return message

    async def send(self, message):
        data = json.dumps(message).encode()
        data_length = len(data)

        # Protocol version
        self.writer.write(self.version)

        # Message length
        length = data_length.to_bytes(Streamer.length_size, byteorder='big')
        self.writer.write(length)

        # Message data
        self.writer.write(data)

        await self.writer.drain()

    async def close(self):
        await self.writer.drain()
        self.writer.close()


class Connection:

    def __init__(self, conn_id: int, queue_server, reader, writer):
        self.id = conn_id
        # print(f'Connection with id {self.id}')
        self.server = queue_server
        self.streamer = Streamer(self.id, reader, writer)
        self.input_queue = asyncio.Queue()

    async def run(self):
        while True:
            try:
                message = await self.streamer.receive()
                await self._handle_message(message)
            except (ConnectionResetError, asyncio.IncompleteReadError):
                print('************ Connection Reset ************')
                self.server.remove_connection(self.id)
                break

    async def _handle_message(self, message: dict):
        cmd = message['cmd']
        if cmd == 'send':
            await self._handle_send(message)
        elif cmd == 'receive':
            await self._handle_receive(message)
        elif cmd == 'connect':
            await self._handle_connect(message)

    async def _handle_send(self, message: dict):
        reply = {'cmd': 'status'}
        try:
            self.server.push_on_queue(message)
            reply['status'] = 'ok'
        except asyncio.QueueFull:
            reply['status'] = 'error'
            reply['reason'] = 'Queue full'

        await self.streamer.send(reply)

    async def _handle_receive(self, message: dict):
        reply = {}
        try:
            msg = self._get_next_message(message['queue'])
            reply['cmd'] = 'message'
            reply['payload'] = msg
        except asyncio.QueueEmpty:
            reply['cmd'] = 'status'
            reply['status'] = 'notice'
            reply['reason'] = 'Queue empty'

        await self.streamer.send(reply)

    async def _handle_connect(self, message: dict):
        reply = {'cmd': 'status'}
        try:
            name = message['name']
            queue_name = message['queue']
            self.server.connect_to_queue(queue_name, self.id)
            reply['status'] = 'ok'
            print(f'{name} connected to queue "{queue_name}"')
        except QueueNotFoundError:
            reply['status'] = 'error'
            reply['reason'] = f'Queue {message["queue"]} not found'

        await self.streamer.send(reply)

    def _get_next_message(self, queue_name: str) -> str:
        # There might be a broadcast message waiting
        msg = self._pop_input_queue()
        if msg:
            return msg

        self.server.deliver_from_queue(self.id, queue_name)

        return self._pop_input_queue()

    def _pop_input_queue(self):
        try:
            msg = self.input_queue.get_nowait()
            self.input_queue.task_done()
            return msg
        except asyncio.QueueEmpty:
            return None


class QueueServer(Process):
    """
    A queue server.
    """

    def __init__(self, queue_config: list):
        super().__init__()

        self._queue_config = queue_config
        self._connection_count = 0
        self._connections = {}
        self._queue_connection_ids = {}
        self._queues = {}
        self.port = 8888

    async def on_new_connection(self, reader, writer):
        conn = self._create_connection(reader, writer)
        await conn.run()

    def remove_connection(self, conn_id: int):
        if conn_id in self._connections:
            # print(f'Removing connection {cid}')
            del self._connections[conn_id]
            # print(f'Active connections: {self._connections}')

    def run(self):
        self._create_queues(self._queue_config)

        loop = asyncio.get_event_loop()

        # The default event loop on Windows doesn't support subprocesses.
        # Use the Proactor event loop instead.
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)

        loop.call_later(0.2, self.periodic)
        coro = asyncio.start_server(self.on_new_connection,
                                    '0.0.0.0', self.port, loop=loop)
        server = loop.run_until_complete(coro)

        print(f'Serving on {server.sockets[0].getsockname()}')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('****** Keyboard interrupt *******')
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    def stop(self):
        self.terminate()

    def periodic(self):
        # print(self._queues['trigger'])
        loop = asyncio.get_event_loop()
        loop.call_later(10, self.periodic)

    def connect_to_queue(self, queue_name: str, conn_id: int):
        if queue_name not in self._queue_connection_ids:
            self._queue_connection_ids[queue_name] = set()
        self._queue_connection_ids[queue_name].add(conn_id)

    def push_on_queue(self, msg):
        queue = self._queues[msg['queue']]
        if queue:
            entry = {
                'msg_type': msg['msg_type'],
                'message': msg['payload']
            }
            queue.put_nowait(entry)
        else:
            raise QueueNotFoundError

    def deliver_from_queue(self, conn_id: int, queue_name: str):
        """
        The connection calls this when it needs to forward a message to
        the worker.
        """
        queue = self._queues[queue_name]
        if queue:
            entry = queue.get_nowait()
            queue.task_done()
            if entry['msg_type'] == 'broadcast':
                self._broadcast_message(queue_name, entry['message'])
            else:
                self._enqueue_on_connection(conn_id, entry['message'])
        else:
            raise QueueNotFoundError

    def _create_queues(self, queues: list):
        for queue in queues:
            self._queues[queue['name']] = asyncio.Queue()

    def _create_connection(self, reader, writer):
        self._connection_count += 1
        cid = self._connection_count
        conn = Connection(cid, self, reader, writer)
        self._connections[cid] = conn
        # print(f'Connections: {self._connections}')
        return conn

    def _broadcast_message(self, queue_name, msg):
        # Only broadcast to connected queues
        if queue_name in self._queue_connection_ids:
            for cid in self._queue_connection_ids[queue_name]:
                self._enqueue_on_connection(cid, msg)
        else:
            print(f'Dropping broadcast message to queue {queue_name}: {msg}')

    def _enqueue_on_connection(self, conn_id: int, msg):
        # print(f'Enquing {msg} on connection {conn_id}')
        conn = self._connections[conn_id]
        conn.input_queue.put_nowait(msg)
