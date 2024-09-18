import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=KEY, model_name = "gpt-4o-mini", temperature=0.3)

quiz_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template="""
    Text:{text}
    You are an expert MCQ make. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} in {tone} tone.
    Make sure the questions are not repeated and check all the questions in compliance with the tone as well.
    Make sure to format the your response like RESPONSE_JSON below and use it as a guide. \
    ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}
    """
)
quiz_chain = LLMChain(llm = llm, prompt=quiz_prompt, output_key="quiz", verbose=True)

quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template="""
    You are an expert english grammarian and writer. Given a multiple choice Quiz for {subject} students. \
    You need to evaluate the complexity of teh questions and give a complexity analysis of the quiz. \
    Only use 50 words max for complexity analysis. if the quiz is not at par with the cognitive and analytical
    abilities of the students , update the quiz questions and change the tone of the quiz accordingly. \
    Quiz:
    {quiz}
    Check from an expert English Writer of the above quiz"""
)
quiz_review_chain = LLMChain(llm =llm, prompt=quiz_evaluation_prompt, output_key="review", verbose = True)

generate_and_evaluate_chain = SequentialChain(
    chains = [quiz_chain,quiz_review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"],
    verbose=True
)