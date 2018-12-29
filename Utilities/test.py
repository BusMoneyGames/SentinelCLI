from unittest import TestCase


class ComponentTest(TestCase):

    def verify_end_of_stream(self, comp):
        comp.setup({'end_of_stream': True})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
            'msg_type': 'broadcast',
            'from': comp.name,
            'end_of_stream': True
        }, result)

        queue, result = comp.run()
        self.assertIsNone(queue)
        self.assertIsNone(result)
