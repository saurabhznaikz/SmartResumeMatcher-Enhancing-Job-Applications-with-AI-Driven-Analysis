import base64

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import pandas as pd
import json


load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("google_api_key"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}
"""

## streamlit app
st.title("Smart Resume matcher")
st.text("Improve Your Resume as per Job description")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume in pdf format",type="pdf",help="Please upload the resume pdf")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        # st.subheader(response)
        df = pd.DataFrame([json.loads(response)])
        st.table(df)
