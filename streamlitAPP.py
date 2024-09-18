import os
import json
import traceback
import pandas as pd
import streamlit as str
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQgenerator import generate_and_evaluate_chain
from langchain.callbacks import get_openai_callback

#loading the response json format
with open('/Users/arsh/Desktop/mcqGEN/response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)
    
# creating a title for app
str.title("MCQ creator APP with Langchain")

# Create a form using str.form
with str.form("user_inputs"):
    uploaded_file = str.file_uploader("Upload a PDF or txt file")
    mcq_count = str.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = str.text_input("Insert Subject", max_chars=30)
    tone = str.text_input("Complexity level of Questions", max_chars=30, placeholder="Simple")
    button = str.form_submit_button("Generate MCQs")
    
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with str.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                response  = generate_and_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                    }
                )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                str.error("error")
            
            else:
                if isinstance(response, dict):
                    #Extract quiz from the repsonse
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            str.table(df)
                            # dispaly the review in a text box as well
                            str.text_area(label="Review", value=response["review"])
                        else:
                            str.error("Error in table data")
                else:
                    str.write(response)
    