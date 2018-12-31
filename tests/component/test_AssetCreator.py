import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetCreator(test.ComponentTest):

    def setUp(self):
        self.comp = component.AssetCreator('comp1', {})

    def tearDown(self):
        db.commit()

    def _create_or_get(self, filename):
        self.comp.setup({'filename': filename})
        queue, result = self.comp.run()
        self.assertEqual('default', queue)

        asset = entity.Asset()
        asset.id = result['asset_id']
        asset.load()

        self.assertEqual(filename, asset.filename)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': asset.id
                         }, result)

        queue, result = self.comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)

        return asset.id

    def test_create_and_get(self):
        filename = 'some/file/name'

        id1 = self._create_or_get(filename)
        id2 = self._create_or_get(filename)

        self.assertEqual(id1, id2)

        asset = entity.Asset()
        asset.id = id1
        asset.delete()

        self.verify_end_of_stream(self.comp)
