import datetime 

class Task(object):
    def __init__(self, datetime = None, task_text = None):
        self.datetime = datetime
        self.task_text = task_text
        
    def set_date_and_time(self, string):
        assert type(string) != type(str), "Text must be not null"
        try:
            self.datetime = datetime.datetime.strptime(string, '%d.%m.%y %H:%M')
        except ValueError:
            raise NameError('Convert string datetime to value data and time!')
    
    def set_text(self, text):
         assert type(text) != type(str), "Text must be not null"  
         self.text = text
        

class Target(object):
    def __init__(self, text = None):
        self.text = text
    
    def set_text(self, text):
        assert type(text) != type(str), "Text must be not null"
        self.text = text

        
class User(object):
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id
        self.tasks = list()
        self.targets = list()
        
    def change_name(self, new_name):
        assert type(new_name) != type(str), "New name must be not null"
        self.name = new_name
        
    def add_task(self, task):
        assert type(task) != type(str), "Task in not defined" # think about types !!!
        self.tasks.append(task)
        
    def add_target(self, target):
        assert type(target) != type(str), "Target in not defined" # think about types !!!
        self.targets.append(target)