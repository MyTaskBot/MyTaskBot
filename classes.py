import datetime 

class User(object):
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id

class Task(object):
	def __init__(self, date, time, task_text):
		self.date = date
		self.time = time
		self.task_text = task_text
