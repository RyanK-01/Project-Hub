import os
import json
import PyPDF2
from file_loader import loader
from google import genai
from google.genai import types
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextProcessor:
    def __init__(self):
        
        #Load the local .env file
        load_dotenv()
        self.api_key = os.getenv('GEMINI_API_KEY')

        #Create new client
        self.client = genai.Client(api_key=self.api_key)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 50000,
            chunk_overlap = 1000,
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
    def generate_script(self, chunks):
        full_script = []
        previous_text = '' #Baton

        for chunk in chunks:

            #Prompt
            system_prompt = f'''
            ### ROLE
            You are a professional podcast producer. Your job is to convert study notes into a
            strictly structured JSON dialouge script. Assume that the listener has NO prior knowledge 
            of this topic, try to break down concepts into simpler chunks.

            ### CHARACTERS INVOLVED
            1. **Alex (Host): **A curious, energetic, asks clarifying questions kind of student.
            2. **John (Expert): **A calm, knowledgeable, uses everyday language and simple analogies to explain complex topics.

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

            user_prompt = f'''
            ### INPUT DATA
            Here is the raw text to discuss: '{chunk}'

            ### CONTEXT (PREVIOUS CONVERSATION)
            The podcast is already in progess. Here is the last thing that was said: '{previous_text}'
            '''

            # In your generation loop:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt # Pass rules here
                ),
                contents=user_prompt # Pass data here
            )
                        
            # Clean and parse JSON
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            try:
                current_segment = json.loads(clean_text)
                full_script.extend(current_segment)
                previous_text = str(current_segment[-3:])
            except json.JSONDecodeError:
                print(f"Error parsing JSON for chunk: {chunk[:50]}...")
        
        return full_script

if __name__ == '__main__':
    processor = TextProcessor()
    full_text = processor.extract_text_from_pdf('Adobe_sample.pdf')
    chunks = processor.get_chunk(full_text)
    
    test_script = processor.generate_script(chunks[:1])
    print(json.dumps(test_script, indent=2))