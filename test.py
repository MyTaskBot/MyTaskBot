import unittest

#  to run tests exc python3 -m unittest -v test.py

from classes import Task, Target, User


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_task_time(self):
        self.assertEqual(Task.set_date_and_time(Task(), '22.11.63 22:44'), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be not null'):
            Task.set_date_and_time(Task(), None)
        with self.assertRaisesRegex(AssertionError, 'Text must be string'):
            Task.set_date_and_time(Task(), 1)
        with self.assertRaisesRegex(NameError, 'Convert string datetime to value data and time!'):
            Task.set_date_and_time(Task(), '22.13.53 22:44')

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
        self.assertEqual(User.change_name(User('Sviat', 2), 'Igor'), None)
        with self.assertRaisesRegex(AssertionError, 'New_name must be string'):
            User.change_name(User('Sviat', 2), 456785455344444443433434433443)
        with self.assertRaisesRegex(AssertionError, 'New_name must be not null'):
            User.change_name(User('Sviat', 2), None)

    def test_add_task(self):
            self.assertEqual(User.add_task(User('Sviat', 2), Task()), None)
            with self.assertRaisesRegex(AssertionError, 'task must be Task'):
                User.add_task(User('Sviat', 2), 456785455344444443433434433443)
            with self.assertRaisesRegex(AssertionError, 'task must be not null'):
                User.add_task(User('Sviat', 2), None)

    def test_add_target(self):
                self.assertEqual(User.add_target(User('Sviat', 2), Target()), None)
                with self.assertRaisesRegex(AssertionError, 'target must be Target'):
                    User.add_target(User('Sviat', 2), 456785455344444443433434433443)
                with self.assertRaisesRegex(AssertionError, 'target must be not null'):
                    User.add_target(User('Sviat', 2), None)



suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)