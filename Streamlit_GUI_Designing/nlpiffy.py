import streamlit as slt
import spacy
from gensim.summarization import summarize
from textblob import TextBlob


#NLP packages
def text_tokenizer(tokening_text):
	nlp=spacy.load("en_core_web_sm")
	docx=nlp(tokening_text)
	f_tokens=[('"Tokens: "{},"Lemma: "{}'.format(token.text,token.lemma_)) for token in docx]
	return f_tokens


def entities_extractor(entities_extraction):
	nlp=spacy.load("en_core_web_sm")
	docx=nlp(entities_extraction)
	# e_entitis=[(entity.text,entity.label_) for entity in docx.ents]
	f_e_entities=[('"Tokens: "{},"Entity: "{}'.format(entity.text,entity.label_)) for entity in docx.ents]
	return f_e_entities








def main():
	"""NLP app with Streamlit"""
slt.title("NLPiffy App with Streamlit")

#Tokenization
if slt.checkbox("Show Tokens and Lemma"):
	 slt.subheader("Tokenize Your Text")
	 to_tokenize=slt.text_area('Enter Text', "Type Here...")
	 if slt.button("Tokenize"):
	 	tokenized_text=text_tokenizer(to_tokenize)
	 	slt.json(tokenized_text)



#Names Entity
if slt.checkbox("Entities Extraction"):
	 slt.subheader("Entities in Your Text")
	 to_entities=slt.text_area('Enter Text', "Type Here...")
	 if slt.button("Extract"):
	 	extracted_entities=entities_extractor(to_entities)
	 	slt.json(extracted_entities)



#Sentiment Analysis
if slt.checkbox("Sentiment Analysis"):
	 slt.subheader("Sentiment of Your Text")
	 to_sentiment=slt.text_area('Enter Text', "Type Here...")
	 if slt.button("Analyze"):
	 	blob=TextBlob(to_sentiment)
	 	sentiment=blob.sentiment
	 	if  sentiment.polarity<0 :
	 		slt.warning("Sentiment is Negative")
	 	elif sentiment.polarity>0 :
	 		slt.success("Sentiment is Positive")
	 	# elif sentiment.polarity==0.5:
	 	# 	slt.info("Neither Positive or Negative")


#Text Summarization
if slt.checkbox("Text Summarization"):
	 slt.subheader("Summary of Your Text")
	 to_summary=slt.text_area('Enter Text', "Type Here...")
	 if slt.button("Summarize"):
	 		summarized=summarize(to_summary)
	 		slt.success(summarized)


if __name__ == '__main__':
	main()