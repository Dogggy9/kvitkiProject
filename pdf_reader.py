
from PyPDF2 import PdfFileReader

class PdfReader:
    def reader(self, pdf_document):
        # pdf_document = 'D:\pythonProject\pdfProject\ee_2022_1.pdf'
        with open(pdf_document, 'rb') as filehandle:
            pdf = PdfFileReader(filehandle)
            ex_page = []
            # info = pdf.getDocumentInfo()
            pages = pdf.getNumPages()
            for i in range(pages):
                ex_page.append(pdf.getPage(i).extractText())
            # print(info)
            # print(f'количество страниц {pages}')
            # page1 = pdf.getPage(0)
            # print("page1= ", page1)
            # extractText_page1 = page1.extractText()
            # print(len(extractText_page1))
            # print(extractText_page1.find('Энергоснабжение'))
            # k = 0
            # i =1
            # a1 = ''
            # while k != ' ':
            #     if k != 0:
            #         a1 = a1 + k
            #         i += 1
            #     print(k := extractText_page1[extractText_page1.find('Энергоснабжение') + len('Энергоснабжение') + i])
            # print(a1)
        return ex_page


if __name__ == '__main__':
    p = PdfReader()
    print(p.reader('D:\pythonProject\pdfProject\ee_2022_1.pdf'))
