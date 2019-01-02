import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetCreator(test.ComponentTest):

    def setUp(self):
        self.a1 = entity.Asset()
        self.a1.filename = 'path/to/asset1'
        self.a1.save()

        self.a2 = entity.Asset()
        self.a2.filename = 'path/to/asset2'
        self.a2.save()

    def tearDown(self):
        self.a1.delete()
        self.a2.delete()
        db.commit()

    def _create_message(self):
        return {
            'msg_type': 'regular',
            'group_name': 'default',
            'group': [
                {'msg_type': 'regular', 'asset_id': self.a1.id},
                {'msg_type': 'regular', 'asset_id': self.a2.id}
            ]
        }

    def test_default_flags(self):
        comp = component.Command('comp1',
                                 {
                                     'command': 'path/to/command',
                                     'project': 'path/to/project/file',
                                     'flags': ['-names', '-paths']
                                 })
        comp.test = True

        msg = self._create_message()

        expected = [
            'path/to/command',
            'path/to/project/file',
            '-names',
            '-paths',
            'path/to/asset1',
            'path/to/asset2'
        ]

        comp.setup(msg)
        self.assertEqual(expected, comp.run())

    def test_type_flags(self):
        comp = component.Command('comp1',
                                 {
                                     'command': 'path/to/command',
                                     'project': 'path/to/project/file',
                                     'flags': ['-names', '-paths'],
                                     'type_flags': {
                                         'blueprint': ['-deps', '-abs'],
                                         'texture': ['-size']
                                     }
                                 })
        comp.test = True

        # Blueprint
        msg = self._create_message()
        msg['asset_type'] = 'blueprint'

        expected = [
            'path/to/command',
            'path/to/project/file',
            '-names',
            '-paths',
            '-deps',
            '-abs',
            'path/to/asset1',
            'path/to/asset2'
        ]

        comp.setup(msg)
        self.assertEqual(expected, comp.run())

        # Texture
        msg['asset_type'] = 'texture'

        expected = [
            'path/to/command',
            'path/to/project/file',
            '-names',
            '-paths',
            '-size',
            'path/to/asset1',
            'path/to/asset2'
        ]

        comp.setup(msg)
        self.assertEqual(expected, comp.run())

    def test_actual_run(self):
        comp = component.Command('comp1',
                                 {
                                     'command': 'say_hello.bat'
                                 })

        msg = {}

        comp.setup(msg)
        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
            'msg_type': 'regular',
            'command_output': 'hello\n'
        }, result)
