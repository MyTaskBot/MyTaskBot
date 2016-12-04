import psycopg2
from classes import *
from configDB import config

class Database ():
    def register_user(self, chat, name):
        sql = """INSERT INTO public."User"(chat, name)
                 VALUES(%s, %s) RETURNING chat;"""
        conn = None
        user_id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (chat, name))
            # get the generated id back
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return user_id

    def get_user(self, user_id):
            sql = """SELECT chat, name FROM public."User" WHERE chat = %s;"""
            conn = None
            id = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql, (user_id,))
                id = cur.fetchone()[0]
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return id

    def add_task(self, user_id, task):
        sql = """INSERT INTO public."Task"(user_t, text, time)
                 VALUES(%s, %s, %s) RETURNING id;"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id, task.text, task.datetime))
            id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return id

    def add_target(self, user_id, target):
        sql = """INSERT INTO public."Target"(user_t, text) VALUES(%s, %s) RETURNING id;"""
        conn = None
        id = None
        print(user_id)
        print(target.text)
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id, target.text,))
            id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return id


def get_target(self, user_id):
    sql = """SELECT text FROM public."Target" as t JOIN public."User" as u ON t.user_t = u.id WHERE u.chat = %s;"""
    conn = None
    list = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (user_id,))
        rows = cur.fetchone()
        for row in rows:
            list.add[Task(row)]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return list


