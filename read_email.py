import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re

# пароль
mail_pass = "hlrbsnkstsjemdqi"
# почта
username = "Dogggy9@gmail.com"
imap_server = "imap.gmail.com"
imap = imaplib.IMAP4_SSL(imap_server)
# соединение с ответом ('OK', [b'Authentication successful'])
print(imap.login(username, mail_pass))
# какие есть папки ('OK', [b'(\\Inbox) "/" "INBOX"', b'() "/" "Junk"', b'() "/" "Unwanted"', b'(\\Spam) "/" "&BCEEPwQwBDw-"', b'(\\Sent) "/" "&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"', b'(\\Drafts) "/" "&BCcENQRABD0EPgQyBDgEOgQ4-"', b'(\\Trash) "/" "&BBoEPgRABDcEOAQ9BDA-"'])
print(imap.list())
# Чтобы добраться до письма нужно буквально открыть папку и в неё зайти, выполняется так:
# Возвращает примерно такой кортеж ('OK', [b'19']), первое, это статус операции, второе - количество писем в папке.
imap.select("inbox")
# Письма расположены в ящике по порядку номеров. Если выполнить поиск без каких-либо параметров, получим список номеров писем.
imap.search(None, 'ALL')
# Поиск можно осуществлять и более предметно: аргумент "UNSEEN" вернёт, все номера непросмотренных писем:
imap.search(None, "UNSEEN")
# можно получить их UID, неизменяемый номер
imap.uid('search', "UNSEEN", "ALL")
# Зная номер письма теперь его можно наконец-то получить.
res, msg = imap.fetch(b'19', '(RFC822)')  #Для метода search по порядковому номеру письма
res, msg = imap.uid('fetch', b'28', '(RFC822)')  #Для метода uid
# Извлекаем письмо при помощи метода message_from_bytes библиотеки email :
msg = email.message_from_bytes(msg[0][1])
# Тип объекта msg будет email.messages.Message. Непосредственно из него, не заглядывая внутрь можно извлечь почти всё кроме текста письма и вложений (текст иногда тоже можно извлечь).
letter_date = email.utils.parsedate_tz(msg["Date"]) # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
letter_id = msg["Message-ID"] #айди письма
letter_from = msg["Return-path"] # e-mail отправителя
msg["Subject"] # тема письма написана кириллицей и закодирована в base64
#   можно воспользоваться методом decode_header, который импортируем из email.header:
decode_header(msg["Subject"])
#  перевести символы в читаемый текст:
decode_header(msg["Subject"])[0][0].decode()
#  Если темы письма нет, msg["Subject"] вернет NoneType.
#  получить тему письма можно так:
imap.fetch(b'19', "(BODY[HEADER.FIELDS (Subject)])")  # не сработал
#  Чтобы продолжить нам нужно получить из объекта email.message.Message его полезную нагрузку, методом msg.get_payload()
"""И как нам любезно сообщает документация к библиотеке email результат может быть:
1. простым текстовым сообщением,
2. двоичным объектом,
3. структурированной последовательностью подсообщений, каждое из которых имеет собственный набор заголовков и собственный payload.
   """
msg.is_multipart()
"""
Пойдём по-порядку. Если мы получили простое текстовое сообщение... Нет, оно конечно-же никакое не простое, а 
закодированное в base64, но тут вроде всё просто, берем и декодируем и… можем получить, например, HTML-код, который 
уже почти читается, но тоже его лучше почистить (поэтому и BeautifulSoup в библиотеках).

Двоичный объект переводим в текстовый, и тут делаем тоже что и в первом случае.
"""
#  Если полученный объект состоит из группы других объектов начинаем итерировать.
payload=msg.get_payload()
for part in payload:
    print(part.get_content_type())

#  Но тут есть подвох, полученные части тоже могут составными, т.е. циклы нужно усложнять. Сильно упрощает этот вопрос метод walk
for part in msg.walk():
    print(part.get_content_type())

#  Если тоже самое исполнить стандартным способом получиться примерной такой код:
payload=msg.get_payload()
for part in payload:
    print(part.get_content_type())
    if part.is_multipart():
        level=part.get_payload()
        for l_part in level:
            print(l_part.get_content_type())

#  Нас интересует текст, поэтому проходимся по payload с условием part.get_content_maintype() == 'text'
for part in msg.walk():
    if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
        print(base64.b64decode(part.get_payload()).decode())

#  Вложения ловятся в частях письма также как и текст, по условию get_content_disposition() == 'attachment'.
"""
get_content_type() сообщит нам тип вложения (/ "image" / "audio" / "video" / "application" /) и более конкретную 
разновидность его, например application/pdf. Также в заголовке содержится и название файла. Если название не 
латиницей, то добро пожаловать в MIME + Base64.
"""
for part in msg.walk():
    print(part.get_content_disposition() == 'attachment')





