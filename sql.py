import sqlite3


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
