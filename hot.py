from finder import Finder


class Hot(Finder):
    def __init__(self):
        self.query_create_table_tgk2_if_not_exists = '''CREATE TABLE IF NOT EXISTS tgk2(
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

    def find_tgk2_hot(self, ex_page, mesto: int):
        val = ['tgk2']
        total_area, mesto = self.find(mesto, ex_page[0], 'Общая площадь всех жилых и нежилых помещений: ', ' ')
        val.append(total_area)
        common_property, mesto = self.find(mesto, ex_page[0],
                                           'Площадь помещений, входящих в состав общего имущества дома: ', ' ')
        val.append(common_property)
        houseroom, mesto = self.find(mesto, ex_page[0], 'Общая площадь жилого помещения: ', ' ')
        val.append(houseroom)
        living_house, mesto = self.find(mesto, ex_page[0], 'Количество проживающих в доме: ', ' ')
        val.append(living_house)
        calculation_on, mesto = self.find(mesto, ex_page[0], 'Расчет выполнен на: ', ' ')
        val.append(calculation_on)
        kod, mesto = self.find(mesto, ex_page[0], 'Извещение № ', ' ')
        val.insert(1, kod)
        account, mesto = self.find(mesto, ex_page[0], 'Отопление ГВС Л/с', ' ')
        val.append(account)
        component_total, mesto = self.find(mesto, ex_page[0], 'компонент на \nтеплоноситель', ' ')
        val.append(component_total)
        heating_total, mesto = self.find(mesto, ex_page[0], component_total + ' ', ' ')
        val.append(heating_total if heating_total.isdigit() else 0)
        gvs_total, mesto = self.find(mesto, ex_page[0], heating_total + ' ', 'Г')
        val.append(gvs_total)
        component_coolant, mesto = self.find(mesto, ex_page[0], 'Горячая вода (компонент на теплоноситель) ', ' ')
        val.append(heating_total if component_coolant.isdigit() else 0)
        heating_total, mesto = self.find(mesto, ex_page[0], component_coolant + ' ', ' ')
        val.append(heating_total if heating_total.isdigit() else 0)
        gvs_total, mesto = self.find(mesto, ex_page[0], heating_total + ' ', ' ')
        val.append(gvs_total)
        print(val)
        period, mesto = self.find(mesto, ex_page[0], 'водоснабжение за ', ' ', 2)
        val.insert(2, period)
        print(period)
        month = period.split()[0]
        print(month)
        mm = self.MONTH_DICT[month.lower()]
        val.insert(3, mm)
        year = period.split()[1]
        val.insert(4, int(year))
        self.val = val
