import os
import openai
from app.models import db, Covenant
import PyPDF2
from docx import Document as DocxDocument

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])

def process_document(file_path, document_id):
    # Extract text based on file type
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        text = extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        with open(file_path, 'r') as file:
            text = file.read()
    else:
        raise ValueError('Unsupported file type')

    # Process with OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a financial covenant extraction expert. 
                Analyze the provided document and extract financial covenants. For each covenant, identify:
                1. The covenant text
                2. Type of covenant
                3. Threshold value or requirement
                4. Any specific conditions or exceptions"""},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
        )

        # Parse OpenAI response and create Covenant objects
        covenants = []
        extracted_text = response.choices[0].message['content']
        
        # Simple parsing (in production, use more robust parsing)
        sections = extracted_text.split('\n\n')
        for section in sections:
            if not section.strip():
                continue
            
            covenant = Covenant(
                document_id=document_id,
                text=section,
                covenant_type='financial',  # Default type
                threshold_value='N/A',
                compliance_status='pending'
            )
            db.session.add(covenant)
            covenants.append(covenant)
        
        db.session.commit()
        return covenants
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error processing document: {str(e)}")
