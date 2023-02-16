#dependencies
import pandas as pd
import streamlit as slt
import neattext as nt
import io
import docx2txt
import unidecode
import re
#utils to download the file
import base64
import time
import requests
timestring=time.strftime("%Y%M%d-%H%M%S")


def app():
	#method for reading multiple documents
	def read_bulk_docx(document):
	    document= docx2txt.process(document)
	    doc_text = str(document)
	    return doc_text
    #methods for downloading single-file extracted results
	def download(data,job_type):
		csv_file=data.to_csv(index=False)
		b64=base64.b64encode(csv_file.encode()).decode() #b64 encoding
		slt.markdown("### Import Results ")
		new_file='Extracted_{}_Results_{}.csv'.format(job_type,timestring)
		href=f'<a href="data:file/csv;base64,{b64}" download="{new_file}">Click Here</a>'
		slt.markdown(href,unsafe_allow_html=True)
    #method for downloading multi-file extracted results
	def download_bulk(data):
		csv_file=data.to_csv(index=False)
		b64=base64.b64encode(csv_file.encode()).decode() #b64 encoding
		slt.markdown("### Import Results ")
		new_file='Extracted_Results_{}.csv'.format(timestring)
		href=f'<a href="data:file/csv;base64,{b64}" download="{new_file}">Click Here</a>'
		slt.markdown(href,unsafe_allow_html=True)

    #method for searching query on the Google
	def fetch_query(query):
		base_url="https://www.google.com/search?q={}".format(query)
		request=requests.get(base_url)
		return request.text
    #application title
	slt.title("Text Extractor")
	#text extraction by quering the google
	choice="Extract Query"
	if choice=="Extract Query":
		query_input=slt.text_input("Paste Query Here")
		generated_query=f"{query_input}"
		slt.info("Generated_Query: {}".format(generated_query))
		query_text=fetch_query(generated_query)
    #extracting the specific terms
	slt.subheader("Extract Specific Terms")
	slt.write("Write Here")

	col1,col2,col3=slt.columns((1,1,2))
	with col1:
		term1=slt.text_input("Term 1")
	with col2:
		term2=slt.text_input("Term 2")
	with col3:
		term3=slt.text_input("Pattern")
	uploaded_files=slt.file_uploader("Import File",type=["docx"],accept_multiple_files=True)
    #available text extracion options
	slt.subheader("Select Extraction Terms")
	selections=slt.multiselect("Select",["Phone No","Emails","User Handles","URLS"])
	col1,col2=slt.columns(2)
	with col1:
		flag=0
		documents=list()
		if len(uploaded_files)!=0 or generated_query!="":
		    for files in uploaded_files:
		        data = io.BytesIO(files.getbuffer())
		        data=read_bulk_docx(data)
		        documents.append(data)
		    raw_text=str(documents)+query_text
		    raw_text=unidecode.unidecode(raw_text)
		    raw_text=raw_text.encode('unicode_escape').decode('ascii')
		    extracts=[]
		    if slt.button("Extract"):
		    	if term1 !="":
		    		term1_finds=re.findall(term1,raw_text)
		    		term1_finds=list(term1_finds)
		    		term1_finds=pd.DataFrame(term1_finds,columns=["Term1 Finds"])
		    		extracts.append(term1_finds)
		    	if term2 !="":
		    		term2_finds=re.findall(term2,raw_text)
		    		term2_finds=list(term2_finds)
		    		term2_finds=pd.DataFrame(term2_finds,columns=["Term2 Finds"])
		    		extracts.append(term2_finds)
		    	if term3 !="":
		    		term3_finds=re.findall(term3,raw_text)
		    		term3_finds=list(term3_finds)
		    		term3_finds=pd.DataFrame(term3_finds,columns=["Term3 Finds"])
		    		extracts.append(term3_finds)
		    	if "User Handles" in selections:
		    		user_handles=nt.extract_userhandles(raw_text)
		    		user_handles=pd.DataFrame(emails,columns=["User Handles"])
		    		extracts.append(user_handles)
		    	if "Emails" in selections:
		    		emails=nt.extract_emails(raw_text)
		    		emails=pd.DataFrame(emails,columns=["Emails"])
		    		extracts.append(emails)
		    	if "URLS" in selections:
		    		urls=nt.extract_urls(raw_text)
		    		urls=pd.DataFrame(urls,columns=["URLS"])
		    		extracts.append(urls)
		    	if "Phone No" in selections:
		    		phones=nt.extract_phone_numbers(raw_text)
		    		phones=pd.DataFrame(phones,columns=["Phone No"])
		    		extracts.append(phones)
		    	if "Telegram Profiles" in selections:
		    		telegram_profiles=re.findall(re.compile("(?:https?:)?\/\/(?:t(?:elegram)?\.me|telegram\.org)\/(?P<username>[a-z0-9\_]{5,32})\/?"),raw_text)
		    		telegram_profiles=pd.DataFrame(telegram_profiles,columns=["Telegram Profiles"])
		    		extracts.append(telegram_profiles)
		    	if "GitHub Profiles" in selections:
		    		git_profiles=re.findall(re.compile("(?:https?:)?\/\/(?:www\.)?github\.com\/(?P<login>[A-z0-9_-]+)\/(?P<repo>[A-z0-9_-]+)\/?"),raw_text)
		    		git_profiles=pd.DataFrame(git_profiles,columns=["GitHub Profiles","S"])
		    		extracts.append(git_profiles)
		    	if len(selections)!=0:
		    		df=pd.concat(extracts,axis=1)
		    		slt.write(df)
		    	else:
		    		slt.info("Please Make At least One Selection")
		    	with slt.expander("Conert to DataFrame"):
		    		download(df,selections)
