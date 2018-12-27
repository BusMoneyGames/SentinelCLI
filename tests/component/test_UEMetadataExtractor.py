from unittest import TestCase
import os

import sentinel.component as component


class TestUEMetadataExtractor(TestCase):

    def test_change(self):
        comp = component.AssetChangeDetector('comp1', {})
        comp.setup({'filename': self.filename})

        done, result = comp.run()
        self.assertFalse(done)
        self.assertEqual(result,
                         {
                             'msg_type': 'regular',
                             'filename': os.path.join(self.dir, 'file1')
                         })

