from unittest import TestCase

import persistence
import entity

db = persistence.Database()


class TestRuleViolation(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        db.rollback()

    def test_save_load_update(self):
        rv1 = entity.RuleViolation()
        rv1.rule_name = 'Rule 1'
        rv1.rule = 'Some rule'
        rv1.reason = 'The reason the rule was violated'
        rv1.save()

        rv2 = entity.RuleViolation()
        rv2.id = rv1.id
        rv2.load()

        self.assertEqual(rv1.id, rv2.id)
        self.assertEqual(rv1.rule_name, rv2.rule_name)
        self.assertEqual(rv1.rule, rv2.rule)
        self.assertEqual(rv1.reason, rv2.reason)

        rv2.reason = 'Some new reason'
        rv2.save()

        rv3 = entity.RuleViolation()
        rv3.id = rv2.id
        rv3.load()

        self.assertEqual(rv2.id, rv3.id)
        self.assertEqual(rv2.rule_name, rv3.rule_name)
        self.assertEqual(rv2.rule, rv3.rule)
        self.assertEqual(rv2.reason, rv3.reason)
