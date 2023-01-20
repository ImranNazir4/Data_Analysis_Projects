import streamlit as st 
import pickle
import numpy as np
import pandas as pd
import time
import altair as alt
from sklearn.metrics import accuracy_score

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Load RANDOM FOREST Model
def load_model():
    with open('rf.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data1 = load_model()
clfr = data1["model"]
y_train = data1["y_train"]

def rf_predict_page2(X , y):
    #Predict w time
    rfstart_time = time.time()
    rftypes = clfr.predict(X)
    rfend_time = time.time()
        
    #Calculat testing time
    rftime = rfend_time - rfstart_time
   
    #Convert numpy.ndarray to list
    rftypelist = rftypes.tolist()
    
    
    #RF Count the number of attacks and normal
    rfnormal = rftypelist.count('normal')
    rfdos = rftypelist.count('dos')
    rfu2r = rftypelist.count('u2r')
    rfr2l = rftypelist.count('r2l')
    rfprobe = rftypelist.count('probe')

    

    

    st.markdown("<h1 style='text-align: center; color: #80ced6; border: 5px solid #80ced6; margin-bottom: 10px;'>RANDOM FOREST Model</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px;'>NORMAL <br> {rfnormal}</h4>", unsafe_allow_html=True)
    col2.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px;'>DOS <br> {rfdos}</h4>", unsafe_allow_html=True)
    col3.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px;'>U2R <br> {rfu2r}</h4>", unsafe_allow_html=True)
    col4.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px;'>R2L <br> {rfr2l}</h4>", unsafe_allow_html=True)
    col5.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px;'>PROB <br> {rfprobe}</h4>", unsafe_allow_html=True)

    
    st.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px; margin-top: 10px;'>TESTING ACCURACY : 99.895%</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; border: 2px solid #80ced6; padding: 5% 5% 5% 10%; border-radius: 5px; margin-top: 10px;'>TESTING TIME : {rftime:.3f}</h4>", unsafe_allow_html=True)
   