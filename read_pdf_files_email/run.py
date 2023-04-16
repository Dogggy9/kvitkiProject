from utils import read_credentails
from read_emails_scripts import get_unseen_emails, get_mail_attachments


if __name__ == '__main__':
    email_address, password = read_credentails()
    messages = get_unseen_emails(email_address, password)
    if messages:
        print(type(messages))

        for message in messages:
            attachments = get_mail_attachments(message, lambda x: x.endswith('.pdf'))
            for attachment in attachments:
                if attachment:
                    with open(f'./data/pdf_files/{attachment[0]}', 'wb') as file:
                        file.write(attachment[1])
