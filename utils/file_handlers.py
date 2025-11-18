import PyPDF2
import docx
import re
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    def extract_text(self, file_path):
        """Extract text from various file formats with enhanced error handling"""
        try:
            if file_path.endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._extract_from_docx(file_path)
            elif file_path.endswith('.txt'):
                return self._extract_from_txt(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return None
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF file with enhanced error handling"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if reader.is_encrypted:
                    logger.warning("PDF is encrypted, trying to decrypt")
                    try:
                        reader.decrypt('')  # Try empty password
                    except:
                        logger.error("Could not decrypt PDF")
                        return None
                
                text = ""
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        else:
                            logger.warning(f"No text found on page {page_num + 1}")
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
                
                if not text.strip():
                    logger.error("No text could be extracted from PDF")
                    return None
                    
                return text
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            return None
    
    def _extract_from_docx(self, file_path):
        """Extract text from DOCX file with enhanced error handling"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    text += paragraph.text + "\n"
            
            if not text.strip():
                logger.error("No text found in DOCX file")
                return None
                
            return text
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path}: {e}")
            return None
    
    def _extract_from_txt(self, file_path):
        """Extract text from TXT file with enhanced error handling"""
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
                    if text.strip():
                        return text
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading TXT with encoding {encoding}: {e}")
                continue
        
        logger.error(f"Could not read TXT file with any encoding: {file_path}")
        return None
    
    def validate_file(self, file_path, max_size_mb=10):
        """Validate file before processing"""
        import os
        
        try:
            # Check file size
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > max_size_mb:
                logger.error(f"File too large: {file_size:.2f}MB")
                return False, f"File too large. Maximum size is {max_size_mb}MB"
            
            # Check if file is readable
            if not os.access(file_path, os.R_OK):
                logger.error(f"File not readable: {file_path}")
                return False, "File is not readable"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file: {e}")
            return False, f"Error validating file: {str(e)}"
