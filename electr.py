from finder import Finder


class Electr(Finder):
    def __init__(self):
        self.query_create_table_electric_if_not_exists = '''CREATE TABLE IF NOT EXISTS electric(
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

    def find_tgk2_energ(self, ex_page, mesto, mesto2):
        val = ['electric', ]
        kod, mesto = self.find(mesto, ex_page[0], 'Код: ', ' ')
        val.append(int(kod))
        period, mesto = self.find(mesto, ex_page[0], 'Ананьин В.А. ', ' ', 2)
        val.append(period)
        month = self.MONTH_DICT[period.split()[0]]
        val.append(month)
        year = int(period.split()[1])
        val.append(year)
        in_total_to_pay, mesto = self.find(mesto, ex_page[0], 'Всего к оплате: ', ' ')
        val.append(float(in_total_to_pay.replace(",", ".")))
        dolg, mesto = self.find(mesto, ex_page[0], 'Энергоснабжение ', ' ')
        accrued, mesto = self.find(mesto, ex_page[0], dolg + ' ', ' ')
        val.append(float(dolg.replace(",", ".")))
        paid, mesto = self.find(mesto, ex_page[0], accrued + ' ', ' ')
        val.append(float(accrued.replace(",", ".")))
        total_for_payment, mesto = self.find(mesto, ex_page[0], paid + ' ', '\n')
        val.append(float(paid.replace(",", ".")))
        val.append(float(total_for_payment.replace(",", ".")))
        nomer_pribora_noch, mesto2 = self.find(mesto2, ex_page[1], 'Сутки ', ' ')
        start_noch, mesto2 = self.find(mesto2, ex_page[1], nomer_pribora_noch + ' ', ' ')
        val.append(int(nomer_pribora_noch))
        end_noch, mesto2 = self.find(mesto2, ex_page[1], start_noch + ' ', ' ')
        val.append(float(start_noch.replace(",", ".")))
        schet_noch, mesto2 = self.find(mesto2, ex_page[1], end_noch + ' ', ' ')
        val.append(float(end_noch.replace(",", ".")))
        tarif_noch, mesto2 = self.find(mesto2, ex_page[1], schet_noch + ' ', ' ')
        val.append(float(schet_noch.replace(",", ".")))
        pay_noch, mesto2 = self.find(mesto2, ex_page[1], tarif_noch + ' ', ' ')
        val.append(float(tarif_noch.replace(",", ".")))
        val.append(float(pay_noch.replace(",", ".")))
        nomer_pribora_den, mesto2 = self.find(mesto2, ex_page[1], 'Сутки ', ' ')
        val.append(int(nomer_pribora_den))
        start_den, mesto2 = self.find(mesto2, ex_page[1], nomer_pribora_den + ' ', ' ')
        end_den, mesto2 = self.find(mesto2, ex_page[1], start_den + ' ', ' ')
        val.append(float(start_den.replace(",", ".")))
        schet_den, mesto2 = self.find(mesto2, ex_page[1], end_den + ' ', ' ')
        val.append(float(end_den.replace(",", ".")))
        tarif_den, mesto2 = self.find(mesto2, ex_page[1], schet_den + ' ', ' ')
        val.append(float(schet_den.replace(",", ".")))
        pay_den, mesto2 = self.find(mesto2, ex_page[1], tarif_den + ' ', ' ')
        val.append(float(tarif_den.replace(",", ".")))
        val.append(float(pay_den.replace(",", ".")))
        self.val = val
