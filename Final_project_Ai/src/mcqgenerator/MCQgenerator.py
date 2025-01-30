import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

import sys
import os

# Add the path to the mcqgenerator module
sys.path.append(os.path.abspath("C:\\Users\\boby.DESKTOP-06SD1DP\\OneDrive - MSFT\\Final_project_Ai\\src"))

# Now import the module
from mcqgenerator.utils import read_file, get_table_data
from mcqgenerator.logger import logging
# imporing necessary packages packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key = os.getenv("OPENAI_API_KEY")

print("Value of MY_VARIABLE:", key)

llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.3)

template = """
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
    template=template,
)


quiz_chain = LLMChain(
    llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True
)

template = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of teh question and give a complete analysis of the quiz if the students
will be able to unserstand the questions and answer them. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update tech quiz questions which needs to be changed  and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"], template=template
)

review_chain = LLMChain(
    llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True
)


# This is an Overall Chain where we run the two chains in Sequence
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
)
