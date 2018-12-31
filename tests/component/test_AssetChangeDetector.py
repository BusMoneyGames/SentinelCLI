import os
import shutil

import Utilities.test as test
import persistence
import component
import entity

db = persistence.Database()


class TestAssetChangeDetector(test.ComponentTest):

    def setUp(self):
        self.dir = os.path.join('tmp', 'dir')
        try:
            shutil.rmtree(os.path.split(self.dir)[0])
        except FileNotFoundError:
            pass
        os.makedirs(self.dir)

        self.filename = os.path.join(self.dir, 'file1')

        with open(self.filename, 'w+') as f:
            f.write('a')

        self.asset = entity.Asset()
        self.asset.filename = self.filename
        self.asset.set_processing_state(entity.ProcessingState.PENDING)
        self.asset.save()

    def tearDown(self):
        self.asset.delete()
        db.commit()

    def test_new(self):
        comp = component.AssetChangeDetector('comp1', {})
        comp.setup({'asset_id': self.asset.id})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': self.asset.id
                         }, result)

        self.verify_end_of_stream(comp)

    def test_no_change(self):
        # The asset has not changed if it has two alike consecutive hashes.
        # Simulate a previous run by manually generating a second hash.
        self.asset.generate_and_save_hash()

        comp = component.AssetChangeDetector('comp1', {})
        comp.setup({'asset_id': self.asset.id})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

        self.verify_end_of_stream(comp)

    def test_change(self):
        with open(self.filename, 'a') as f:
            f.write('b')

        comp = component.AssetChangeDetector('comp1', {})
        comp.setup({'asset_id': self.asset.id})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'asset_id': self.asset.id
                         }, result)

        self.verify_end_of_stream(comp)
