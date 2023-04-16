import pdf_reader as pr


if __name__ == '__main__':
    text = r'D:\pythonProject\pdfProject\kvitki\rostelekom_202205[25].pdf'
    ex_page = pr.PdfReader.reader(text)

    with open('pdf.txt', 'w', encoding='utf-8') as file:
        file.write(ex_page[0])
