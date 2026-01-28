import os
import PyPDF2
from docx import Document

def detect_file_type(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    if ext == '.docx':
        return WordLoader.loader(file_name)
    elif ext == '.txt':
        return TxtLoader.loader(file_name)
    else:
        return detect_pdf_type(file_name)
     
def detect_pdf_type(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        page = reader.pages[0]
        w_pdf = float(page.mediabox.width)
        h_pdf = float(page.mediabox.height)

        #Check if document is a slide or document
        if w_pdf > h_pdf: #it is a slide pdf
            return WpdfLoader().loader(pdf_path)
        else:
            return HpdfLoader().loader(pdf_path)

class BaseLoader():
    def loader(self, file_path):
        raise NotImplementedError # Must override this in subclasses

#Does not have page number, word docs work like a scroll
class WordLoader(BaseLoader):
    def loader(self, file_path):
        
        #Open docx
        docx = Document(file_path)
        all_text = ''
        
        #Paragraph loops
        for para in docx.paragraphs:
            text = para.text
            if text.strip(): #(Optional Clean-up) Only add it if its not empty
                all_text.append(text)

        #Join them all together with "Enter" keys
        full_text = '\n'.join(all_text)

        #Return the standard format
        return [{'text': full_text}]

class TxtLoader(BaseLoader):
    def loader(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        return [{'page': 'Full page', 'text': content}]

class WpdfLoader(BaseLoader):
    def loader(self, pdf_path):
        pages = []
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            last_seen_title = ''
            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue  # skip pages with no text
                lines = text.split('\n')
                current_title = lines[0].strip() if lines else ''
                if last_seen_title == current_title and len(lines) > 1:
                    clean_text = '\n'.join(lines[1:])
                    page_text = clean_text
                else:
                    page_text = text
                    last_seen_title = current_title
                pages.append({'page': f'Page{index}', 'text': page_text})
        return pages

class HpdfLoader(BaseLoader):
    def loader(self, pdf_path):
        pages = []
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            last_seen_title = ''
            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue  # skip pages with no text
                lines = text.split('\n')
                current_title = lines[0].strip() if lines else ''
                if last_seen_title == current_title and len(lines) > 1:
                    clean_text = '\n'.join(lines[1:])
                    page_text = clean_text
                else:
                    page_text = text
                    last_seen_title = current_title
                pages.append({'page': f'Page{index}', 'text': page_text})
        return pages