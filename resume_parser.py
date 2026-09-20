from pypdf import PdfReader
from docx import Document

def extract_text(filepath):

   if filepath.lower().endswith(".txt"):

      with open(filepath, "r", encoding="utf-8") as file:
         return file.read()
     
   elif filepath.lower().endswith(".pdf"):

      reader = PdfReader(filepath)

      text = ""

      for page in reader.pages:
         text += page.extract_text() or ""

      return text
      
   elif filepath.lower().endswith(".docx"):

      document = Document(filepath)   

      text = ""

      for paragraph in document.paragraphs:
          text += paragraph.text + "\n"

      return text

    
   else:
        return ""