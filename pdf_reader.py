from PyPDF2 import PdfFileReader


class PdfReader:
    @staticmethod
    def reader(pdf_document):
        with open(pdf_document, 'rb') as filehandle:
            pdf = PdfFileReader(filehandle)
            pages = pdf.getNumPages()
            ex_page = []
            for i in range(pages):
                ex_page.append(pdf.getPage(i).extractText())
            print(ex_page[0])
        return ex_page


if __name__ == '__main__':
    text = r'D:\pythonProject\pdfProject\kvitki\rostelekom_202205[25].pdf'
    PdfReader.reader(text)
