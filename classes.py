import datetime 

class Task(object):
    def __init__(self, date, time, task_text):
        self.date = date
        self.time = time
        self.task_text = task_text
        
    def get_date_and_time(self, string):
        try:
            tmp = datetime.datetime.strptime(string, '%d.%m.%y %H:%M')
            self.date = tmp.date()
            self.time = tmp.time()
        except ValueError:
            raise NameError('Convert string datetime to value data and time!')
        

class Target(object):
    def __init__(self, text):
        self.text = text

class User(object):
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id
        self.tasks = list()
        self.targets = list()
        
    def add_task(self, task = None):
        assert task != None, "Task in not defined" # think about types !!!
        self.tasks.append(task)
        
    def add_terget(self, target = None):
        assert target != None, "Target in not defined" # think about types !!!
        self.targets.append(target)

