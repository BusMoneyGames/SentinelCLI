import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetTypeChecker(test.ComponentTest):

    def setUp(self):
        self.asset = entity.Asset()
        self.asset.filename = 'some/file'
        self.asset.save()

    def tearDown(self):
        # Rollback is fine here because the component doesn't commit.
        db.rollback()

    def test_with_type(self):
        comp = component.AssetTypeChecker('comp1', {})

        comp.setup({'asset_id': self.asset.id})
        queue, result = comp.run()
        self.assertEqual('untyped', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': self.asset.id
                         }, result)

        self.verify_end_of_stream(comp)

    def test_without_type(self):
        comp = component.AssetTypeChecker('comp1', {})

        at = entity.AssetType()
        at.id = 1
        at.name = 'Some type'
        at.insert()

        self.asset.type_id = at.id
        self.asset.save()

        comp.setup({'asset_id': self.asset.id})
        queue, result = comp.run()
        self.assertEqual('typed', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': self.asset.id
                         }, result)

        self.verify_end_of_stream(comp)
