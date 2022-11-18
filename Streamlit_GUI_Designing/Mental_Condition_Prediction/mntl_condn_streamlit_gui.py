#dependencies
import pandas as pd
import numpy as np
import streamlit as st
import pickle
from sklearn.preprocessing import LabelEncoder
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
le = LabelEncoder()

# loading the trained model
loaded_model = pickle.load(open('model_RF.pkl', 'rb'))

#loading the trained text vectorizer
vectorization_model = pickle.load(open('vectorizer.sav', 'rb'))

#lagel encoding of target feature
y=pd.read_csv('y.csv')
y = le.fit_transform(y)

#setting page layout
st.set_page_config(layout="wide")
import streamlit.components.v1 as components  # Import Streamlit

#lottie animation
import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://lottie.host/ac88792f-32a5-46a5-997a-ea021a43b178/0nsqWZlAhf.json"
lottie_url_download = "https://lottie.host/ac88792f-32a5-46a5-997a-ea021a43b178/0nsqWZlAhf.json"
lottie_hello = load_lottieurl(lottie_url_hello)
lottie_download = load_lottieurl(lottie_url_download)

#application title
st.title('Mental Condition Recognition System')
# application subtitle
st.subheader('There is hope, even when your brain tells you there isn’t.')
st.write(' ')
st.write(' ')
st.write(' ')

#taking input from user
col1,col2=st.columns((2,1))
with col1:
	# selected_symtoms=st.multiselect('What symptoms do you have?',symptoms)
	st.write(' ')
	problem_statement=st.text_area('Tell about your mental situation?')
	
	# problem_statement=problem_statement.split()
	st.write(' ')
    #making predictions
	if st.button('Predict'):
		new_X = vectorization_model.transform([problem_statement]).toarray()
		# st.write(new_X)
		Predict = loaded_model.predict(new_X.reshape(1,-1))
		Predicted = le.classes_[Predict]
		# results=Predicted[0]
		st.title(Predicted[0])
		st.subheader('Is Your Mental Condition')
with col2:
    st_lottie(lottie_hello, key="hello")
symptoms_df=pd.read_csv("symptms_of_mntl_cndtn.csv")
st.title("Find Symptoms of Your Mental Condition")
conditions=symptoms_df["condition"].tolist()
conditions.insert(0,"NA")
selected_condition=st.selectbox("Select Your Mental Condition",conditions)
symptoms=symptoms_df[symptoms_df["condition"]==selected_condition]["symptoms"]
symptoms=".".join(symptoms)
if selected_condition!="NA":
	st.subheader("Symptoms are following:")
	for index,sent in enumerate(symptoms.split(".")[0:-1]):
		st.write(str(index+1)+" - "+sent)
	  

