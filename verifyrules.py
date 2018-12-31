import os
import time

import persistence
import sentinel.routing as routing
import sentinel.component as component

db = persistence.Database()

queues = [
    {'name': 'pre.directory'},
    {'name': 'pre.asset_file'},
    {'name': 'pre.unchecked_asset'},
    {'name': 'pre.changed_asset'},
    {'name': 'untyped.asset'},
    {'name': 'untyped.asset_group'},
    {'name': 'untyped.assets_type_info'},
    {'name': 'untyped.asset_type_info'},
    {'name': 'typed.asset'},
    {'name': 'typed.asset_group'},
    {'name': 'typed.assets_rule_info'},
    {'name': 'typed.asset_rule_info'},
    {'name': 'rules.unverified_asset'},
    {'name': 'rules.verified_asset'},
    {'name': 'post.result'}
]

components = {
    'list directory recursively': {
        'class_name': 'DirectoryLister',
        'instance_count': 1,
        'input_queue': 'pre.directory',
        'output_queues': {
            'default': 'pre.asset_file'
        },
        'config': {}
    },
    'create/get asset': {
        'class_name': 'AssetCreator',
        'instance_count': 1,
        'input_queue': 'pre.asset_file',
        'output_queues': {
            'default': 'pre.unchecked_asset'
        },
        'config': {}
    },
    # 'detect changed asset': {
    #     'class_name': 'AssetChangeDetector',
    #     'instance_count': 2,
    #     'input_queue': 'pre.unchecked_asset',
    #     'output_queues': {
    #         'default': 'pre.changed_asset'
    #     },
    #     'config': {}
    # },
    'is asset type known?': {
        'class_name': 'AssetTypeChecker',
        'instance_count': 1,
        # 'input_queue': 'pre.changed_asset',
        'input_queue': 'pre.unchecked_asset',  # To test the typed path
        'output_queues': {
            'typed': 'typed.asset',
            'untyped': 'untyped.asset'
        },
        'config': {}
    },
    # 'group into bin': {
    #     'class_name': 'AssetGrouper',
    #     'instance_count': 1,
    #     'input_queue': 'untyped.asset',
    #     'output_queues': {
    #         'default': 'untyped.asset_group'
    #     },
    #     'config': {
    #         'group_size': 3
    #     }
    # },
    # 'group into bins by type': {
    #     'class_name': 'AssetGrouper',
    #     'instance_count': 1,
    #     'input_queue': 'typed.asset',
    #     'output_queues': {
    #         'default': 'typed.asset_group'
    #     },
    #     'config': {
    #         'sync_eos_count': -1,
    #         'group_size': 3,
    #         'group_by': 'type_id'
    #     }
    # }
}

# Update the config instance counts to match the real instance counts
# components['is asset type known?']['config']['sync_eos_count'] = \
#    components['detect changed asset']['instance_count']

if __name__ == '__main__':
    # The queue server needs to be running before the builder runs
    queue_server = routing.QueueServer(queues)
    queue_server.start()

    builder = component.Builder(components)

    builder.wait_until_connected_to_server()
    builder.build()

    # Wait a while to allow the components to start and connect
    # TODO: Deterministically wait for the components to become ready
    #       before continuing (builder.run should wait)
    #       The best way is probably to add a system queue and wait
    #       for all the components to post a ready message onto that queue.
    #       Run builder.run async the same way builder.send and
    #       builder.broadcast do it.
    time.sleep(2)

    directory = os.path.join(os.getcwd(), 'test_content')
    builder.send('pre.directory',
                 {
                     'directory': directory,
                     'extension': '.uasset'
                 })
    builder.broadcast('pre.directory', {'from': 'builder', 'end_of_stream': True})
    # builder.print_queue('pre.asset_file')
    # builder.print_queue('pre.unchecked_asset')
    # builder.print_queue('pre.changed_asset')
    # builder.print_queue('untyped.asset')
    builder.print_queue('typed.asset')
    # builder.print_queue('untyped.asset_group')

    builder.wait_for_message('post.result', {'msg_type': 'regular', 'done': True})
    print("Done")

    builder.disconnect_from_server()

    queue_server.stop()
