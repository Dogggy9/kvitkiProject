from email import message_from_bytes
from imaplib import IMAP4_SSL


def get_unseen_emails(email_address, password):
    """
    Отфильтруйте электронное письмо и верните невидимые электронные письма
    Args:
        :param email_address: Электронная почта получателя
        :param password: пароль получателя
    :return:
    """
    with IMAP4_SSL("imap.gmail.com") as mail_connection:
        mail_connection.login(email_address, password)
        print(mail_connection.list())
        mail_connection.select("inbox")
        retcode, messages = mail_connection.search(None, '(OR (UNSEEN) (FROM dogggy9@gmail.com))')
        print(len(messages[0]))
        if retcode == 'OK' and messages[0]:
            for index, num in enumerate(messages[0].split()):
                print(index, num)
                typ, data = mail_connection.fetch(num, '(rfc822)')
                message = message_from_bytes(data[0][1])
                typ, data = mail_connection.store(num, '+FLAGS', '\\Seen')
                yield message

def get_mail_attachments(message: message_from_bytes, condition_check):
    """
    Получить файлы вложений по почте
    :param message: объект электронной почты для получения вложения из
    :param condition_check: функция для использования при фильтрации
    Электронная почта должна вернуть конкретное состояние, которое мы фильтруем
    :return: [fileName, файл]: имя файла, поток ввода из файлов
    """
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if not part.get('Content-Disposition'):
            continue
        file_name = part.get_filename()
        if condition_check(file_name):
            yield part.get_filename(), part.get_payload(decode=1)
