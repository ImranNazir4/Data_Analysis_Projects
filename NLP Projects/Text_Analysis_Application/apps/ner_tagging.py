#dependencies
import streamlit as slt
import spacy
from spacy import displacy
import pandas as pd
nlp = spacy.load('en_core_web_sm')
# packages for downloading extractedentities
import time
timestring=time.strftime("%Y%M%d-%H%M%S")
import base64

def app():
	# method for downloading extracted entities
	def download_extracted_entities(data):
	    csv_file=data.to_csv(index=False)
	    b64=base64.b64encode(csv_file.encode()).decode() #b64 encoding
	    slt.markdown("### Import Results ")
	    new_file='Extracted_Entities_{}.csv'.format(timestring)
	    href=f'<a href="data:file/csv;base64,{b64}" download="{new_file}">Click Here</a>'
	    slt.markdown(href,unsafe_allow_html=True)
    #method for entities extraction
	def entity_entractor(text):
		docx=nlp(text)
		ents_list=[(ent.text,ent.label_) for ent in docx.ents]
		df=pd.DataFrame(ents_list,columns=["Entity","Tag"])
		return df

    # method for reading the document
	def read_docx(document):
		import docx2txt
		document= docx2txt.process(document)
		doc_text = str(document)
		return doc_text

	slt.title("Named Entity Recognizer")
	HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

	if True:
		uploaded_file=slt.file_uploader("Import File",type=["docx"])
		if uploaded_file is not None:
			if "document" in uploaded_file.type:
				raw_text=read_docx(uploaded_file)
            # available named entities
			selected_ents=slt.multiselect("Entities",["PERSON","ORG","GPE","LOC","PRODUCT","EVENT","DATE","LANGUAGE"])

			result_df=entity_entractor(raw_text)
			filtered_ents=[]
			if slt.button("Extract"):
				if selected_ents!=False:
					for i,j in enumerate(selected_ents):
						temp=result_df[result_df['Tag']==j]['Entity'].unique().tolist()
						t=pd.DataFrame(temp,columns=[j])
						filtered_ents.append(t)
						extracted_ents=pd.concat(filtered_ents,axis=1)
					slt.dataframe(extracted_ents)
					# downloading extracted entities
					download_extracted_entities(extracted_ents)

	HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
	col1,col2=slt.columns((3,2))

