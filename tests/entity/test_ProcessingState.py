from unittest import TestCase

import persistence
import entity

db = persistence.Database()


class TestProcessingState(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        db.rollback()

    def test_default_states(self):
        state = entity.ProcessingState()
        state.id = 1
        state.load()

        self.assertEqual(1, state.id)
        self.assertEqual('Pending', state.name)

    def test_save(self):
        state1 = entity.ProcessingState()
        state1.id = 1
        state1.load()

        state1.name = 'New name'
        state1.save()

        state2 = entity.ProcessingState()
        state2.id = 1
        state2.load()

        self.assertEqual(state1.id, state2.id)
        self.assertEqual(state1.name, state2.name)

    def test_insert(self):
        state1 = entity.ProcessingState()
        state1.id = 4
        state1.name = 'Unknown state'
        state1.insert()

        state2 = entity.ProcessingState()
        state2.id = 4
        state2.load()

        self.assertEqual(state1.id, state2.id)
        self.assertEqual(state1.name, state2.name)
