import os
import PyPDF2
from docx import Document

def detect_file_type(file_name):
    ext = os.path.splitext(file_name)
    if ext == '.docx':
        return WordLoader.loader(file_name)
    elif ext == '.txt':
        return TxtLoader.loader(file_name)
    else:
        return detect_pdf_type(file_name)
     
def detect_pdf_type(pdf):
    with open(pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        page = reader.pages[0]
        w_pdf = page.mediaBox.width
        h_pdf = page.mediaBox.height

        #Check if document is a slide or document
        if w_pdf > h_pdf: #it is a slide pdf
            return WpdfLoader.loader(pdf)
        else:
            return HpdfLoader.loader(pdf)

class BaseLoader():
    def loader(self, file_path):
        raise NotImplementedError # Must override this in subclasses

class WordLoader(BaseLoader):
    def loader(self, file_path):
        
        #Does not have page number, word docs work like a scroll
        pass

class TxtLoader(BaseLoader):
    def loader(self, file_path):
     pass

class WpdfLoader(BaseLoader):
    def loader(self, pdf_path):
     pass

class HpdfLoader(BaseLoader):
    def loader(self, pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            last_seen_title =''
            full_text = ''
            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                full_text += 'Page' + str(index) + '\n' + text +'\n\n'

        print(full_text)
        return full_text