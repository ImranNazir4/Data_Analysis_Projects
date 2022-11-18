import pandas as pd
import numpy as np
import streamlit as slt
import unidecode
import io
import re
import neattext as nt
import docx2txt
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer 
import time
import requests
timestring=time.strftime("%Y%M%d-%H%M%S")
import base64
# import displacy
nlp=spacy.load("en_core_web_sm")

def app():
    #method for downloading the ranked resumes
	def download_bulk(data):
	    csv_file=data.to_csv(index=False)
	    b64=base64.b64encode(csv_file.encode()).decode() #b64 encoding
	    slt.markdown("### Import Results ")
	    new_file='Extracted_Results_{}.csv'.format(timestring)
	    href=f'<a href="data:file/csv;base64,{b64}" download="{new_file}">Click Here</a>'
	    slt.markdown(href,unsafe_allow_html=True)
    
    # method for reading a single document
	def read_docx(document):
		import docx2txt
		document= docx2txt.process(document)
		doc_text = str(document)
		return doc_text
    #method for reading the multiple document
	def read_bulk_docx(document,file_name):
	    resumes_data=dict()
	    document= docx2txt.process(document)
	    doc_text = str(document)
	    resumes_data[file_name]=document
	    df=pd.DataFrame(resumes_data.items(),columns=['Resume Name','Resume Text'])
	    return df

    # method for ranking the resumes
	def resume_ranker(resume_text,std_resume_text):
		cv=CountVectorizer()
		content=[resume_text,std_resume_text]
		matrix=cv.fit_transform(content)
		similarity_matrix=cosine_similarity(matrix)[0][1]
		similarity=round((similarity_matrix*100),3)
		return similarity
    #application title
	slt.title("Resumes Ranking System")
	ranking_type=slt.radio("Select",["Rank Your Resume","Rank Bulk Resumes"])
	if ranking_type=="Rank Your Resume":
		uploaded_resume=slt.file_uploader("Add Resume",type=["docx"])
		if uploaded_resume is not None:
			job_description=slt.text_area("Paste Job Description Here")
			if "document" in uploaded_resume.type:
				resume_text=read_docx(uploaded_resume)
			if slt.button("Rank"):
				slt.subheader("Your Resume Matched with Job Description",slt.title(resume_ranker(resume_text,job_description)))
			#finding matched keywords
			with slt.expander("Analyze"):
				slt.subheader("MATCHED_KEYWORDS")
				import yake
				matched_words=[]
				job_description=job_description.lower()
				resume_text=resume_text.lower()
				kw_extractor = yake.KeywordExtractor(stopwords=None)
				keywords = kw_extractor.extract_keywords(job_description)
				for kw,v in keywords:
					if kw in resume_text:
						matched_words.append(kw)
				slt.write(matched_words)
	else:
        #method for ranking multiple resumes
		uploaded_file = slt.file_uploader("Choose a file",type=['docx'],accept_multiple_files=True)
		dfs=[]
		#reading the uploaded files
		if len(uploaded_file)!=0:
		    for files in uploaded_file:
		        data = io.BytesIO(files.getbuffer())
		        data=read_bulk_docx(data,files.name)
		        dfs.append(data)
		    df=pd.concat(dfs,axis=0)  #joining all the dataframes
		    df['Resume Text']=df['Resume Text'].apply(lambda x:unidecode.unidecode(x))
		    df['Resume Text']=df['Resume Text'].apply(lambda x:re.sub('\n',' ',x))
		    df['Candidate Email']=df['Resume Text'].apply(lambda x:'|'.join(nt.extract_emails(x)))
		    df['Candidate Email']=df['Candidate Email'].apply(lambda x:[email for email  in x.split("|")][0])
		    df['Candidate Phone']=df['Resume Text'].apply(lambda x:'|'.join(nt.extract_phone_numbers(x)))
		    df['Candidate Phone']=df['Candidate Phone'].apply(lambda x:[phone for phone  in x.split("|")][0])
		    slt.dataframe(df)
		    with slt.expander("Resumes Ranker"):
		    	slt.subheader("Define Ranking Attributes")
		    	std_resume=slt.file_uploader("Select Standard Resume",type=['docx'])
		    	if std_resume is not None:
			    	std_resume_text=read_docx(std_resume)
			    	df['Eligibility_%']=df['Resume Text'].apply(lambda x:resume_ranker(x.lower(),std_resume_text.lower()))
			    	slt.dataframe(df[['Resume Name','Candidate Email','Candidate Phone','Eligibility_%']].sort_values("Eligibility_%",ascending=False))
		    		eligibility=slt.number_input("Select Eligibility_%",min_value=40, max_value=90, value=50, step=5)
		    		if slt.button("Filter"):
		    			slt.dataframe(df[df['Eligibility_%']>=eligibility][['Resume Name','Candidate Email','Candidate Phone','Eligibility_%']].sort_values("Eligibility_%",ascending=False))
	    			if slt.button("Import Filtered Results"):
	    				res=df[df['Eligibility_%']>=eligibility][['Resume Name','Candidate Email','Candidate Phone','Eligibility_%']]
	    				download_bulk(res)

