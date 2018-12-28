from unittest import TestCase
import os
import shutil

import persistence
import entity

db = persistence.Database()


class TestAsset(TestCase):

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

        self.type1 = entity.AssetType()
        self.type1.id = 1
        self.type1.name = 'AssetType1'
        self.type1.insert()

        self.asset = entity.Asset()
        self.asset.name = 'DefaultAsset'
        self.asset.filename = self.filename
        self.asset.set_type(self.type1)
        self.asset.set_processing_state(entity.ProcessingState.PENDING)
        self.asset.save()

        self.asset.generate_and_save_hash()

    def tearDown(self):
        db.rollback()

    def test_load(self):
        a1 = entity.Asset()
        a1.id = self.asset.id
        a1.load()

        self.assertEqual(a1.name, self.asset.name)
        self.assertEqual(a1.filename, self.asset.filename)
        self.assertEqual(a1.asset_type_id, self.asset.asset_type_id)
        self.assertEqual(a1.processing_state_id, self.asset.processing_state_id)

    def test_load_by_filename(self):
        a1 = entity.Asset()
        a1.filename = self.asset.filename
        a1.load_by_filename()

        self.assertEqual(a1.name, self.asset.name)
        self.assertEqual(a1.filename, self.asset.filename)
        self.assertEqual(a1.asset_type_id, self.asset.asset_type_id)
        self.assertEqual(a1.processing_state_id, self.asset.processing_state_id)

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

    def test_add_rule_violation(self):
        rv1 = entity.RuleViolation()
        rv1.rule_name = 'Rule1'
        rv1.rule = 'rule expression'
        rv1.reason = 'Reason'
        rv1.save()

        self.asset.add_rule_violation(rv1)

        rule_violations = self.asset.get_rule_violations()
        rv2 = rule_violations[0]

        self.assertEqual(rv1.id, rv2.id)
        self.assertEqual(rv1.rule_name, rv2.rule_name)
        self.assertEqual(rv1.rule, rv2.rule)
        self.assertEqual(rv1.reason, rv2.reason)

    def test_add_multiple_rule_violations(self):
        for i in range(10):
            rv = entity.RuleViolation()
            rv.rule_name = f'Rule{i}'
            rv.rule = f'rule expression {i}'
            rv.reason = f'Reason {i}'
            rv.save()
            self.asset.add_rule_violation(rv)

        rule_violations = self.asset.get_rule_violations()

        i = 0
        for rv in rule_violations:
            self.assertEqual(f'Rule{i}', rv.rule_name)
            self.assertEqual(f'rule expression {i}', rv.rule)
            self.assertEqual(f'Reason {i}', rv.reason)
            i += 1
