from unittest import TestCase

import persistence
import entity

db = persistence.Database()


class TestAssetType(TestCase):

    def setUp(self):
        self.asset_type = entity.AssetType()
        self.asset_type.id = 1
        self.asset_type.name = 'AssetType1'
        self.asset_type.insert()

    def tearDown(self):
        db.rollback()

    def test_load(self):
        at = entity.AssetType()
        at.id = 1
        at.load()

        self.assertEqual(self.asset_type.id, at.id)
        self.assertEqual(self.asset_type.name, at.name)

    def test_load_by_name(self):
        at = entity.AssetType()
        at.name = 'AssetType1'
        at.load_by_name()

        self.assertEqual(self.asset_type.id, at.id)
        self.assertEqual(self.asset_type.name, at.name)

    def test_save(self):
        at1 = entity.AssetType()
        at1.id = 1
        at1.load()

        at1.name = 'ChangedName'
        at1.save()

        at2 = entity.AssetType()
        at2.id = 1
        at2.load()

        self.assertEqual(at1.id, at2.id)
        self.assertEqual(at1.name, at2.name)
