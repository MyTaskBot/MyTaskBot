import datetime


class Target(object):
    def __init__(self, user_id=None, text=None, t_id=None):
        self.text = text
        self.id = t_id
        self.user_id = user_id

    def set_text(self, text):
        assert text is not None, "Text must be not null"
        assert type(text) == str, "Text must be string"
        self.text = text


class Task(Target):
    def __init__(self, dtime=None, text=None):
        super().__init__(text=text)
        self.datetime = dtime
        
    def set_date_and_time(self, string):
        assert string is not None, "Text must be not null"
        assert type(string) == str, "Text must be string"
        try:
            self.datetime = datetime.datetime.strptime(string, '%d.%m.%y %H:%M')
        except ValueError:
            raise NameError('Convert string datetime to value data and time!')

        
class User(object):
    def __init__(self, name, chat_id, user_id):
        self.name = name
        self.chat_id = chat_id
        self.tasks = list()
        self.targets = list()
        self.user_id = user_id


    def change_name(self, new_name):
        assert new_name is not None, "New_name must be not null"
        assert type(new_name) == str, "New_name must be string"
        self.name = new_name
        
    def add_task(self, task):
        assert task is not None, "task must be not null"
        assert type(task) == Task, "task must be Task"
        self.tasks.append(task)
        
    def add_target(self, target):
        assert target is not None, "target must be not null"
        assert type(target) == Target, "target must be Target"
        self.targets.append(target)
