import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetCreator(test.ComponentTest):

    def setUp(self):
        pass

    def tearDown(self):
        db.rollback()

    def test_create(self):
        filename = 'some/file/name'
        comp = component.AssetCreator('comp1', {})

        comp.setup({'filename': filename})
        queue, result = comp.run()
        self.assertEqual('default', queue)

        asset = entity.Asset()
        asset.id = result['asset_id']
        asset.load()

        self.assertEqual(filename, asset.filename)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': asset.id
                         }, result)

        self.verify_end_of_stream(comp)

