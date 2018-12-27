from unittest import TestCase
import os
import shutil

import sentinel.persistence as persistence
import sentinel.entity as entity


class TestAsset(TestCase):

    def _execute(self, sql):
        cur = persistence.Database.get_connection().cursor()
        cur.execute(sql)
        return cur.fetchall()

    def setUp(self):
        self.dir = os.path.join('tmp')
        try:
            shutil.rmtree('tmp')
        except FileNotFoundError:
            pass
        os.makedirs(self.dir)

        self.filename = os.path.join(self.dir, 'file1')

        with open(self.filename, 'w+') as f:
            f.write('a')

        rows = self._execute('select * from asset_type')

        self.type1 = entity.AssetType()
        self.type1.id = 1
        self.type1.name = 'AssetType1'
        self.type1.insert()

        self.asset = entity.Asset()
        self.asset.name = 'DefaultAsset'
        self.asset.filename = self.filename
        self.asset.asset_type_id = self.type1.id
        self.asset.processing_state_id = entity.ProcessingState.PENDING
        self.asset.save()

        self.asset.generate_and_save_hash()

    def tearDown(self):
        persistence.Database.get_connection().rollback()

    def test_save(self):
        a1 = entity.Asset()
        a1.name = 'Asset1'
        a1.filename = 'dir1/file1.asset'
        a1.asset_type_id = self.type1.id
        a1.processing_state_id = entity.ProcessingState.PENDING
        a1.save()

        a2 = entity.Asset()
        a2.id = a1.id
        a2.load()

        self.assertEqual(a1.name, a2.name)
        self.assertEqual(a1.filename, a2.filename)
        self.assertEqual(a1.asset_type_id, self.type1.id)
        self.assertEqual(a1.processing_state_id, entity.ProcessingState.PENDING)

    def test_hash(self):
        self.assertEqual(self.asset.get_hash(), 'd24ec4f1a98c6e5b')

    def test_latest_hash(self):
        with open(self.filename, 'a') as f:
            f.write('b')
        self.asset.generate_and_save_hash()
        self.assertEqual(self.asset.get_hash(), '65f708ca92d04a61')

    def test_force_reload_latest_hash(self):
        with open(self.filename, 'a') as f:
            f.write('b')
        self.asset.generate_and_save_hash()
        self.asset._hash = None
        self.assertEqual(self.asset.get_hash(), '65f708ca92d04a61')
