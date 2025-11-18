import re
import numpy as np
from textstat import flesch_reading_ease, syllable_count
from collections import Counter

class AIContentDetector:
    def __init__(self):
        self.ai_indicators = [
            'highly', 'delve', 'tapestry', 'realm', 'testament',
            'moreover', 'furthermore', 'additionally', 'however',
            'it is important to note', 'in conclusion'
        ]
        
    def analyze_text(self, text):
        """Analyze text for AI-generated patterns"""
        features = self._extract_features(text)
        ai_probability = self._calculate_ai_probability(features)
        
        return {
            'ai_probability': ai_probability,
            'features': features,
            'verdict': 'AI-generated' if ai_probability > 0.7 else 
                      'Mixed' if ai_probability > 0.4 else 
                      'Human-written'
        }
    
    def _extract_features(self, text):
        """Extract linguistic features for detection"""
        words = text.lower().split()
        sentences = re.split(r'[.!?]+', text)
        
        # Basic statistics
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_sentence_length = word_count / max(1, sentence_count)
        
        # Readability score
        readability = flesch_reading_ease(text)
        
        # AI indicator words
        ai_word_count = sum(1 for word in words if word in self.ai_indicators)
        ai_word_ratio = ai_word_count / max(1, word_count)
        
        # Repetition analysis
        word_freq = Counter(words)
        most_common_count = word_freq.most_common(1)[0][1] if word_freq else 0
        repetition_ratio = most_common_count / max(1, word_count)
        
        # Sentence structure variation
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        sentence_variation = np.std(sentence_lengths) if sentence_lengths else 0
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'readability_score': readability,
            'ai_word_ratio': ai_word_ratio,
            'repetition_ratio': repetition_ratio,
            'sentence_variation': sentence_variation,
            'word_count': word_count
        }
    
    def _calculate_ai_probability(self, features):
        """Calculate probability of AI generation"""
        probability = 0.0
        
        # Sentence length heuristic (AI tends to have more uniform length)
        if 15 <= features['avg_sentence_length'] <= 25:
            probability += 0.2
        
        # Readability heuristic (AI often has very high readability)
        if features['readability_score'] > 60:
            probability += 0.2
        
        # AI word indicators
        probability += min(features['ai_word_ratio'] * 10, 0.3)
        
        # Repetition (AI might repeat certain phrases)
        if features['repetition_ratio'] > 0.05:
            probability += 0.1
        
        # Sentence variation (Human writing has more variation)
        if features['sentence_variation'] < 5:
            probability += 0.2
        
        return min(probability, 1.0)