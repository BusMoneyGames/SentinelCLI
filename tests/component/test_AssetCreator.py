from unittest import TestCase

import persistence
import component
import entity

db = persistence.Database()


class TestAssetCreator(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        db.rollback()

    def test_create(self):
        filename = 'some/file/name'
        comp = component.AssetCreator('comp1', {})
        comp.setup({'filename': filename})

        result = comp.run()

        asset = entity.Asset()
        asset.id = result['asset_id']
        asset.load()

        self.assertEqual(filename, asset.filename)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': asset.id
                         }, result)
