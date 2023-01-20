import streamlit as st
from AlgoPredict import rf_predict_page2
from Preprocessing import process
import time

def all_predict_page():
    fille = st.file_uploader(label="Upload the data in csv format :",type=['csv'])
    rf = st.button("Predict")
    if fille is not None:
        if rf:
            with st.spinner("Please ..."):
                time.sleep(5)
                x,y = process(fille)
                rf_predict_page2(x,y)
            st.success('Done!')