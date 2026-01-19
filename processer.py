import os
#import json
import PyPDF2
# import google.generativeai as genai
#from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextProcessor:
    def __init__(self):
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 2000,
            chunk_overlap = 20,
            length_function = len
        )

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            last_seen_title =''
            full_text = ''
            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                full_text += 'Page' + str(index) + '\n' + text +'\n\n'

        print(full_text)
        return full_text

    '''Break down large chunck of text to smaller ones'''
    def get_chunk(self, full_text):
        chunk = self.text_splitter.split_text(full_text)
        return chunk


if __name__ == '__main__':
    processor = TextProcessor()
    full_text = processor.extract_text_from_pdf('file-sample_150kB.pdf')
    chunks = processor.get_chunk(full_text)
    print(len(chunks), chunks[0])