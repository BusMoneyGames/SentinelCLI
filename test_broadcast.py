import asyncio
import time

import sentinel.routing as routing
import sentinel.component as component


class Number:
    def __init__(self, value):
        self.value = value


queues = [
    {'name': 'input'},
    {'name': 'output'},
    {'name': 'result'}
]

components = {
    'intermediate': {
        'class_name': 'Printer',
        'instance_count': 2,
        'input_queue': 'input',
        'output_queues': {
            'default': 'output'
        },
        'config': {}
    },
    'result': {
        'class_name': 'Printer',
        'instance_count': 1,
        'input_queue': 'output',
        'output_queues': {
            'default': 'result'
        },
        'config': {
            'sync_eos': True
        }
    }
}
components['result']['config']['sync_eos_count'] = \
    components['intermediate']['instance_count']

# Should print out at the end something similar to the following.
# The order may vary but the message
#  'result-0 received all end of stream messages'
# should always be last.
#
# ...
# intermediate-0 received {'property1': 10}
# intermediate-0 received {'property1': 20}
# intermediate-0 received {'end_of_stream': True}
# intermediate-1 received {'end_of_stream': True}
# result-0 received {'end_of_stream': True, 'msg_type': 'broadcast', 'from': 'intermediate-0'}
# result-0 received {'end_of_stream': True, 'msg_type': 'broadcast', 'from': 'intermediate-1'}
# result-0 received all end of stream messages

if __name__ == '__main__':
    # The queue server needs to be running before the builder runs
    queue_server = routing.QueueServer(queues)
    queue_server.start()

    builder = component.Builder(components)

    # Enable the builder to run async (doesn't do anything for now)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(builder.run())

    # Wait a while to allow the components to start and connect
    # TODO: Deterministically wait for the components to become ready
    #       in the builder (builder.run).
    #       The best way is probably to add a system queue and wait
    #       for all the components to post a ready message onto that queue.
    time.sleep(1)

    builder.send('input', {'property1': 10})
    builder.send('input', {'property1': 20})
    builder.broadcast('input', {'end_of_stream': True})

    queue_server.join()
    builder.join_all()
