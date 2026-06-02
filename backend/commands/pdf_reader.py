import os
from pypdf import PdfReader
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

def extract_pdf_text(pdf_path: str) -> str:
    full_path = os.path.abspath(os.path.expanduser(pdf_path))
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"PDF file not found at: {full_path}")
        
    try:
        reader = PdfReader(full_path)
        text_content = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_content.append(text)
                
        return "\n".join(text_content).strip()
    except Exception as e:
        logger.error(f"Error reading PDF content: {e}")
        raise e

def read_pdf(pdf_path: str) -> dict:
    try:
        text = extract_pdf_text(pdf_path)
        if not text:
            return format_response(False, "PDF file appears to be empty or contains scanned images only.")
            
        # Return first 600 characters as preview text
        preview = text[:600] + "..." if len(text) > 600 else text
        return format_response(True, f"PDF read complete. Content preview: {preview}", {"text": text})
    except Exception as e:
        return format_response(False, f"Failed to read PDF file: {str(e)}")

def summarize_pdf(pdf_path: str, assistant_router) -> dict:
    try:
        text = extract_pdf_text(pdf_path)
        if not text:
            return format_response(False, "PDF content is empty, cannot generate summary.")
            
        # Slice text to prevent token overflows (~2500 words limit for prompt)
        max_chars = 10000
        truncated_text = text[:max_chars]
        
        prompt = f"Please provide a concise, high-level summary of the following PDF document content:\n\n{truncated_text}\n\nSummary:"
        logger.info(f"Summarizing PDF content using default AI client...")
        summary = assistant_router.query_assistant(prompt)
        
        return format_response(True, f"PDF Summary: {summary}", {"summary": summary})
    except Exception as e:
        logger.error(f"Error summarizing PDF: {e}")
        return format_response(False, f"Failed to summarize PDF: {str(e)}")
