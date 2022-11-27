class Finder:
    MONTH_DICT = {'январь': 1, "февраль": 2, "март": 3, "апрель": 4, "май": 5, "июнь": 6,
                  "июль": 7, "август": 8, "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12}
    val = None

    @staticmethod
    def find(place: int, text: str, slovo: str, stop: str, stop_pos=1):
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

