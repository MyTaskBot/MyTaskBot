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
    def __init__(self, user_id=None, text=None, t_id=None, dtime=None):
        super().__init__(text=text, user_id=user_id, t_id=t_id)
        self.datetime = dtime
        
    def set_datetime(self, dtime):
        assert dtime is not None, "Text must be not null"
        assert type(dtime) == datetime.datetime, "Text must be string"
        self.datetime = dtime

        
class User(object):
    def __init__(self, name, chat_id, user_id, gmt=3):
        self.name = name
        self.chat_id = chat_id
        self.user_id = user_id
        self.gmt = gmt

    def change_name(self, new_name):
        assert new_name is not None, "New_name must be not null"
        assert type(new_name) == str, "New_name must be string"
        self.name = new_name
        
    def change_gmt(self, new_gmt):
        assert type(new_gmt) == int, "New_name must be string"
        if -12 < new_gmt < 13:
            self.gmt = new_gmt
