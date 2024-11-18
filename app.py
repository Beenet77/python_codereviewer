import streamlit as st
import google.generativeai as ai

# Configure Google GenAI API
ai.configure(api_key="AIzaSyDXYaDfwMEw49jVzfZFpO5y_cvUxT4gXPw")  

# Define system prompt for AI
sys_prompt = """You are an AI assistant for Python code review. 
Analyze the provided Python code for syntax and logical issues. 
Identify potential bugs or improvements, and provide detailed explanations along with corrected code snippets.
Your response should be concise and helpful."""

# Streamlit App Layout
st.set_page_config(page_title=" AI Code Reviewer", layout="wide")
st.title(" An AI Code Reviewer")

# Add instructions
st.write("Enter your Python code below to analyze it for bugs and get corrected suggestions.")

# User Input Section
user_code = st.text_area("Enter your Python code here...", height=200, placeholder="Paste your Python code here...")

# Button to trigger the analysis
if st.button("Generate"):
    if user_code.strip():  # Ensure user has entered code
        has_syntax_error = False
        error_message = ""

        try:
            compile(user_code, "<string>", "exec")  # Validate syntax
        except SyntaxError as e:
            has_syntax_error = True
            error_message = f"Syntax Error: {e.msg} at line {e.lineno}."

      
        prompt = f"{sys_prompt}\n\nCode:\n{user_code}"
        if has_syntax_error:
            prompt += f"\n\n{error_message} Provide corrections."

    
        try:
            model = ai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            ai_feedback = response.text

            # Display Results
            st.subheader("Code Review")

            # Bug Report
            st.markdown("### Bug Report")
            if has_syntax_error:
                st.error(error_message)
            else:
                st.write("No syntax errors found!")

            # AI Suggestions
            st.write(ai_feedback)

        except Exception as api_error:
            st.error(f"Error fetching response from AI: {api_error}")
    else:
        st.warning("Please enter Python code for analysis.")
