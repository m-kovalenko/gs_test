import json

import psycopg2

from src.constants import DB_CREDENTIALS

TODOS_TASKS_TABLE_NAME = 'todos_tasks'


class Database:

    def __init__(
            self,
            host=DB_CREDENTIALS['host'],
            db_name=DB_CREDENTIALS['db_name'],
            user=DB_CREDENTIALS['user'],
            password=DB_CREDENTIALS['password'],
    ):
        self.dsn = f'postgresql://{user}:{password}@{host}/{db_name}'

    def __enter__(self):
        self.conn = psycopg2.connect(dsn=self.dsn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    @staticmethod
    def _paginate(seq, page_size):
        page = []
        it = iter(seq)
        while True:
            try:
                for i in range(page_size):
                    page.append(next(it))
                yield page
                page = []
            except StopIteration:
                if page:
                    yield page
                return

    def execute_chunks(self, cur, sql, argslist, page_size=100):
        for page in self._paginate(argslist, page_size=page_size):
            sqls = [cur.mogrify(sql, args) for args in page]
            cur.execute(b";".join(sqls))

    def delete_tasks(self):
        sql = f"""delete from todos_tasks;"""
        with self.conn.cursor() as cur:
            cur.execute(sql)

    def insert_tasks(self, tasks: list[str]):
        args = [[t] for t in tasks]
        sql = f"""INSERT INTO 
            {TODOS_TASKS_TABLE_NAME} (task) 
            VALUES (%s)"""
        with self.conn.cursor() as cur:
            self.execute_chunks(cur, sql, args)

    def replace_tasks(self, tasks):
        self.delete_tasks()
        self.insert_tasks(tasks)

    def load_tasks(self):
        sql = f"""SELECT task from todos_tasks;"""
        with self.conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return [t[0] for t in rows]
