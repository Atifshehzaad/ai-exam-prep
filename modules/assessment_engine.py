from sentence_transformers import SentenceTransformer, util
import numpy as np
import re

class AssessmentEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def evaluate_answer(self, question, student_answer, model_answer=None):
        """Evaluate student answer against question"""
        if not student_answer.strip():
            return {
                'score': 0,
                'feedback': "No answer provided.",
                'strengths': [],
                'improvements': ["Please provide a complete answer."]
            }
        
        # Calculate similarity with question (to check relevance)
        question_embedding = self.model.encode([question])
        answer_embedding = self.model.encode([student_answer])
        
        relevance_score = util.cos_sim(question_embedding, answer_embedding).item()
        
        # Analyze answer quality
        quality_metrics = self._analyze_answer_quality(student_answer)
        
        # Calculate overall score
        base_score = min(quality_metrics['completeness'] * 10, 8)
        relevance_bonus = min(relevance_score * 2, 2)
        
        final_score = min(base_score + relevance_bonus, 10)
        
        # Generate feedback
        feedback = self._generate_feedback(quality_metrics, relevance_score, final_score)
        
        return {
            'score': round(final_score, 1),
            'feedback': feedback,
            'strengths': quality_metrics['strengths'],
            'improvements': quality_metrics['improvements']
        }
    
    def _analyze_answer_quality(self, answer):
        """Analyze various quality aspects of the answer"""
        words = answer.split()
        sentences = re.split(r'[.!?]+', answer)
        
        metrics = {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if len(s.strip()) > 0]),
            'avg_sentence_length': len(words) / max(1, len(sentences)),
            'has_technical_terms': len([w for w in words if w.istitle() and len(w) > 3]) > 2,
            'has_examples': any(word in answer.lower() for word in ['example', 'for instance', 'such as']),
            'structure_score': self._assess_structure(answer)
        }
        
        # Determine strengths and improvements
        strengths = []
        improvements = []
        
        if metrics['word_count'] >= 50:
            strengths.append("Good answer length")
        else:
            improvements.append("Provide more detailed explanation")
            
        if metrics['has_technical_terms']:
            strengths.append("Uses appropriate terminology")
        else:
            improvements.append("Include more technical terms")
            
        if metrics['has_examples']:
            strengths.append("Includes examples")
        else:
            improvements.append("Add specific examples to support your points")
            
        if metrics['structure_score'] >= 0.7:
            strengths.append("Well-structured answer")
        else:
            improvements.append("Improve answer structure with clear paragraphs")
        
        metrics['completeness'] = min(metrics['word_count'] / 100, 1.0)
        metrics['strengths'] = strengths
        metrics['improvements'] = improvements
        
        return metrics
    
    def _assess_structure(self, answer):
        """Assess the structure of the answer"""
        structure_indicators = [
            len(re.findall(r'\b(first|second|third|finally)\b', answer.lower())) > 0,
            len(re.findall(r'\b(therefore|however|moreover)\b', answer.lower())) > 0,
            answer.count('.') >= 2,
            len(answer.split('\n')) > 1 or answer.count(',') >= 3
        ]
        
        return sum(structure_indicators) / len(structure_indicators)
    
    def _generate_feedback(self, metrics, relevance, score):
        """Generate personalized feedback"""
        if score >= 9:
            return "Excellent answer! Comprehensive, well-structured, and highly relevant."
        elif score >= 7:
            return "Good answer. Covers main points well with room for minor improvements."
        elif score >= 5:
            return "Satisfactory answer. Addresses the question but needs more depth and detail."
        else:
            return "Needs significant improvement. Focus on providing more detailed explanations and examples."