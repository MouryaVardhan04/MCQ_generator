import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import re

from langchain_community.callbacks.manager import get_openai_callback
from src.mcq_generator.utils import read_file
from src.mcq_generator.MCQGenerator import generate_evaluate_chain
from src.mcq_generator.logger import logging

# Load predefined response JSON structure
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Set app title
st.title("MCQs Creator Application with LangChain 🦜⛓️")

# Initialize session state for quiz and response if not set
if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.response = None

# Input form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")

# Generate quiz only if it hasn't been generated
if st.session_state.quiz is None:
    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("❌ Something went wrong during MCQ generation.")
            else:
                quiz = response.get("quiz", {})

                if isinstance(quiz, str):
                    match = re.search(r'({.*})', quiz, re.DOTALL)
                    if match:
                        quiz_json_str = match.group(1)
                        try:
                            quiz = json.loads(quiz_json_str)
                        except:
                            st.error("Failed to parse quiz JSON.")
                            quiz = {}
                    else:
                        st.error("No valid quiz JSON found.")
                        quiz = {}

                # Save quiz and response to session state
                st.session_state.quiz = quiz
                st.session_state.response = response

# Display quiz if already generated
if st.session_state.quiz:
    quiz = st.session_state.quiz
    response = st.session_state.response
    user_answers = {}

    st.subheader("📝 Answer the following MCQs:")

    for key, item in quiz.items():
        question_number = int(key)
        st.markdown(f"### Q{question_number}: {item['mcq']}")
        options = item["options"]
        option_labels = [f"{k.upper()}: {v}" for k, v in options.items()]
        selected_option = st.radio(
            "Choose an option:",
            option_labels,
            key=f"radio_{question_number}"
        )
        # Save selected option key (a/b/c/d) in lowercase
        user_answers[key] = selected_option.split(":")[0].strip().lower()

    if st.button("Submit Answers"):
        score = 0
        st.subheader("📊 Results")
        for key, item in quiz.items():
            selected_key = user_answers.get(key)
            correct_key = item["correct"].strip().lower()
            correct_text = item["options"].get(correct_key, "Unknown")

            if selected_key == correct_key:
                st.success(f"Q{key}: ✅ Correct Answer!")
                score += 1
            else:
                st.error(f"Q{key}: ❌ Wrong Answer!\n\n**Correct Answer:** {correct_key.upper()}: {correct_text}")

            st.markdown(f"**Explanation:** {item['explain']}")
            st.markdown("---")

        st.info(f"🎯 Your Score: {score}/{len(quiz)}")

        # Optional Review
        if "review" in response:
            st.text_area("Review", value=response["review"], height=150)
