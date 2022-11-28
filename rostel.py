from finder import Finder


class Rostel(Finder):
    def __init__(self):
        self.query_create_table_rostelekom_if_not_exists = '''CREATE TABLE IF NOT EXISTS rostelekom(
                                                            "Счет №" text,
                                                            "Счет за" text,
                                                            "месяц" integer,
                                                            "год" integer,
                                                            "К оплате:" real,
                                                            "(+ переплата/- долг)" real,
                                                            "Абонентская плата" real, 
                                                            CONSTRAINT date PRIMARY KEY ("год", "месяц")
                                                            )'''
        self.query_create_table_rostelekom_dict = '''CREATE TABLE IF NOT EXISTS rostelekom(
                                                            "Счет №" text,
                                                            "Счет за" text,
                                                            "месяц" integer,
                                                            "год" integer,
                                                            "К оплате:" real,
                                                            "(+ переплата/- долг)" real,
                                                            "оплачено" real,
                                                            "Абонентская плата" real, 
                                                            CONSTRAINT date PRIMARY KEY ("год", "месяц")
                                                            )'''

    # def find_rostelekom(self, ex_page, mesto):
    #     self.ex_page = ex_page
    #     val = ['rostelekom']
    #     # kod = re.search('Счет №\)?:? *((\d+((.|,)\d+)?)|х))')
    #     kod, mesto = self.find(mesto, ex_page[0], 'Счет № ', ' ')
    #     val.append(int(kod))
    #     period, mesto = self.find(mesto, ex_page[0], ' за ', 'У')
    #     val.append(period)
    #     month = period.split()[0]
    #     mm = self.MONTH_DICT[month]
    #     val.append(mm)
    #     year = period.split()[1]
    #     val.append(int(year))
    #     in_total_to_pay, mesto = self.find(mesto, ex_page[0], 'ОПЛАТИТЬ\n', ' ', 3)
    #     oplata = float(in_total_to_pay.translate({ord(i): None for i in ' руб'}))
    #     val.append(oplata)
    #     dolg_pereplata, mesto = self.find(mesto, ex_page[0], period.upper() + '\n', ' ')
    #     print(mesto)
    #     accrued, mesto = self.find(mesto, ex_page[0], dolg_pereplata + ' ', ' ')
    #     val.append(dolg_pereplata)
    #     val.append(accrued)
    #     self.val = val

    def find_rostelekom(self, ex_page, place):
        self.ex_page = ex_page
        val = {'table': 'rostelekom'}
        [val["Счет №"], place] = self.find(place, ex_page[0], 'Счет № ', ' ')
        val['Счет за'], place = self.find(place, ex_page[0], ' за ', 'У')
        val['месяц'] = val['Счет за'].split()[0]
        val['месяц'] = self.MONTH_DICT[val['месяц']]
        val['год'] = int(val['Счет за'].split()[1])
        val['К оплате:'], place = self.find(place, ex_page[0], 'ОПЛАТИТЬ\n', ' ', 3)
        val['оплачено'] = float(val['К оплате:'].translate({ord(i): None for i in ' руб'}))
        val['(+ переплата/- долг)'], place = self.find(place, ex_page[0], val['Счет за'].upper() + '\n', ' ')
        val['Абонентская плата'], place = self.find(place, ex_page[0], val['(+ переплата/- долг)'] + ' ', ' ')
        self.val_dict = val
