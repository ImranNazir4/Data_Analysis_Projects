import streamlit as slt           #python package for creating GUI
import sumy                       #python package for extractive text summarization
#Plain text parsers since we are parsing through text
from sumy.parsers.plaintext import PlaintextParser
#for tokenization
from sumy.nlp.tokenizers import Tokenizer
#utils to download the file
import base64
import time
import requests
timestring=time.strftime("%Y%M%d-%H%M%S")

def app():
    #reading the document files
    def read_docx(document):
        import docx2txt
        document= docx2txt.process(document)
        doc_text = str(document)
        return doc_text

    #method for downloading the summarized text
    def text_downloader(raw_text):
        b64 = base64.b64encode(raw_text.encode()).decode()
        new_filename = "summarized_text_{}_.txt".format(timestring)
        slt.markdown("#### Download File ###")
        href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
        slt.markdown(href,unsafe_allow_html=True)
    #application title
    slt.title('Text Summarization')
    uploaded_file= slt.file_uploader("Add Document",type=['docx'])
    sentences=slt.number_input('Summarize to Sentences',min_value=2, max_value=500, value=2, step=1)
    #text summarization options
    choices=slt.multiselect("Summarization Technique",["Latent Semantic Analysis","Lex Rank","Text Rank","Luhn"])
    summarized_text=""
    if slt.button("Summarize") and uploaded_file is not None:
        raw_text=read_docx(uploaded_file)
        #initialzing text tokenizer
        parser = PlaintextParser(raw_text, Tokenizer("english"))
        for choice in choices:
            #LSA text summarizer
            if choice=="Latent Semantic Analysis":
                summarized_text+="LSA Summarization"
                summarized_text+="\n"
                slt.subheader("LSA Summarization")
                from sumy.summarizers.lsa import LsaSummarizer
                lsa_summarizer = LsaSummarizer()
                lsa_summary=lsa_summarizer(parser.document,sentences)
                for sentence in lsa_summary:
                    summarized_text=summarized_text+str(sentence)+"\n"
                    slt.write(str(sentence))
            #Lex Rank text summarizer    
            if choice=="Lex Rank":
                summarized_text+="\n"
                summarized_text+="==============================================================================="
                summarized_text+="\n"
                summarized_text+="\n"
                summarized_text+="Lex Rank Summarization"
                summarized_text+="\n"
                slt.subheader("Lex Rank Summarization")
                from sumy.summarizers.lex_rank import LexRankSummarizer 
                lex_summarizer = LexRankSummarizer()
                #Summarize the document with 2 sentences
                lex_summary = lex_summarizer(parser.document, sentences) 
                for sentence in lex_summary:
                    summarized_text=summarized_text+str(sentence)+"\n"
                    slt.write(str(sentence))
            #Text Rank text summarizer
            if choice=="Text Rank":
                summarized_text+="\n"
                summarized_text+="==============================================================================="
                summarized_text+="\n"
                summarized_text+="\n"
                summarized_text+="Text Rank Summarization"
                summarized_text+="\n"
                slt.subheader("Text Rank Summarization")
                from sumy.summarizers.text_rank import TextRankSummarizer
                text_rank_summarizer = TextRankSummarizer()
                text_rank_summary =text_rank_summarizer(parser.document,sentences)
                for sentence in text_rank_summary:
                    summarized_text=summarized_text+str(sentence)+"\n"
                    slt.write(str(sentence))
            #Luhn text summarizer
            if choice=="Luhn":
                summarized_text+="\n"
                summarized_text+="==============================================================================="
                summarized_text+="\n"
                summarized_text+="\n"
                summarized_text+="Luhn Summarization"
                summarized_text+="\n"
                slt.subheader("Luhn Summarization")
                from sumy.summarizers.luhn import LuhnSummarizer
                luhun_summarizer = LuhnSummarizer()
                luhun_summary =luhun_summarizer(parser.document,sentences)
                for sentence in luhun_summary:
                    summarized_text=summarized_text+str(sentence)+"\n"
                    slt.write(str(sentence))
        #downloading the summarized text
        text_downloader(str(summarized_text))