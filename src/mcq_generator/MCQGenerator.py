import os
import pandas as pd
from dotenv import load_dotenv
import warnings

# Suppress warnings to avoid the warnings module error
warnings.filterwarnings("ignore")

# Importing necessary packages from langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
KEY = os.getenv("OPENAI_API_KEY")

# At this point, key is guaranteed to be a string
llm = ChatOpenAI(openai_api_key=KEY, model_name='gpt-3.5-turbo', temperature=0.3, verbose=False)

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "grade", "tone", "response_json"],
    template=template)

template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz if the students
will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=template2)



def generate_evaluate_chain(inputs):
    """
    Simple function to generate MCQs and evaluate them
    """
    try:
        # Generate the quiz
        quiz_prompt = quiz_generation_prompt.format(
            text=inputs["text"],
            number=inputs["number"],
            subject=inputs["subject"],
            tone=inputs["tone"],
            response_json=inputs["response_json"]
        )
        
        quiz_response = llm.invoke(quiz_prompt)
        quiz_content = quiz_response.content
        
        # Generate the review
        review_prompt = quiz_evaluation_prompt.format(
            subject=inputs["subject"],
            quiz=quiz_content
        )
        
        review_response = llm.invoke(review_prompt)
        review_content = review_response.content
        
        return {
            "quiz": quiz_content,
            "review": review_content
        }
        
    except Exception as e:
        print(f"Error in generate_evaluate_chain: {e}")
        return {
            "quiz": "Error generating quiz",
            "review": "Error generating review"
        }
    
