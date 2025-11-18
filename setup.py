from setuptools import setup, find_packages

setup(
    name="ai_exam_preparation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.28.0',
        'numpy>=1.24.3',
        'pandas>=2.0.3',
        'scikit-learn>=1.3.0',
        'nltk>=3.8.1',
        'transformers>=4.33.0',
        'torch>=2.0.1',
        'sentence-transformers>=2.2.2',
        'PyPDF2>=3.0.1',
        'python-docx>=0.8.11',
        'plotly>=5.15.0',
        'textstat>=0.7.3'
    ],
    author="AI Exam Preparation Team",
    description="AI-Powered Exam Preparation and Assessment System",
    python_requires='>=3.8',
)