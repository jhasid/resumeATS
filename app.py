import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json


load_dotenv() ## load all env variable from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
        #print(text)
    return text
    
  

#PROMPT TEMPLATE

input_prompt="""
You are skillful HR assistant and very experience in ATS(Application Tracking System)
with a deep understanding of Robotic Process Automation(RPA) jon profile. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and the missing keywords with high accuracy.

resume:{pdftxt}
description:{jd}

I want the response in one single string having the structure
{{"Candidate Name":"","JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""


## Streamlit  app
st.title("Smart ATS Resume Scanner")
st.text("Improve Resume ATS")
jd=st.text_area("Paste the job description")
#print(jd)
uploaded_file=st.file_uploader("Upload your resume",type="pdf",help="Please upload the Resume PDF")

submit=st.button("SUBMIT")

if submit:
    if uploaded_file is not None:
        pdftxt=input_pdf_text(uploaded_file)
        #print(pdftxt)
        #print(jd)
        input_prompt=input_prompt.format(pdftxt=pdftxt,jd=jd)
        #print(input_prompt)
        response=get_gemini_response(input_prompt)
        st.subheader(response)