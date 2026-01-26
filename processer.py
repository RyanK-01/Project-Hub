import os
import json
import PyPDF2
import google.generativeai as genai
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
    
    '''Generate Script'''
    def generate_script(chunks):
        full_script = []
        previous_text = '' #Baton

        for i in range(chunks):

            #Prompt
            prompt = f'''
            ### ROLE
            You are a professional podcast producer. Your job is to convert study notes into a
            strictly structured JSON dialouge script. Assume that the listener has NO prior knowledge 
            of this topic, try to break down concepts into simpler chunks.

            ### CHARACTERS INVOLVED
            1. **Alex (Host): **A curious, energetic, asks clarifying questions kind of student.
            2. **John (Expert): **A calm, knowledgeable, uses everyday language and simple analogies to explain complex topics.

            ### INPUT DATA
            Here is the raw text to discuss: '{chunks}'

            ### CONTEXT (PREVIOUS CONVERSATION)
            The podcast is already in progess. Here is the last thing that was said: '{previous_text}'

            ### INSTRUCTIONS
            1. Continue the conversation naturally from the CONTEXT. (no 'Welcome back')
            2. If CONTEXT is empty, start with a catchy introduction.
            3. Explain the INPUT DATA clearly through dialouge. Keep iteractions short (2-3 sentence per turn).
            4. End the segment natuarlly, but do not say 'Goodbye' or 'In summary' unless the text explicitly ends.

            ### OUTPUT FORMAT (CRITICAL)
            Output ONLY valid JSON. Do not use Markdown.
            Follow this exact schema:
            [
                {{'speaker': 'Alex', 'text': 'Wait, so how does that work?'}}
                {{'speaker': 'John', 'text': 'Think of it like a battery...'}}           
            ]
            '''
        
            #Generate prompt with Gemini
            response = genai.generate(prompt)
            current_segment = json.loads(response)

            #Append it to the Script
            full_script.extend(current_segment)

            #Updating of Baton
            #Grab the last few items from current_segment to show the next iteration
            previous_text = str(current_segment[-3:])


if __name__ == '__main__':
    processor = TextProcessor()
    full_text = processor.extract_text_from_pdf('file-sample_150kB.pdf')
    chunks = processor.get_chunk(full_text)
    print(len(chunks), chunks[0])