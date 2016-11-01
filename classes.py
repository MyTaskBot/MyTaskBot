import datetime

class Task(object):
    def __init__(self, datetime = None, text = None):
        self.datetime = datetime
        self.text = text
        
    def set_date_and_time(self, string):
        assert string is not None, "Text must be not null"
        assert type(string) == str, "Text must be string"
        try:
            self.datetime = datetime.datetime.strptime(string, '%d.%m.%y %H:%M')
        except ValueError:
            raise NameError('Convert string datetime to value data and time!')
    
    def set_text(self, text):
        assert text is not None, "Text must be not null"
        assert type(text) == str, "Text must be string"
        self.text = text

        

class Target(object):
    def __init__(self, text = None):
        self.text = text
    
    def set_text(self, text):
        assert text is not None, "Text must be not null"
        assert type(text) == str, "Text must be string"
        self.text = text

        
class User(object):
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id
        self.tasks = list()
        self.targets = list()
        
    def change_name(self, new_name):
        assert new_name is not None, "New_name must be not null"
        assert type(new_name) == str, "New_name must be string"
        self.name = new_name
        
    def add_task(self, task):
        assert task is not None, "task must be not null"
        assert type(task) == Task, "task must be Task"
        # print ('\n\n {text}\n\n'.format(text = task.text))
        self.tasks.append(task)
        
    def add_target(self, target):
        assert target is not None, "target must be not null"
        assert type(target) == Target, "target must be Target"
        self.targets.append(target)
