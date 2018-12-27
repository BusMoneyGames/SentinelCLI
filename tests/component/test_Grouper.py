from unittest import TestCase

import sentinel.component as component


class TestGrouper(TestCase):

    def test_grouping(self):
        comp = component.Grouper('comp1',
                                 {
                                    'group_size': 3,
                                    'stream_end_count': 2
                                 })

        # TODO: setup should understand group_name and group messages having
        #  that key into the group with that name. If the group does not exist
        #  then create it (and add the message to it).
        #  Then I don't need a separate BinGrouper.

        # Group 1 (full)

        comp.setup({'property1': 'something1', 'property2': 10})
        result = comp.run()
        self.assertIsNone(result)

        comp.setup({'property1': 'something2', 'property2': 20})
        result = comp.run()
        self.assertIsNone(result)

        comp.setup({'property1': 'something3', 'extra': 35})
        result = comp.run()
        self.assertEqual({
                             'msg_type': 'regular',
                             'group':
                             [
                                 {'property1': 'something1', 'property2': 10},
                                 {'property1': 'something2', 'property2': 20},
                                 {'property1': 'something3', 'extra': 35}
                             ]
                         }, result)

        # Group 2 (full)

        comp.setup({'property1': 'something4', 'property2': 40})
        result = comp.run()
        self.assertIsNone(result)

        comp.setup({'property1': 'something5', 'property2': 50})
        result = comp.run()
        self.assertIsNone(result)

        comp.setup({'property1': 'something6', 'extra': 65})
        result = comp.run()
        self.assertEqual({
                             'msg_type': 'regular',
                             'group':
                             [
                                 {'property1': 'something4', 'property2': 40},
                                 {'property1': 'something5', 'property2': 50},
                                 {'property1': 'something6', 'extra': 65}
                             ]
                         }, result)

        # Group 3 (partial)

        comp.setup({'property1': 'something7', 'property2': 70})
        result = comp.run()
        self.assertIsNone(result)

        # Worker 1 signals done
        comp.setup({'stream_end': None})
        result = comp.run()
        self.assertIsNone(result)

        comp.setup({'property1': 'something8', 'extra': 85})
        result = comp.run()
        self.assertIsNone(result)

        # Worker 2 (last one) signals done and triggers the group
        comp.setup({'stream_end': None})
        result = comp.run()
        self.assertEqual({
                             'msg_type': 'regular',
                             'group':
                             [
                                 {'property1': 'something7', 'property2': 70},
                                 {'property1': 'something8', 'extra': 85}
                             ]
                         }, result)

