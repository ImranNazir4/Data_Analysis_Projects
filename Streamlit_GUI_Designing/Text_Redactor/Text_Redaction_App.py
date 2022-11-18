import streamlit as slt
import os
import spacy
#NLP Packages
# import spacy
# from spacy import displacy
# nlp=spacy.load("en_core_web_sm")

#Function for Sanitization and Redaction
# def  Sanintize_Names(text):
# 	docx=nlp(text)
# 	redaction_sentences=[]
# 	for ent in docx.ents:
# 		for token in docx:
# 			if token.ent_type_=="PERSON":
# 				redaction_sentences.append("[Name Redacted]")
# 			else:
# 				redaction_sentences.append(token.text)
# 	return " ".join(redaction_sentences)





def main():
	slt.title("Document Redactor App")
	slt.text("This App is Build Using Spacy and streamlit")

	activities=["Redaction","Downloads","About"]
	choice=slt.sidebar.selectbox("Menu",activities)

	if choice=="Redaction":
		slt.subheader("Redaction of Document")
		rawtext=slt.text_area("","Type Here")
		redaction_item=["names","places","orgs","dates"]
		redaction_choice=slt.selectbox("Select Term to Sensor",redaction_item)
		save_option=slt.radio("Save File",["Yes","No"])
		# if slt.button("Submit"):
		# 	# result=Sanintize_Names(rawtext)
			# slt.write(result)







	if choice=="Downloads":
		slt.subheader("Downloads")
	if choice=="About":
		slt.subheader("About")





if __name__ == '__main__':
	main()