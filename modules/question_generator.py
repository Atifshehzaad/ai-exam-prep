import random
import re
from sentence_transformers import SentenceTransformer
import numpy as np

class QuestionGenerator:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def generate_questions(self, text, num_questions=10):
        """Generate various types of questions from text"""
        sentences = self._extract_important_sentences(text)
        questions = []
        
        question_templates = [
            "Explain the concept of {key_term} in your own words.",
            "What is the significance of {key_term}?",
            "How does {key_term} relate to other concepts in the text?",
            "Describe the process of {key_term}.",
            "What are the main characteristics of {key_term}?",
            "Compare and contrast {key_term} with similar concepts.",
            "What would happen if {key_term} was absent?",
            "How is {key_term} applied in real-world scenarios?"
        ]
        
        key_terms = self._extract_key_terms(text)
        
        for _ in range(num_questions):
            if key_terms:
                term = random.choice(key_terms)
                template = random.choice(question_templates)
                question = template.format(key_term=term)
                questions.append(question)
            else:
                # Fallback: use sentence-based questions
                if sentences:
                    sentence = random.choice(sentences)
                    question = f"Explain: {sentence}"
                    questions.append(question)
        
        return list(set(questions))[:num_questions]
    
    def generate_mcqs(self, text, num_questions=5):
        """Generate multiple choice questions"""
        key_terms = self._extract_key_terms(text)
        mcqs = []
        
        for term in key_terms[:num_questions]:
            question = f"What is {term}?"
            
            # Generate options (simplified - in production, use more sophisticated methods)
            correct = f"The main concept discussed in the text"
            incorrect_options = [
                "An unrelated concept",
                "A secondary topic mentioned briefly",
                "Not covered in the material",
                "A historical reference"
            ]
            
            options = [correct] + random.sample(incorrect_options, 3)
            random.shuffle(options)
            
            mcq = {
                'question': question,
                'a': options[0],
                'b': options[1],
                'c': options[2],
                'd': options[3],
                'correct': chr(97 + options.index(correct))  # 'a', 'b', etc.
            }
            mcqs.append(mcq)
        
        return mcqs
    
    def generate_summary(self, text, num_sentences=5):
        """Generate text summary"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= num_sentences:
            return " ".join(sentences)
        
        # Simple extraction-based summary (in production, use abstractive methods)
        embeddings = self.model.encode(sentences)
        doc_embedding = self.model.encode([text])
        
        similarities = []
        for sent_embedding in embeddings:
            similarity = np.dot(sent_embedding, doc_embedding[0]) / (
                np.linalg.norm(sent_embedding) * np.linalg.norm(doc_embedding[0])
            )
            similarities.append(similarity)
        
        top_indices = np.argsort(similarities)[-num_sentences:]
        top_sentences = [sentences[i] for i in sorted(top_indices)]
        
        return " ".join(top_sentences)
    
    def _extract_important_sentences(self, text):
        """Extract important sentences using embedding similarity"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= 10:
            return sentences
        
        embeddings = self.model.encode(sentences)
        doc_embedding = self.model.encode([text])
        
        similarities = []
        for sent_embedding in embeddings:
            similarity = np.dot(sent_embedding, doc_embedding[0]) / (
                np.linalg.norm(sent_embedding) * np.linalg.norm(doc_embedding[0])
            )
            similarities.append(similarity)
        
        top_indices = np.argsort(similarities)[-10:]
        return [sentences[i] for i in top_indices]
    
    def _extract_key_terms(self, text):
        """Extract key terms from text"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Simple frequency-based approach
        from collections import Counter
        common_words = set(['which', 'what', 'when', 'where', 'why', 'how', 'this', 'that', 'with', 'from'])
        filtered_words = [word for word in words if word not in common_words and len(word) > 3]
        
        term_freq = Counter(filtered_words)
        return [term for term, freq in term_freq.most_common(20)]