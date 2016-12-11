import psycopg2
from classes import *
from configDB import config

class Database ():
    def register_user(self, user):
        sql = """INSERT INTO public."User"(user_id, chat_id, name)
                 VALUES(%s, %s, %s) RETURNING chat_id;"""
        conn = None
        user_id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user.user_id, user.chat_id, user.name,))
            # get the generated id back
            chat_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return chat_id

    def is_user(self, user_id):
        sql = """SELECT chat_id, name FROM public."User" WHERE user_id = %s;"""
        conn = None
        chat_id = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            res = cur.fetchone()
            if res:
                chat_id = res[0]
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error")
            print(error)
            print("error")
        finally:
            if conn is not None:
                conn.close()
        return chat_id

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
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id, target.text,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id


    def get_target(self, user_id):
        sql = """SELECT text FROM public."Target" as t JOIN public."User" as u ON t.user_t = u.user_id WHERE u.user_id = %s AND t.is_deleted = 0;"""
        conn = None
        list = []
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            for row in rows:
                list.append(Target(row[0]))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return list

    def get_tasks(self, user_id):
            sql = """SELECT time, text FROM public."Task" as t JOIN public."User" as u ON t.user_t = u.user_id WHERE u.user_id = %s AND t.is_deleted = 0 AND is_done = 0"""
            conn = None
            list = []
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql, (user_id,))
                rows = cur.fetchall()
                for row in rows:
                    list.append(Task(row[0], row[1]))
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return list

    def remove_target(self, user_id, target):
        sql = """UPDATE public."Target" SET is_deleted = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (target.id, user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id

    def remove_task(self, user_id, task):
        sql = """UPDATE public."Task" SET is_deleted = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (task.id, user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id

    def done_task(self, user_id, task):
        sql = """UPDATE public."Task" SET is_done = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (task.id, user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id


    def get_all_users(self):
            sql = """SELECT name, chat, user_id, name FROM public."User" """
            conn = None
            list = []
            users = dict()
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    users[row[2]] = User(row[0], row[1], row[2])
                    print(row[0])
                    print(row[1])
                    print(row[2])
                    print(users[row[2]])
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return users

    def get_recent_tasks(self, time):
        sql = """SELECT time, text FROM public."Task" WHERE time = %s AND t.is_deleted = 0 AND is_done = 0 ORDER BY TIME ASC"""
        conn = None
        list = []
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (time,))
            rows = cur.fetchall()
            for row in rows:
                list.append(Task(row[0], row[1]))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return list





