from finder import Finder


class Rostel(Finder):
    def __init__(self):
        self.query_create_table_rostelecom = '''CREATE TABLE IF NOT EXISTS rostelecom(
                        "Счет №" text,
                        "Счет за" text PRIMARY KEY,
                        "месяц" integer,
                        "год" integer,
                        "К оплате:" real,
                        "(+ переплата/- долг)" real,
                        "оплачено" real,
                        "Абонентская плата" real
                        )'''

    def find_rostelecom(self, ex_page, place):
        self.ex_page = ex_page
        val = {'table': 'rostelecom'}
        [val["Счет №"], place] = self.find(place, ex_page[0], 'Счет № ', ' ')
        val['Счет за'], place = self.find(place, ex_page[0], ' за ', 'У')
        val['месяц'] = val['Счет за'].split()[0]
        val['месяц'] = self.MONTH_DICT[val['месяц']]
        val['год'] = int(val['Счет за'].split()[1])
        val['К оплате:'], place = self.find(place, ex_page[0], 'ОПЛАТИТЬ\n', ' ', 3)
        val['оплачено'] = float(val['К оплате:'].translate({ord(i): None for i in ' руб'}))
        val['(+ переплата/- долг)'], place = self.find(place, ex_page[0], val['Счет за'].upper() + '\n', ' ')
        val['Абонентская плата'], place = self.find(place, ex_page[0], val['(+ переплата/- долг)'] + ' ', ' ')
        self.val = val
