#dependencies
import pandas as pd
import numpy as np
import streamlit as slt
import re
import neattext as nt
# utils for downloding the redacted text
import time
import requests
timestring=time.strftime("%Y%M%d-%H%M%S")
import base64

def app():
    #method for downloading the redcted text
	def text_downloader(raw_text):
		b64 = base64.b64encode(raw_text.encode()).decode()
		new_filename = "redacted_text_{}_.txt".format(timestring)
		slt.markdown("#### Download File ###")
		href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
		slt.markdown(href,unsafe_allow_html=True)
    #method for reading the documents
	def read_docx(document):
		import docx2txt
		document= docx2txt.process(document)
		doc_text = str(document)
		return doc_text

    #application title
	slt.title("Document Redactor")
	#redaction of specific term
	slt.subheader("Redact Specific Terms")
	slt.write("Write Here")
	col1,col2,col3=slt.columns((1,1,2))
	with col1:
		term1=slt.text_input("Term 1")
	with col2:
		term2=slt.text_input("Term 2")
	with col3:
		term3=slt.text_input("Regular Expression")

	file=slt.file_uploader("Import File",type=["docx"])
	slt.subheader("Select Redaction Terms")
	#available text redaction options
	selections=slt.multiselect("Select",["Phone No","Credit Card No","National Tax Number","Vehicle Number","IBAN","Emails","Skype ID","National ID","Drivig Liscence","URLS"])
	col1,col2=slt.columns(2)
	with col1:
		if file is not None:
			slt.subheader("Raw Text")
			slt.write(" ")
			slt.write(" ")
			slt.write(" ")
			if "document" in file.type:
				raw_text=read_docx(file)
				slt.write(read_docx(file))
	with col2:
		if file is not None:
			slt.subheader("Redacted Text")
			if slt.button("Redact"):
				redacted_text=raw_text
				if term1 !="":
					redacted_text=re.sub(term1,"[Redacted]",redacted_text)
				if term2 !="":
					redacted_text=re.sub(term2,"[Redacted]",redacted_text)
				if term3 !="":
					redacted_text=re.sub(term3,"[Redacted]",redacted_text)
				if "Credit Card No" in selections:
					redacted_text=re.sub(re.compile(r'''(\b(?:\d[ -]*?){13,16}\b)''',re.VERBOSE),"[CREDT CARD]",redacted_text)
				if "IBAN" in selections:
					redacted_text=re.sub(re.compile("[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}"),"[IBAN]",redacted_text)
				if "Phone No" in selections:
					redacted_text=nt.replace_phone_numbers(redacted_text,"[PHONE NO]")
				if "Emails" in selections:
					redacted_text=nt.replace_emails(redacted_text,"[EMAIL]")
				if "URLS" in selections:
					redacted_text=re.sub(re.compile(r'''(?P<domain>(https?:\/\/(www\.)?|www\.)[\-\w@:%\.\+~\#=]{2,256}\.[a-z]{2,6}/?)(?P<path>[\-\w@:%\+\.~\#?&/=]*)''', re.VERBOSE),"[URL]",redacted_text)
				if "Vehicle Number" in selections:
					redacted_text=re.sub(re.compile("[A-Z]{3}-[0-9]{4}"),"[Vehicle-Bike]",redacted_text)
					redacted_text=re.sub(re.compile("[A-Z]{3}-[0-9]{3}"),"[Vehicle]",redacted_text)
				if "National ID" in selections:
					redacted_text=re.sub(re.compile("[0-9]{5}-[0-9]{7}-[0-9]{1}"),"[CNIC]",redacted_text)
					redacted_text=re.sub(re.compile("[0-9]{13}"),"[CNIC]",redacted_text)
				if "Skype ID" in selections:
					redacted_text=re.sub(re.compile("(?:(?:callto|skype):)(?P<username>[a-z][a-z0-9\.,\-_]{5,31})(?:\?(?:add|call|chat|sendfile|userinfo))?"),"[SKYPE ID]",redacted_text)
				if "MAC Address" in selections:
					redacted_text=re.sub("^([0-9A-Fa-f]{2}[:-])"+"{5}([0-9A-Fa-f]{2})|"+"([0-9a-fA-F]{4}\\."+"[0-9a-fA-F]{4}\\."+"[0-9a-fA-F]{4})$","[MAC ADDRESS]",redacted_text)
				if "Drivig Liscence" in selections:
					redacted_text=re.sub(re.compile("[0-9]{5}-[0-9]{7}-[0-9]{1}[#][0-9]{3}"),'DLN',redacted_text)
				if "National Tax Number" in selections:
					redacted_text=re.sub(re.compile("[0-9]{7}-[0-9]{1}"),'NTN',redacted_text)	
				slt.write(redacted_text)
				#downloading the redacted text
				text_downloader(redacted_text)
