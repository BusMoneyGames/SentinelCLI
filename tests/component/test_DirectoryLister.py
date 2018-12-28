from unittest import TestCase

import os
import shutil

import sentinel.component as component


class TestDirectoryLister(TestCase):

    def setUp(self):
        self.root = os.path.join(os.getcwd(), 'tmp')
        self.level1 = os.path.join(self.root, 'dir1')
        self.level2 = os.path.join(self.root, 'dir1', 'dir2')
        try:
            shutil.rmtree(self.root)
        except FileNotFoundError:
            pass
        os.makedirs(self.level2)

    def test_empty_directory(self):
        comp = component.DirectoryLister('comp1', {})
        comp.setup({'directory': self.root, 'extension': '.txt'})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

    def test_list_directory(self):
        with open(os.path.join(self.root, 'file1.txt'), 'w+') as f:
            f.write('a')
        with open(os.path.join(self.level1, 'file2.txt'), 'w+') as f:
            f.write('b')
        with open(os.path.join(self.level2, 'file3.txt'), 'w+') as f:
            f.write('c')
        with open(os.path.join(self.level2, 'file4.abc'), 'w+') as f:
            f.write('d')

        comp = component.DirectoryLister('comp1', {})
        comp.setup({'directory': self.root, 'extension': '.txt'})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'filename': os.path.join(self.root, 'file1.txt')
                         }, result)

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'filename': os.path.join(self.level1, 'file2.txt')
                         }, result)

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'filename': os.path.join(self.level2, 'file3.txt')
                         }, result)

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

    def test_windows_path(self):
        subdirs = os.path.join('tmp', 'dir1', 'dir2')
        with open(os.path.join(subdirs, 'file1.txt'), 'w+') as f:
            f.write('a')

        comp = component.DirectoryLister('comp1', {})
        comp.setup({'directory': 'tmp\\dir1\\dir2', 'extension': '.txt'})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'filename': os.path.join(subdirs, 'file1.txt')
                         }, result)

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

    def test_mixed_path(self):
        subdirs = os.path.join('tmp', 'dir1', 'dir2')
        with open(os.path.join(subdirs, 'file1.txt'), 'w+') as f:
            f.write('a')

        comp = component.DirectoryLister('comp1', {})
        comp.setup({'directory': 'tmp/dir1\\dir2', 'extension': '.txt'})

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertEqual({
                             'msg_type': 'regular',
                             'filename': os.path.join(subdirs, 'file1.txt')
                         }, result)

        queue, result = comp.run()
        self.assertEqual('default', queue)
        self.assertIsNone(result)

