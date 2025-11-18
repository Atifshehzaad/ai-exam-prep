def render_exam_preparation(self):
    st.header("📚 Exam Preparation Module")
    
    uploaded_file = st.file_uploader(
        "Upload Course Material", 
        type=['pdf', 'txt', 'docx'],
        help="Upload PDF, TXT, or DOCX files (max 10MB)"
    )
    
    if uploaded_file is not None:
        # File validation
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.error("❌ File too large. Please upload a file smaller than 10MB.")
            return
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_path = tmp_file.name
        
        try:
            # Validate file
            is_valid, validation_msg = self.file_handler.validate_file(file_path)
            if not is_valid:
                st.error(f"❌ {validation_msg}")
                return
            
            # Extract text
            with st.spinner("Extracting text from file..."):
                extracted_text = self.file_handler.extract_text(file_path)
            
            if extracted_text:
                st.success(f"✅ Successfully extracted {len(extracted_text)} characters from the file!")
                
                # Show file preview
                with st.expander("📄 File Preview (First 500 characters)"):
                    st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                
                # Process text
                with st.spinner("Analyzing content and identifying key topics..."):
                    processed_data = self.text_processor.process_text(extracted_text)
                
                # Display key information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Document Statistics")
                    stats = self.text_processor.get_document_stats(extracted_text)
                    st.write(f"**Word Count:** {stats['word_count']}")
                    st.write(f"**Sentence Count:** {stats['sentence_count']}")
                    st.write(f"**Key Topics Found:** {len(stats['key_topics'])}")
                
                with col2:
                    st.subheader("🔑 Key Topics Identified")
                    if stats['key_topics']:
                        for i, topic in enumerate(stats['key_topics'][:10], 1):
                            st.write(f"{i}. {topic}")
                    else:
                        st.info("No key topics could be identified from the document.")
                
                # Generate content
                st.subheader("🎯 Generate Study Materials")
                
                gen_col1, gen_col2, gen_col3 = st.columns(3)
                
                with gen_col1:
                    if st.button("📝 Generate Questions", use_container_width=True):
                        with st.spinner("Generating questions... This may take a few moments."):
                            questions = self.question_generator.generate_questions(extracted_text)
                            st.session_state.questions = questions
                
                with gen_col2:
                    if st.button("❓ Generate MCQs", use_container_width=True):
                        with st.spinner("Generating multiple choice questions..."):
                            mcqs = self.question_generator.generate_mcqs(extracted_text)
                            st.session_state.mcqs = mcqs
                
                with gen_col3:
                    if st.button("📋 Generate Summary", use_container_width=True):
                        with st.spinner("Generating summary..."):
                            summary = self.question_generator.generate_summary(extracted_text)
                            st.session_state.summary = summary
                
                # Display generated content
                if 'questions' in st.session_state and st.session_state.questions:
                    st.subheader("📝 Generated Questions")
                    for i, q in enumerate(st.session_state.questions, 1):
                        st.write(f"**{i}. {q}**")
                
                if 'mcqs' in st.session_state and st.session_state.mcqs:
                    st.subheader("❓ Multiple Choice Questions")
                    for i, mcq in enumerate(st.session_state.mcqs, 1):
                        st.write(f"**{i}. {mcq['question']}**")
                        for opt in ['a', 'b', 'c', 'd']:
                            if opt in mcq:
                                st.write(f"   {opt.upper()}. {mcq[opt]}")
                        st.write(f"   **Answer:** {mcq['correct'].upper()}")
                
                if 'summary' in st.session_state and st.session_state.summary:
                    st.subheader("📋 Content Summary")
                    st.write(st.session_state.summary)
            
            else:
                st.error("""
                ❌ Could not extract text from the file. This could be because:
                - The file is empty
                - The PDF is scanned (image-based) rather than text-based
                - The file is corrupted
                - The file format is not supported
                
                Please try with a different file.
                """)
        
        except Exception as e:
            st.error(f"""
            ❌ An error occurred while processing the file:
            **Error details:** {str(e)}
            
            Please try the following:
            1. Ensure the file is not corrupted
            2. Try with a different file format
            3. For PDFs, ensure they contain selectable text (not scanned images)
            """)
            st.info("💡 **Tip:** Try converting your file to .txt format for best results.")
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(file_path)
            except:
                pass
