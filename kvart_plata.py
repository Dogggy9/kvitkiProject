import pathlib

import pandas as pd

from electr import Electr
from finder import Finder
from hot import Hot
from pdf_reader import PdfReader
from rostel import Rostel
from sql import Sql

dir_path = pathlib.Path.cwd()
dir_path_base = pathlib.Path(dir_path, 'kvart_plata.db')
dir_path_files = pathlib.Path(dir_path, 'kvitki')

NUM_FLOAT = r'( *\d+((.|,)\d+)?)'
s = Sql(dir_path_base)
# p = PdfReader()
f = Finder()
e = Electr()
h = Hot()
r = Rostel()
finder = f.find

# удалить таблицу
if True:
    query_drop_table_electric = "DROP TABLE if exists electric"
    s.in_base(query_drop_table_electric)
    print("удаляем таблицу electric")
    query_drop_table_rostelecom = "DROP TABLE if exists rostelecom "
    s.in_base(query_drop_table_rostelecom)
    print("удаляем таблицу rostelecom")
    query_drop_table_tgk2 = "DROP TABLE if exists tgk2 "
    s.in_base(query_drop_table_tgk2)
    print("удаляем таблицу tgk2")

for path in dir_path_files.iterdir():
    print(path)
    if path.is_file():
        mesto = 0
        mesto2 = 0
        pdf_document = path
        ex_page = PdfReader.reader(pdf_document)
        if 'ТГК-2 ЭНЕРГОСБЫТ' in ex_page[0]:
            e.find_tgk2_energ(ex_page, mesto, mesto2)
            s.in_base(e.query_create_table_electric_if_not_exists)
            s.inserter(e.val)
            df_e = pd.read_sql(f"select * from {e.val[0]}", s.con)

        elif 'www.lk.rt.ru' in ex_page[0]:
            r.find_rostelecom(ex_page, mesto)
            s.in_base(r.query_create_table_rostelecom)
            s.insert(r.val)
            df_ros = pd.read_sql(f"select * from {tuple(r.val.values())[0]}", s.con)

        elif 'ПАО "ТГК № 2"' in ex_page[0]:
            h.find_tgk2_hot(ex_page, mesto)

            s.in_base(h.query_create_table_tgk2_if_not_exists)
            s.inserter(h.val)
            df_tgk = pd.read_sql(f"select * from {h.val[0]}", s.con)

        else:
            continue
