import unittest

#  to run tests exc python3 -m unittest -v test.py
import datetime

from classes import Task, Target, User


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_task_time(self):
        self.assertEqual(Task.set_datetime(Task(), datetime.datetime(2012, 9, 16, 0, 0)), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be not null'):
            Task.set_datetime(Task(), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be string'):
            Task.set_datetime(Task(), 1)

    def test_set_task_text(self):
        self.assertEqual(Task.set_text(Task(), 'Create task'), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be string'):
            Task.set_text(Task(), 456785455344444443433434433443)
        with self.assertRaisesRegex(AssertionError, 'Text must be not null'):
            Task.set_text(Task(), None)

    def test_set_target_text(self):
        self.assertEqual(Target.set_text(Target(), 'My target'), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be string'):
            Target.set_text(Target(), 456785455344444443433434433443)
        with self.assertRaisesRegex(AssertionError, 'Text must be not null'):
            Target.set_text(Target(), None)

    def test_change_user_name(self):
        self.assertEqual(User.change_name(User('Sviat', 2, 2), 'Igor'), None)
        with self.assertRaisesRegex(AssertionError, 'New_name must be string'):
            User.change_name(User('Sviat', 2, 2), 456785455344444443433434433443)
        with self.assertRaisesRegex(AssertionError, 'New_name must be not null'):
            User.change_name(User('Sviat', 2, 2), None)



suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)