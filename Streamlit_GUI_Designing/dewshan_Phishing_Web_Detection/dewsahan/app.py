import streamlit as st
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt
import pickle as pkl
st.set_page_config(initial_sidebar_state="collapsed")
from RF import rf_predict_page
from AllInOne import all_predict_page
import streamlit.components.v1 as components


model=pkl.load(open("nb_model.pkl","rb"))


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; font-size-adjust: 0.6; padding-bottom: 80px;'>NETWORK INTRUSION DETECTION SYSTEM</h1>", unsafe_allow_html=True) 
page = st.sidebar.radio("Choose the model :",("Test all the models at once","RANDOM FOREST","INTRUSION DETECTION"))
if page == "Test all the models at once":
    all_predict_page()              
if page == "RANDOM FOREST":
    rf_predict_page()
if page=="INTRUSION DETECTION":
    url = st.text_input('Enter the URL')
    # check the url is valid or not
    if st.button('Check!'):
        try:
            response = re.get(url, verify=False, timeout=4)
            if response.status_code != 200:
                print(". HTTP connection was not successful for the URL: ", url)
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
                result = model.predict(vector)
                if result[0] == 0:
                    st.success("This web page seems a legitimate!")
                else:
                    st.warning("Attention! This web page is a potential PHISHING!")

        except re.exceptions.RequestException as e:
            print("--> ", e)


