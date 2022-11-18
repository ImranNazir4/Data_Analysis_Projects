import streamlit as slt
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def covert_to_df(sentiment):
	dict_sentiment={"Polarity":sentiment.polarity,
	"Subjectivity":sentiment.subjectivity

	}
	df=pd.DataFrame(dict_sentiment.items(),columns=['Metric','Value'])
	return df


def anlyze_token_sentiment(docx):
	analyzer=SentimentIntensityAnalyzer()
	positive_sent=[]
	negative_sent=[]
	neutral_sent=[]
	for i in docx.split():
		res=analyzer.polarity_scores(i)['compound']
		if res>=0.1:
			positive_sent.append(i)
			positive_sent.append(res)
		elif res<=-0.1:
			negativ_sent.append(i)
			negative_sent.append(res)
		else:
			neutral_sent.append(i)
			negative_sent.append(res)
	result={'Positive':positive_sent,'Negative':negative_sent,'Neutral':neutral_sent}
	return result




def main():
	slt.title("Streamlit App")
	slt.subheader("Sentiment Analysis")

	menu=["Home","About"]
	choice=slt.sidebar.selectbox("Menu",menu)
	if choice=="Home":
		slt.subheader("Home")
		with slt.form(key='nlpform'):
			raw_text=slt.text_area("Type Here")
			submit_button=slt.form_submit_button(label="Analyze")
		col1 , col2 =slt.columns([1,2])
		if submit_button:
			with col1:
				slt.info("Results")
				sentiment=TextBlob(raw_text).sentiment
				slt.write(sentiment)
				if sentiment.polarity>0:
					slt.markdown("Sentiment: Positive :smile: ")
				elif sentiment.polarity<0:
					slt.markdown("Sentiment: Negative :angry: ")
				else:
					slt.markdown("Sentiment: Neutral :neutral_face: ")
				to_df=covert_to_df(sentiment)
				slt.dataframe(to_df)
				c=alt.Chart(to_df).mark_bar().encode(x='Metric',y='Value', color='Metric')
				slt.altair_chart(c,use_container_width=True)

			with col2:
				slt.info("Token Sentiment Analysis") 
				token_sentiment=anlyze_token_sentiment(raw_text)
				slt.write(token_sentiment)
	
	else:
		slt.subheader("About")





if __name__ == '__main__':
	main()