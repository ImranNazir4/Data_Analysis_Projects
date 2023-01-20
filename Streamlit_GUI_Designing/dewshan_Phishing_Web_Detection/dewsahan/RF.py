import streamlit as st 
import pickle
import numpy as np
import time
import pandas as pd
from Preprocessing import process2
from Preprocessing import ptrain
from Preprocessing import prepare
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os
import warnings


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#show the result
def rf_predict(x):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore", category=UserWarning)
      data = pickle.load(open('rf.pkl', 'rb'))
    clfr = data["model"]
    rftypes = clfr.predict(x)

    if rftypes[0] == "normal" :
        st.success('NORMAL')
    else :
        st.error(f"Intrusion Detected : {rftypes[0].upper()}")


'''def rf_predict(x):
    data = pickle.load(open('rf.pkl', 'rb'))
    clfr = data["model"]
    rftypes = clfr.predict(x)

    if rftypes[0] == "normal" :
        st.success('NORMAL')
    else :
        st.error(f"Intrusion Detected : {rftypes[0].upper()}")
'''
def rf_predict_page():
    st.markdown("<h2 style='border: 5px solid #80ced6; text-align: center; color: #80ced6;'>RANDOM FOREST Model</h2>", unsafe_allow_html=True)
    choix = st.radio("Choose the model :",("Upload the data in csv format","Enter values manually"))
    
    #methode 1
    if choix == "Upload the data in csv format":
        tr = st.button("Traine the model")
        if tr:
            with st.spinner('Please Waitt...'):
                time.sleep(5)
                #train
                X_train, y_train = ptrain()
                #RANDOM FOREST
                clfr = RandomForestClassifier(n_estimators=30)
                clfr.fit(X_train, y_train.values.ravel())
                os.remove("rf.pkl") 
                data = {"model": clfr, "y_train": y_train}
                pickle.dump(data, open('rf.pkl', 'wb'))             

        fille1 = st.file_uploader(label="Upload the record in csv format :",type=['csv'])
        if fille1 is not None:
            df = prepare(fille1)
            st.markdown(f"<h2 style='text-align: center; color: white;'>REEL TYPE : {df['Attack Type'].iloc[0].upper()}</h2>", unsafe_allow_html=True)
            rf = st.button("Predict")
            if rf:
                with st.spinner('Please wait...'):
                    time.sleep(5)
                    x,y = process2(df)
                    rf_predict(x)
                

    #methode 2
    if choix == "Enter values manually":
        
        #Load RANDOM FOREST Model
        data = pickle.load(open('rf44.pkl', 'rb'))
        clfr = data["model"]
        fmap = data["flag"]
        pmap = data["protocol"]

        st.markdown("<h5 style='padding-top: 20px; color :white; font-weight: bold; font-size: 22px;'>We need some informations to predict if it's an intrusion</h5>", unsafe_allow_html=True)

        duration = st.number_input("duration",0,58329,0,1)
        protocol_type = st.selectbox("Protocol", pmap)
        flag = st.selectbox("Flag", fmap)
        src_bytes = st.number_input("src_bytes",0,988218,0,1)
        dst_bytes = st.number_input("dst_bytes",0,33040,0,1)
        land = st.slider("land",0,1,0,1)
        wrong_fragment = st.slider("wrong_fragment",0,3,0,1)
        urgent = st.slider("urgent",0,3,0,1)
        hot = st.slider("hot",0,30,0,1)
        num_failed_logins = st.slider("num_failed_logins",0,5,0,1)
        logged_in = st.slider("logged_in",0,1,0,1)
        num_compromised = st.slider("num_compromised",0,884,0,1)
        root_shell = st.slider("root_shell",0,1,0,1)
        su_attempted = st.slider("su_attempted",0,2,0,1)
        num_file_creations = st.slider("num_file_creations",0,28,0,1)
        num_shells = st.slider("num_shells",0,2,0,1)
        num_access_files = st.slider("num_access_files",0,8,0,1)
        is_guest_login = st.slider("is_guest_login",0,1,0,1)
        count = st.slider("count",0,511,0,1)
        srv_count = st.slider("srv_count",0,511,0,1)
        serror_rate = st.slider("serror_rate",0,1,0)
        rerror_rate = st.slider("rerror_rate",0,1,0)
        same_srv_rate = st.slider("same_srv_rate",0,1,0)
        diff_srv_rate = st.slider("diff_srv_rate",0,1,0)
        srv_diff_host_rate = st.slider("srv_diff_host_rate",0,1,0)
        dst_host_count = st.slider("dst_host_count",0,255,0,1)
        dst_host_srv_count = st.slider("dst_host_srv_count",0,255,0,1)
        dst_host_diff_srv_rate = st.slider("dst_host_diff_srv_rate",0,1,0)
        dst_host_same_src_port_rate = st.slider("dst_host_same_src_port_rate",0,1,0)
        dst_host_srv_diff_host_rate = st.slider("dst_host_srv_diff_host_rate",0,1,0)

        ok = st.button("Predict")
        if ok:
            x = np.array([[duration, pmap[protocol_type], fmap[flag], src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, num_failed_logins, logged_in, num_compromised, root_shell, su_attempted, num_file_creations, num_shells, num_access_files, is_guest_login, count, srv_count, serror_rate, rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count, dst_host_diff_srv_rate, dst_host_same_src_port_rate, dst_host_srv_diff_host_rate]])

            Attack_Type = clfr.predict(x)
            if Attack_Type[0] == "normal" :
                st.success('NORMAL')
            else :
                st.error(f"Intrusion Detected : {Attack_Type[0].upper()}")