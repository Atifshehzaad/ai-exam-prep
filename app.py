import streamlit as st
import pandas as pd
import plotly.express as px
from modules.text_processing import TextProcessor
from modules.question_generator import QuestionGenerator
from modules.assessment_engine import AssessmentEngine
from modules.ai_detector import AIContentDetector
from modules.text_rewriter import TextRewriter
from utils.file_handlers import FileHandler
from utils.visualization import Visualization
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="AI-Powered Exam Preparation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .module-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .score-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class ExamPreparationApp:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.question_generator = QuestionGenerator()
        self.assessment_engine = AssessmentEngine()
        self.ai_detector = AIContentDetector()
        self.text_rewriter = TextRewriter()
        self.file_handler = FileHandler()
        self.visualizer = Visualization()
        
    def render_sidebar(self):
        st.sidebar.title("🎓 AI Exam Preparation System")
        st.sidebar.markdown("---")
        
        module = st.sidebar.selectbox(
            "Select Module",
            ["🏠 Dashboard", "📚 Exam Preparation", "📝 Assessment", "🔍 AI Content Detection", "✍️ Text Rewriting"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **Group Members:**
        - Atif Shahzad
        - Adil Yousaf  
        - Adil Ahmad
        - Muhammad Abdul Mussawar
        - Muhammad Usama
        """)
        
        return module
    
    def render_dashboard(self):
        st.markdown('<h1 class="main-header">AI-Powered Exam Preparation System</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="module-card">
                <h3>📚 Exam Preparation</h3>
                <p>Upload course materials and generate important questions, MCQs, and summaries.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="module-card">
                <h3>📝 Assessment & Evaluation</h3>
                <p>Attempt questions and get instant AI-powered feedback with scores.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="module-card">
                <h3>🔍 AI Content Detection</h3>
                <p>Detect AI-generated content and improve assignment originality.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick start guide
        st.subheader("🚀 Quick Start Guide")
        guide_col1, guide_col2, guide_col3 = st.columns(3)
        
        with guide_col1:
            st.write("**1. Upload Materials**")
            st.write("Upload PDFs, DOCX, or text files with your course content")
            
        with guide_col2:
            st.write("**2. Generate Content**")
            st.write("Create questions, summaries, and key topics automatically")
            
        with guide_col3:
            st.write("**3. Practice & Improve**")
            st.write("Attempt questions and get personalized feedback")
    
    def render_exam_preparation(self):
        st.header("📚 Exam Preparation Module")
        
        uploaded_file = st.file_uploader(
            "Upload Course Material", 
            type=['pdf', 'txt', 'docx'],
            help="Upload PDF, TXT, or DOCX files"
        )
        
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            
            try:
                # Extract text
                extracted_text = self.file_handler.extract_text(file_path)
                
                if extracted_text:
                    st.success("✅ Text extracted successfully!")
                    
                    # Process text
                    with st.spinner("Processing content..."):
                        processed_data = self.text_processor.process_text(extracted_text)
                    
                    # Display key information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Document Statistics")
                        stats = self.text_processor.get_document_stats(extracted_text)
                        st.write(f"**Word Count:** {stats['word_count']}")
                        st.write(f"**Sentence Count:** {stats['sentence_count']}")
                        st.write(f"**Key Topics:** {len(stats['key_topics'])}")
                    
                    with col2:
                        st.subheader("🔑 Key Topics Identified")
                        for i, topic in enumerate(stats['key_topics'][:10], 1):
                            st.write(f"{i}. {topic}")
                    
                    # Generate content
                    st.subheader("🎯 Generate Study Materials")
                    
                    gen_col1, gen_col2, gen_col3 = st.columns(3)
                    
                    with gen_col1:
                        if st.button("📝 Generate Questions", use_container_width=True):
                            with st.spinner("Generating questions..."):
                                questions = self.question_generator.generate_questions(extracted_text)
                                st.session_state.questions = questions
                    
                    with gen_col2:
                        if st.button("❓ Generate MCQs", use_container_width=True):
                            with st.spinner("Generating MCQs..."):
                                mcqs = self.question_generator.generate_mcqs(extracted_text)
                                st.session_state.mcqs = mcqs
                    
                    with gen_col3:
                        if st.button("📋 Generate Summary", use_container_width=True):
                            with st.spinner("Generating summary..."):
                                summary = self.question_generator.generate_summary(extracted_text)
                                st.session_state.summary = summary
                    
                    # Display generated content
                    if 'questions' in st.session_state:
                        st.subheader("📝 Generated Questions")
                        for i, q in enumerate(st.session_state.questions, 1):
                            st.write(f"**{i}. {q}**")
                    
                    if 'mcqs' in st.session_state:
                        st.subheader("❓ Multiple Choice Questions")
                        for i, mcq in enumerate(st.session_state.mcqs, 1):
                            st.write(f"**{i}. {mcq['question']}**")
                            for opt in ['a', 'b', 'c', 'd']:
                                if opt in mcq:
                                    st.write(f"   {opt.upper()}. {mcq[opt]}")
                    
                    if 'summary' in st.session_state:
                        st.subheader("📋 Content Summary")
                        st.write(st.session_state.summary)
                
                else:
                    st.error("❌ Could not extract text from the file.")
            
            finally:
                os.unlink(file_path)
    
    def render_assessment(self):
        st.header("📝 Assessment & Evaluation Module")
        
        if 'questions' not in st.session_state or not st.session_state.questions:
            st.warning("Please generate questions first in the Exam Preparation module.")
            return
        
        st.subheader("💡 Answer the Following Questions")
        
        user_answers = {}
        scores = []
        
        for i, question in enumerate(st.session_state.questions[:5]):  # Limit to 5 questions for demo
            st.write(f"**Q{i+1}: {question}**")
            answer = st.text_area(f"Your answer for Q{i+1}:", key=f"answer_{i}", height=100)
            user_answers[i] = answer
            
            if st.button(f"Evaluate Q{i+1}", key=f"eval_{i}"):
                if answer.strip():
                    with st.spinner("Evaluating..."):
                        evaluation = self.assessment_engine.evaluate_answer(question, answer)
                        scores.append(evaluation['score'])
                        
                        st.success(f"**Score: {evaluation['score']}/10**")
                        st.write(f"**Feedback:** {evaluation['feedback']}")
                        st.write(f"**Strengths:** {', '.join(evaluation['strengths'])}")
                        st.write(f"**Improvements:** {', '.join(evaluation['improvements'])}")
                else:
                    st.warning("Please provide an answer before evaluating.")
        
        if scores:
            st.subheader("📊 Overall Performance")
            avg_score = sum(scores) / len(scores)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="score-card">
                    <h3>Average Score</h3>
                    <h2>{avg_score:.1f}/10</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="score-card">
                    <h3>Questions Attempted</h3>
                    <h2>{len(scores)}/5</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                performance = "Excellent" if avg_score >= 8 else "Good" if avg_score >= 6 else "Needs Improvement"
                st.markdown(f"""
                <div class="score-card">
                    <h3>Performance</h3>
                    <h2>{performance}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Visualization
            fig = self.visualizer.create_score_chart(scores)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_detection(self):
        st.header("🔍 AI Content Detection Module")
        
        input_text = st.text_area(
            "Paste your assignment text here:",
            height=200,
            placeholder="Enter the text you want to analyze for AI content..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Detect AI Content", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Analyzing text..."):
                        detection_result = self.ai_detector.analyze_text(input_text)
                        
                        st.subheader("Detection Results")
                        
                        # Probability gauge
                        ai_probability = detection_result['ai_probability']
                        human_probability = 1 - ai_probability
                        
                        st.write(f"**🤖 AI-Generated Probability:** {ai_probability:.1%}")
                        st.write(f"**👤 Human-Written Probability:** {human_probability:.1%}")
                        
                        # Visual indicator
                        if ai_probability > 0.7:
                            st.error("🚨 High likelihood of AI-generated content")
                        elif ai_probability > 0.4:
                            st.warning("⚠️ Mixed AI/Human content detected")
                        else:
                            st.success("✅ Likely human-written content")
                        
                        # Features analysis
                        st.subheader("📊 Text Analysis")
                        features = detection_result['features']
                        
                        for feature, value in features.items():
                            st.write(f"**{feature.replace('_', ' ').title()}:** {value:.3f}")
                
                else:
                    st.warning("Please enter some text to analyze.")
        
        with col2:
            if st.button("✍️ Improve Originality", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Rewriting text..."):
                        rewritten = self.text_rewriter.rewrite_text(input_text)
                        
                        st.subheader("✨ Improved Version")
                        st.write(rewritten['improved_text'])
                        
                        st.subheader("🔄 Changes Made")
                        for change in rewritten['changes']:
                            st.write(f"• {change}")
                
                else:
                    st.warning("Please enter some text to rewrite.")
    
    def render_text_rewriting(self):
        st.header("✍️ Text Rewriting & Improvement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_text = st.text_area(
                "Original Text:",
                height=300,
                placeholder="Paste the text you want to improve..."
            )
        
        with col2:
            if st.button("🔄 Improve Text", use_container_width=True):
                if original_text.strip():
                    with st.spinner("Improving text..."):
                        result = self.text_rewriter.rewrite_text(original_text)
                        
                        st.text_area(
                            "Improved Text:",
                            value=result['improved_text'],
                            height=300
                        )
                        
                        st.subheader("📝 Improvements Made")
                        for improvement in result['changes']:
                            st.write(f"✅ {improvement}")
                else:
                    st.warning("Please enter some text to improve.")
        
        # Show writing tips
        st.subheader("💡 Writing Improvement Tips")
        tips = [
            "Use active voice instead of passive voice",
            "Vary sentence structure and length",
            "Include specific examples and evidence",
            "Use transition words for better flow",
            "Avoid repetitive phrases and words",
            "Include personal insights and opinions",
            "Use discipline-specific terminology appropriately"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

    def run(self):
        module = self.render_sidebar()
        
        if module == "🏠 Dashboard":
            self.render_dashboard()
        elif module == "📚 Exam Preparation":
            self.render_exam_preparation()
        elif module == "📝 Assessment":
            self.render_assessment()
        elif module == "🔍 AI Content Detection":
            self.render_ai_detection()
        elif module == "✍️ Text Rewriting":
            self.render_text_rewriting()

# Run the app
if __name__ == "__main__":
    app = ExamPreparationApp()
    app.run()