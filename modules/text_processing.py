import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.strip()
    
    def segment_text(self, text, segment_length=500):
        """Segment text into chunks"""
        sentences = sent_tokenize(text)
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment + " " + sentence) <= segment_length:
                current_segment += " " + sentence
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence
        
        if current_segment:
            segments.append(current_segment.strip())
            
        return segments
    
    def extract_key_phrases(self, text, top_n=15):
        """Extract key phrases using TF-IDF"""
        # Simple implementation - in production, use more sophisticated methods
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        freq_dist = FreqDist(words)
        return [word for word, freq in freq_dist.most_common(top_n)]
    
    def identify_topics(self, text, num_topics=5):
        """Identify main topics using LDA"""
        segments = self.segment_text(text)
        
        if len(segments) < 2:
            return ["Insufficient text for topic modeling"]
        
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(segments)
        
        lda = LatentDirichletAllocation(n_components=min(num_topics, len(segments)), random_state=42)
        lda.fit(tfidf_matrix)
        
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_features = [feature_names[i] for i in topic.argsort()[:-6:-1]]
            topics.append(" ".join(top_features))
            
        return topics
    
    def process_text(self, text):
        """Main text processing pipeline"""
        cleaned_text = self.clean_text(text)
        key_phrases = self.extract_key_phrases(cleaned_text)
        topics = self.identify_topics(cleaned_text)
        
        return {
            'cleaned_text': cleaned_text,
            'key_phrases': key_phrases,
            'topics': topics,
            'segments': self.segment_text(cleaned_text)
        }
    
    def get_document_stats(self, text):
        """Get document statistics"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'key_topics': self.extract_key_phrases(text, 10)
        }