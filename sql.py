import sqlite3
from sqlite3 import Error


class Sql:
    def __init__(self, dir_path_base):
        self.con = sqlite3.connect(dir_path_base)
        self.cur = self.con.cursor()

    def table_exists(self, table_name):
        self.cur.execute(f"""SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{table_name}'""")
        if self.cur.fetchone()[0] == 1:
            return True
        return False

    def in_base(self, query):
        """передать в базу передав sql запрос"""
        self.cur.execute(query)
        self.con.commit()

    def out_base(self, query):
        """достать из базы передав sql запрос"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def inserter(self, values):
        rows = self.out_base(f"SELECT rowid, * FROM {values[0]}")
        for row in rows:
            if values[1] in row:
                break
        else:
            # # Добавление данных
            self.in_base(f'''INSERT INTO {values[0]} VALUES {tuple(values[1:])}''')

    def insert(self, values):
        try:
            self.in_base(f'''
                insert into {tuple(values.values())[0]}{tuple(values.keys())[1:]} values {tuple(values.values())[1:]}
                ''')
        except sqlite3.IntegrityError:
            print("ошибка primary key")
            print("наверно такая строка уже есть")
        # sqlite3.IntegrityError: UNIQUE constraint failed
