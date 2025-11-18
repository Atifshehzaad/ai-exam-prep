import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data with error handling
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

download_nltk_data()

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

class TextProcessor:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            logger.warning(f"Could not load stopwords: {e}")
            self.stop_words = set()
        
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not text or not isinstance(text, str):
            return ""
        
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s.,!?;:]', '', text)
            return text.strip()
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return text if text else ""
    
    def segment_text(self, text, segment_length=500):
        """Segment text into chunks"""
        if not text:
            return []
            
        try:
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
        except Exception as e:
            logger.error(f"Error segmenting text: {e}")
            return [text] if text else []
    
    def extract_key_phrases(self, text, top_n=15):
        """Extract key phrases using TF-IDF"""
        if not text:
            return []
            
        try:
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalnum() and word not in self.stop_words]
            
            freq_dist = FreqDist(words)
            return [word for word, freq in freq_dist.most_common(top_n)]
        except Exception as e:
            logger.error(f"Error extracting key phrases: {e}")
            return []
    
    def identify_topics(self, text, num_topics=5):
        """Identify main topics using LDA"""
        if not text:
            return ["No text available for topic modeling"]
            
        try:
            segments = self.segment_text(text)
            
            if len(segments) < 2:
                return ["Insufficient text for topic modeling"]
            
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(segments)
            
            lda = LatentDirichletAllocation(
                n_components=min(num_topics, len(segments)), 
                random_state=42
            )
            lda.fit(tfidf_matrix)
            
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            
            for topic_idx, topic in enumerate(lda.components_):
                top_features = [feature_names[i] for i in topic.argsort()[:-6:-1]]
                topics.append(" ".join(top_features))
                
            return topics
        except Exception as e:
            logger.error(f"Error in topic modeling: {e}")
            return ["Error in topic identification"]
    
    def process_text(self, text):
        """Main text processing pipeline"""
        if not text:
            return {
                'cleaned_text': "",
                'key_phrases': [],
                'topics': ["No text available"],
                'segments': []
            }
            
        try:
            cleaned_text = self.clean_text(text)
            key_phrases = self.extract_key_phrases(cleaned_text)
            topics = self.identify_topics(cleaned_text)
            
            return {
                'cleaned_text': cleaned_text,
                'key_phrases': key_phrases,
                'topics': topics,
                'segments': self.segment_text(cleaned_text)
            }
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return {
                'cleaned_text': text[:1000] if text else "",
                'key_phrases': [],
                'topics': ["Processing error"],
                'segments': []
            }
    
    def get_document_stats(self, text):
        """Get document statistics"""
        if not text:
            return {
                'word_count': 0,
                'sentence_count': 0,
                'key_topics': []
            }
            
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            return {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'key_topics': self.extract_key_phrases(text, 10)
            }
        except Exception as e:
            logger.error(f"Error getting document stats: {e}")
            return {
                'word_count': 0,
                'sentence_count': 0,
                'key_topics': []
            }
