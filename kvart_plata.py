import re
from sql import Sql
import sys
import pandas as pd
from PyPDF2 import PdfFileReader
from pdf_reader import PdfReader
import pathlib

dir_path = pathlib.Path.cwd()
dir_path_base = pathlib.Path(dir_path, 'kvart_plata.db')
dir_path_files = pathlib.Path(dir_path, 'kvitki')
MONTH_DICT = {'январь': 1, "февраль": 2, "март": 3, "апрель": 4, "май": 5, "июнь": 6,
              "июль": 7, "август": 8, "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12}
NUM_FLOAT = r'( *\d+((.|,)\d+)?)'
s = Sql(dir_path_base)
p = PdfReader()


def finder(place: int, text: str, slovo: str, stop: str, stop_pos=1):
    """
    :param place: позиция поиска
    :param text: текст в котором ищем
    :param slovo: слово от которого отталкиваемся
    :param stop: символ по которому останавливаемся
    :param stop_pos: если надо не по первому символу
    :return: искомые слова или цифры
    """
    x = 0
    next_simbol = 0
    iskomoe = ''
    while x != stop:
        while stop_pos != 0:
            if x != 0:
                iskomoe = iskomoe + x
                next_simbol += 1
            x = text[text.find(slovo, place) + len(slovo) + next_simbol]
            if x == stop:
                stop_pos -= 1

        return iskomoe, text.find(slovo, place)



# удалить таблицу
query_drop_table_electric = "DROP TABLE if exists electric"
s.in_base(query_drop_table_electric)
query_drop_table_rostelekom = "DROP TABLE if exists rostelekom "
s.in_base(query_drop_table_rostelekom)
query_drop_table_tgk2 = "DROP TABLE if exists tgk2 "
s.in_base(query_drop_table_tgk2)

for path in dir_path_files.iterdir():
    print(path)
    if path.is_file():
        mesto = 0
        mesto2 = 0
        pdf_document = path
        p.reader(pdf_document)
        with open(pdf_document, 'rb') as filehandle:
            pdf = PdfFileReader(filehandle)
            # info = pdf.getDocumentInfo()
            pages = pdf.getNumPages()  # количество страниц
            # print(pages)
            ex_page = []
            # values = []
            for i in range(pages):
                print(i)
                ex_page.append(pdf.getPage(i).extractText())
            if 'ТГК-2 ЭНЕРГОСБЫТ' in ex_page[0]:
                val = ['electric', ]
                kod, mesto = finder(mesto, ex_page[0], 'Код: ', ' ')
                val.append(int(kod))
                period, mesto = finder(mesto, ex_page[0], 'Ананьин В.А. ', ' ', 2)
                val.append(period)
                month = MONTH_DICT[period.split()[0]]
                val.append(month)
                year = int(period.split()[1])
                val.append(year)
                in_total_to_pay, mesto = finder(mesto, ex_page[0], 'Всего к оплате: ', ' ')
                val.append(float(in_total_to_pay.replace(",", ".")))
                dolg, mesto = finder(mesto, ex_page[0], 'Энергоснабжение ', ' ')
                accrued, mesto = finder(mesto, ex_page[0], dolg + ' ', ' ')
                val.append(float(dolg.replace(",", ".")))
                paid, mesto = finder(mesto, ex_page[0], accrued + ' ', ' ')
                val.append(float(accrued.replace(",", ".")))
                total_for_payment, mesto = finder(mesto, ex_page[0], paid + ' ', '\n')
                val.append(float(paid.replace(",", ".")))
                val.append(float(total_for_payment.replace(",", ".")))
                nomer_pribora_noch, mesto2 = finder(mesto2, ex_page[1], 'Сутки ', ' ')
                start_noch, mesto2 = finder(mesto2, ex_page[1], nomer_pribora_noch + ' ', ' ')
                val.append(int(nomer_pribora_noch))
                end_noch, mesto2 = finder(mesto2, ex_page[1], start_noch + ' ', ' ')
                val.append(float(start_noch.replace(",", ".")))
                schet_noch, mesto2 = finder(mesto2, ex_page[1], end_noch + ' ', ' ')
                val.append(float(end_noch.replace(",", ".")))
                tarif_noch, mesto2 = finder(mesto2, ex_page[1], schet_noch + ' ', ' ')
                val.append(float(schet_noch.replace(",", ".")))
                pay_noch, mesto2 = finder(mesto2, ex_page[1], tarif_noch + ' ', ' ')
                val.append(float(tarif_noch.replace(",", ".")))
                val.append(float(pay_noch.replace(",", ".")))
                nomer_pribora_den, mesto2 = finder(mesto2, ex_page[1], 'Сутки ', ' ')
                val.append(int(nomer_pribora_den))
                start_den, mesto2 = finder(mesto2, ex_page[1], nomer_pribora_den + ' ', ' ')
                end_den, mesto2 = finder(mesto2, ex_page[1], start_den + ' ', ' ')
                val.append(float(start_den.replace(",", ".")))
                schet_den, mesto2 = finder(mesto2, ex_page[1], end_den + ' ', ' ')
                val.append(float(end_den.replace(",", ".")))
                tarif_den, mesto2 = finder(mesto2, ex_page[1], schet_den + ' ', ' ')
                val.append(float(schet_den.replace(",", ".")))
                pay_den, mesto2 = finder(mesto2, ex_page[1], tarif_den + ' ', ' ')
                val.append(float(tarif_den.replace(",", ".")))
                val.append(float(pay_den.replace(",", ".")))

                # создать таблицу если не создана
                print('создаем таблицу electric если не создана')
                query_create_table_electric_if_not_exists = '''CREATE TABLE IF NOT EXISTS electric(
                                                        "код" integer,
                                                        "за период" text,
                                                        "месяц" integer,
                                                        "год" integer,
                                                        "Всего к оплате" real,
                                                        "Задолженность" real,
                                                        "Начислено" real,
                                                        "Оплачено" real,
                                                        "Итого к оплате, ₽" real,
                                                        "№ ПУ ночь" integer,
                                                        "Начальные ночь" real,
                                                        "Конечные ночь" real,
                                                        "Расход ночь, кВт*ч" real,
                                                        "Тариф ночь, ₽" real,
                                                        "Сумма ночь, ₽" real,
                                                        "№ ПУ день" integer,
                                                        "Начальные день" real,
                                                        "Конечные день" real,
                                                        "Расход день, кВт*ч" real,
                                                        "Тариф день, ₽" real,
                                                        "Сумма день, ₽" real
                                                        )'''
                s.in_base(query_create_table_electric_if_not_exists)
                s.inserter(val)
                df_e = pd.read_sql(f"select * from {val[0]}", s.con)

            elif 'www.lk.rt.ru' in ex_page[0]:
                val = ['rostelekom']
                # kod = re.search('Счет №\)?:? *((\d+((.|,)\d+)?)|х))')
                kod, mesto = finder(mesto, ex_page[0], 'Счет № ', ' ')
                val.append(int(kod))
                period, mesto = finder(mesto, ex_page[0], ' за ', 'У')
                val.append(period)
                month = period.split()[0]
                mm = MONTH_DICT[month]
                val.append(mm)
                year = period.split()[1]
                val.append(int(year))
                in_total_to_pay, mesto = finder(mesto, ex_page[0], 'ОПЛАТИТЬ\n', ' ', 3)
                oplata = float(in_total_to_pay.translate({ord(i): None for i in ' руб'}))
                val.append(oplata)
                dolg_pereplata, mesto = finder(mesto, ex_page[0], period.upper() + '\n', ' ')
                print(mesto)
                accrued, mesto = finder(mesto, ex_page[0], dolg_pereplata + ' ', ' ')
                val.append(dolg_pereplata)
                val.append(accrued)

                # создать таблицу если не создана
                print('создаем таблицу rostelekom если не создана')
                query_create_table_rostelekom_if_not_exists = '''CREATE TABLE IF NOT EXISTS rostelekom(
                                        "Счет №" integer,
                                        "Счет за" text,
                                        "месяц" integer,
                                        "год" integer,
                                        "К оплате:" real,
                                        "(+ переплата/- долг)" real,
                                        "Абонентская плата" real
                                    )'''
                s.in_base(query_create_table_rostelekom_if_not_exists)
                s.inserter(val)
                df_ros = pd.read_sql(f"select * from {val[0]}", s.con)

            elif 'ПАО "ТГК № 2"' in ex_page[0]:
                val = ['tgk2']
                total_area, mesto = finder(mesto, ex_page[0], 'Общая площадь всех жилых и нежилых помещений: ', ' ')
                val.append(total_area)
                common_property, mesto = finder(mesto, ex_page[0],
                                                'Площадь помещений, входящих в состав общего имущества дома: ', ' ')
                val.append(common_property)
                houseroom, mesto = finder(mesto, ex_page[0], 'Общая площадь жилого помещения: ', ' ')
                val.append(houseroom)
                living_house, mesto = finder(mesto, ex_page[0], 'Количество проживающих в доме: ', ' ')
                val.append(living_house)
                calculation_on, mesto = finder(mesto, ex_page[0], 'Расчет выполнен на: ', ' ')
                val.append(calculation_on)
                kod, mesto = finder(mesto, ex_page[0], 'Извещение № ', ' ')
                val.insert(1, kod)
                account, mesto = finder(mesto, ex_page[0], 'Отопление ГВС Л/с', ' ')
                val.append(account)
                component_total, mesto = finder(mesto, ex_page[0], 'компонент на \nтеплоноситель', ' ')
                val.append(component_total)
                heating_total, mesto = finder(mesto, ex_page[0], component_total + ' ', ' ')
                val.append(heating_total if heating_total.isdigit() else 0)
                gvs_total, mesto = finder(mesto, ex_page[0], heating_total + ' ', 'Г')
                val.append(gvs_total)
                component_coolant, mesto = finder(mesto, ex_page[0], 'Горячая вода (компонент на теплоноситель) ', ' ')
                val.append(heating_total if component_coolant.isdigit() else 0)
                heating_total, mesto = finder(mesto, ex_page[0], component_coolant + ' ', ' ')
                val.append(heating_total if heating_total.isdigit() else 0)
                gvs_total, mesto = finder(mesto, ex_page[0], heating_total + ' ', ' ')
                val.append(gvs_total)
                period, mesto = finder(mesto, ex_page[0], 'водоснабжение за ', ' ', 2)
                val.insert(2, period)
                month = period.split()[0]
                mm = MONTH_DICT[month.lower()]
                val.insert(3, mm)
                year = period.split()[1]
                val.insert(4, int(year))

                # создать таблицу если не создана
                print('создаем таблицу tgk2 если не создана')
                query_create_table_tgk2_if_not_exists = '''CREATE TABLE IF NOT EXISTS tgk2(
                                                        "Извещение №" text,
                                                        "Счет за" text,
                                                        "месяц" integer,
                                                        "год" integer,
                                                        "Общая площадь дома:" real,
                                                        "Общая площадь имущества" real,
                                                        "Общая площадь жилого помещения" real,
                                                        "Проживающих в доме" integer,
                                                        "Расчет выполнен на" integer,
                                                        "лицевой счет" integer,
                                                        "компонент на теплоноситель общее" real,
                                                        "отопление общее" real,
                                                        "горячая вода общее" real,
                                                        "компонент на теплоноситель" real,
                                                        "отопление" real,
                                                        "горячая вода" real
                                                        )'''
                s.in_base(query_create_table_tgk2_if_not_exists)
                s.inserter(val)
                df_tgk = pd.read_sql(f"select * from {val[0]}", s.con)
                # rows = out_base(f"SELECT rowid, * FROM {values[0]}")
                # # Проверяем не заносили ли мы уже этот файл
                # for row in rows:
                #     if int(values[1]) in row:
                #         break
                # # Если не заносили, добавляем данные
                # else:
                #     in_base(f'''INSERT INTO {values[0]} VALUES {tuple(values[1:])}''')
                #     df_r = pd.read_sql(f"select * from {values[0]}", con)
