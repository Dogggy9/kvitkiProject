import os
from dotenv import load_dotenv

def read_credentails():
    """
    Вернуть учетные данные пользователя из файла переменных среды и
    Поднимите исключение, если учетные данные не присутствуют

    Raises:
        NotimplementError: [Описание]
    :return:
    """
    load_dotenv("sample.env")

    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASS = os.getenv("USER_PASS")
    if USER_EMAIL and USER_PASS:
        print(USER_PASS, USER_EMAIL)
        return USER_EMAIL, USER_PASS
    else:
        raise ValueError("Пожалуйста, добавьте файл sample.env и напишите учетные данные, он его, Обратитесь к образцу")


if __name__ == '__main__':
    read_credentails()

