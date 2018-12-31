import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetGrouper(test.ComponentTest):

    def setUp(self):
        self.assets = []

        self.type_count = 2
        self.assets_per_type = 5

        for type_id in range(self.type_count):
            assets = []
            self.assets.append(assets)

            asset_type = entity.AssetType()
            asset_type.id = type_id
            asset_type.name = f'Type {type_id}'
            asset_type.insert()

            for i in range(self.assets_per_type):
                a = entity.Asset()
                a.filename = f'type{type_id}{i}'
                a.set_type(asset_type)
                a.save()

                assets.append(a)

    def tearDown(self):
        for type_id in range(self.type_count):
            for i in range(self.assets_per_type):
                self.assets[type_id][i].delete()
        for type_id in range(self.type_count):
            asset_type = entity.AssetType()
            asset_type.id = type_id
            asset_type.delete()
        db.commit()

    def test_default_full_group(self):
        group_size = 3
        comp = component.AssetGrouper('comp1',
                                      {
                                          'group_size': group_size
                                      })

        for type_id in range(self.type_count):

            for i in range(group_size - 1):
                comp.setup({'asset_id': self.assets[type_id][i].id})
                queue, result = comp.run()
                self.assertEqual('default', queue)
                self.assertIsNone(result)

            comp.setup({'asset_id': self.assets[type_id][i + 1].id})
            queue, result = comp.run()
            self.assertEqual('default', queue)
            self.assertEqual('regular', result['msg_type'])
            self.assertEqual('default', result['group_name'])
            self.assertEqual(3, len(result['group']))
            for i in range(group_size):
                self.assertEqual({'asset_id': self.assets[type_id][i].id},
                                 result['group'][i])

        # EOS
        comp.setup({'from': comp.name, 'end_of_stream': True})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        queue, result = comp.run()
        self.assertEqual('*', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

    def test_default_trailing_group(self):
        group_size = 3
        comp = component.AssetGrouper('comp1',
                                 {
                                     'group_size': group_size
                                 })

        # Group 1 (full)
        comp.setup({'asset_id': self.assets[0][0].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][1].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][2].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual('default', result['group_name'])
        self.assertEqual(group_size, len(result['group']))
        for i in range(group_size):
            self.assertEqual({'asset_id': self.assets[0][i].id},
                             result['group'][i])

        # Group 2 (partial)
        comp.setup({'asset_id': self.assets[0][3].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][4].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        # EOS
        comp.setup({'from': comp.name, 'end_of_stream': True})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual('default', result['group_name'])
        self.assertEqual(2, len(result['group']))
        for i in range(2):
            self.assertEqual({'asset_id': self.assets[0][group_size + i].id},
                             result['group'][i])

        queue, result = comp.run()
        self.assertEqual('*', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

    def test_default_trailing_group_multiple_senders(self):
        group_size = 3
        comp = component.AssetGrouper('comp1',
                                 {
                                     'sync_eos_count': 2,
                                     'group_size': group_size
                                 })

        # Group 1 (full)
        comp.setup({'asset_id': self.assets[0][0].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][1].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][2].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual('default', result['group_name'])
        self.assertEqual(group_size, len(result['group']))
        for i in range(group_size):
            self.assertEqual(
                {
                    'asset_id': self.assets[0][i].id
                }, result['group'][i])

        # Group 2 (partial)
        comp.setup({'asset_id': self.assets[0][3].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        # EOS from comp1
        comp.setup({'from': 'comp1', 'end_of_stream': True})
        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][4].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        # EOS from comp2
        comp.setup({'from': 'comp2', 'end_of_stream': True})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual('default', result['group_name'])
        self.assertEqual(2, len(result['group']))
        for i in range(2):
            self.assertEqual(
                {
                    'asset_id': self.assets[0][group_size + i].id
                }, result['group'][i])

        queue, result = comp.run()
        self.assertEqual('*', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

    def test_dynamic_full_groups(self):
        group_size = 3
        comp = component.AssetGrouper('comp1',
                                 {
                                     'group_size': group_size,
                                     'group_by': 'type_id'
                                 })

        for type_id in range(self.type_count):

            for i in range(group_size - 1):
                comp.setup({'asset_id': self.assets[type_id][i].id})
                queue, result = comp.run()
                self.assertEqual('default', queue)
                self.assertIsNone(result)

            comp.setup({'asset_id': self.assets[type_id][i + 1].id})
            queue, result = comp.run()
            self.assertEqual('default', queue)
            self.assertEqual('regular', result['msg_type'])
            self.assertEqual(type_id, result['group_name'])
            self.assertEqual(3, len(result['group']))
            for i in range(group_size):
                self.assertEqual({'asset_id': self.assets[type_id][i].id},
                                 result['group'][i])

        # EOS
        comp.setup({'from': comp.name, 'end_of_stream': True})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        queue, result = comp.run()
        self.assertEqual('*', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

    def test_dynamic_trailing_groups(self):
        group_size = 3
        comp = component.AssetGrouper('comp1',
                                 {
                                     'group_size': group_size,
                                     'group_by': 'type_id'
                                 })

        # 1st 2 full groups
        comp.setup({'asset_id': self.assets[0][0].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[1][0].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][1].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[1][1].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        # Full group 1
        comp.setup({'asset_id': self.assets[1][2].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual(1, result['group_name'])
        self.assertEqual(group_size, len(result['group']))
        for i in range(group_size):
            self.assertEqual({'asset_id': self.assets[1][i].id},
                             result['group'][i])

        # Full group 2
        comp.setup({'asset_id': self.assets[0][2].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual(0, result['group_name'])
        self.assertEqual(group_size, len(result['group']))
        for i in range(group_size):
            self.assertEqual({'asset_id': self.assets[0][i].id},
                             result['group'][i])

        # 2nd 2 partial groups
        comp.setup({'asset_id': self.assets[0][3].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[1][3].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[1][4].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        comp.setup({'asset_id': self.assets[0][4].id})
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        # EOS
        comp.setup({'from': comp.name, 'end_of_stream': True})

        # Partial group 1
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual(1, result['group_name'])
        self.assertEqual(2, len(result['group']))
        for i in range(2):
            self.assertEqual({'asset_id': self.assets[1][group_size + i].id},
                             result['group'][i])

        # Partial group 2
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual('regular', result['msg_type'])
        self.assertEqual(0, result['group_name'])
        self.assertEqual(2, len(result['group']))
        for i in range(2):
            self.assertEqual({'asset_id': self.assets[0][group_size + i].id},
                             result['group'][i])

        queue, result = comp.run()
        self.assertEqual('*', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)
