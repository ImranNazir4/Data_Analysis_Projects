#depensencies
import streamlit as slt
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import tomotopy as tp
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt #package for data visulaizations
sent_anal_obj=SentimentIntensityAnalyzer()
import neattext as nt
from sklearn.feature_extraction.text import TfidfVectorizer 
import pickle
# loading the trained model
pickle_in = open('emotions_classifier.pkl', 'wb') 
# em_classifier = pickle.load(pickle_in)
import spacy
nlp=spacy.load("en_core_web_sm")


def app():
	#method for topic modelling
	def topic_modelling(text):
		text=str(text)
		topic_list=[]
		df_list=[]
		l=[]
		f = open("temp.txt", "w")   #reading the temp file
		f.write(text) #writing the review in the file
		f.close()
		mdl = tp.LDAModel(k=10)       #model creation, k=number_of_topic(for which you want to train your model)
		for line in open('temp.txt'):
			mdl.add_doc(line.strip().split())   #adding corpus to model
		for i in range(0, 400, 10):
			mdl.train(10)    #train our model
		for k in range(mdl.k):
			topics=mdl.get_topic_words(k, top_n=5)  #getting desired number of topics from trained model K=number_of_topics
			return topics
    #method for aspect extraction
	def ABSA(text):
		doc=nlp(text)
		descriptive_term = ''
		target = ''
		for token in doc:
			if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
				target = token.text
			if token.pos_ == 'ADJ':
				prepend = ''
				for child in token.children:
					if child.pos_ != 'ADV':
						continue
					prepend += child.text + ' '
					descriptive_term = prepend + token.text
		return target+", "+descriptive_term


    #text cleaning
	def pre_cleaning(text):
	    text=nt.fix_contractions(text)
	    text=nt.remove_puncts(text)
	    text=nt.remove_bad_quotes(text)
	    text=nt.remove_emojis(text)
	    text=nt.remove_accents(text)
	    text=nt.remove_multiple_spaces(text)
	    text=nt.remove_non_ascii(text)
	    text=nt.remove_userhandles(text)
	    return text
	def post_cleaning(text):
		text=nt.remove_stopwords(text)
		text=nt.remove_shortwords(text,3)
		text=nt.remove_numbers(text)
		return text
    #text vectorization
	def vect_predict(em_df):
		vectorizer = TfidfVectorizer(max_features=5000)
		X = vectorizer.fit_transform(em_df.Cleaned_Data)
		y_pred = em_classifier.predict(X)
		fig,ax=plt.subplots()
		ax=sns.countplot(y_pred)
		for container in ax.containers:
			ax.bar_label(container)
			slt.pyplot(fig)

    #sentimet tagging
	def sentiment_tag(polarity):
	    if polarity >= 0.05 :
	        return "Positive"
	    elif polarity <= - 0.05:
	        return "Negative"
	    else:
	        return "Neutral"

    #setiment scoring
	def sentiment_score(my_text):
		sentimnent_dict=sent_anal_obj.polarity_scores(str(my_text))
		return sentimnent_dict['compound']

    #application title
	slt.title('Products Reviews Ananlyzer')

	uploaded_file = slt.file_uploader("Import File",type=["csv"])
	if uploaded_file is not None:
	  df = pd.read_csv(uploaded_file)
	  slt.dataframe(df)
	  df=df.dropna(axis=0)
	  cat_cols = df.select_dtypes(np.object).columns
	  selected_cat_col=slt.selectbox("Select Reviews Feature",cat_cols)
	  if slt.button('Ananlyze'):
	  	slt.subheader("Sentiments Distribution")
	  	df['Sentiments Score']=df[selected_cat_col].apply(lambda x:sentiment_score(str(x)))
	  	df['Sentiments Tag']=df['Sentiments Score'].apply(lambda x:sentiment_tag(x))
	  	fig,ax=plt.subplots()
	  	ax=sns.countplot(df['Sentiments Tag'])
	  	for container in ax.containers:
	  		ax.bar_label(container)
	  		slt.pyplot(fig)
	  	with slt.expander("Advance Sentiment Analysis"):
			  slt.subheader("Emotions Classification")
			  df['Cleaned_Data']=df[selected_cat_col].apply(lambda x:pre_cleaning(str(x)))
			  df['Aspects']=df[selected_cat_col][0:100].apply(lambda x:ABSA(str(x)))
			  df['Cleaned_Data']=df['Cleaned_Data'].apply(lambda x:post_cleaning(str(x)))
			  vect_predict(df)
			  df['Topics']=df['Cleaned_Data'][0:100].apply(lambda x:((topic_modelling(x))))
			  df['Topics']=df['Topics'][0:100].apply(lambda x:', '.join([item[0] for item in x]))
			  slt.table(df[[selected_cat_col,'Sentiments Tag','Aspects','Topics']].head(5))
			




