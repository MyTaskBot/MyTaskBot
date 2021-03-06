import psycopg2
from classes import *
from configDB import config


class Database():


    def register_user(self, user):
        sql = """INSERT INTO public."User"(user_id, chat_id, name, gmt)
                 VALUES(%s, %s, %s, %s) RETURNING chat_id;"""
        conn = None
        chat_id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user.user_id, user.chat_id, user.name, user.gmt))
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
            print(error)
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
            cur.execute(sql, (user_id, task.text, task.datetime.strftime('%Y-%m-%d %H:%M')))
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
        sql = """SELECT text, id FROM public."Target" WHERE user_t = %s AND is_deleted = 0 AND is_done = 0;"""
        conn = None
        list = []
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            for row in rows:
                list.append(Target(text=row[0], user_id=user_id, t_id=row[1]))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return list

    def get_tasks(self, user_id):
            sql = """SELECT time, text, id FROM public."Task" WHERE user_t = %s AND is_deleted = 0 AND is_done = 0;"""
            conn = None
            list = []
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql, (user_id,))
                rows = cur.fetchall()
                for row in rows:
                    list.append(Task(
                        user_id=user_id,
                        dtime=datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M'),
                        text=row[1],
                        t_id=row[2])
                    )
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return list


    def remove_target(self, target):
        sql = """UPDATE public."Target" SET is_deleted = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (target.id, target.user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id


    def remove_task(self, task):
        sql = """UPDATE public."Task" SET is_deleted = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (task.id, task.user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id


    def done_task(self, task):
        sql = """UPDATE public."Task" SET is_done = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (task.id, task.user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id

    def done_target(self, target):
        sql = """UPDATE public."Target" SET is_done = 1 WHERE id = %s AND user_t = %s RETURNING id"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (target.id, target.user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return id

    def change_time_zone(self, user_id, gmt):
        sql = """UPDATE public."User" SET gmt = %s WHERE user_id = %s;"""
        conn = None
        id = None
        try:
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (gmt, user_id,))
            id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_all_users(self):
        sql = """SELECT name, chat_id, user_id, gmt FROM public."User" """
        conn = None
        users = dict()
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                users[row[2]] = User(
                    name=row[0],
                    chat_id=row[1],
                    user_id=row[2],
                    gmt=row[3],
                )
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return users


    def get_recent_tasks(self, time):
        sql = """SELECT time, text, user_t, id FROM public."Task" WHERE time = %s AND is_deleted = 0 AND is_done = 0 ORDER BY TIME ASC"""
        conn = None
        list = []
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (time,))
            rows = cur.fetchall()
            for row in rows:
                list.append(Task(
                    dtime=datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M'),
                    text=row[1],
                    user_id=row[2],
                    t_id=row[3])
                )
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return list
