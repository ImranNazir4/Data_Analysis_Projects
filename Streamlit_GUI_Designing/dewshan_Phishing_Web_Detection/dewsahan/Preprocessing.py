import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
from sklearn.ensemble import RandomForestClassifier


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def prepare(fille):
    cols="""duration,
    protocol_type,
    service,
    flag,
    src_bytes,
    dst_bytes,
    land,
    wrong_fragment,
    urgent,
    hot,
    num_failed_logins,
    logged_in,
    num_compromised,
    root_shell,
    su_attempted,
    num_root,
    num_file_creations,
    num_shells,
    num_access_files,
    num_outbound_cmds,
    is_host_login,
    is_guest_login,
    count,
    srv_count,
    serror_rate,
    srv_serror_rate,
    rerror_rate,
    srv_rerror_rate,
    same_srv_rate,
    diff_srv_rate,
    srv_diff_host_rate,
    dst_host_count,
    dst_host_srv_count,
    dst_host_same_srv_rate,
    dst_host_diff_srv_rate,
    dst_host_same_src_port_rate,
    dst_host_srv_diff_host_rate,
    dst_host_serror_rate,
    dst_host_srv_serror_rate,
    dst_host_rerror_rate,
    dst_host_srv_rerror_rate"""

    columns=[]
    for c in cols.split(','):
        if(c.strip()):
            columns.append(c.strip())

    columns.append('target')

    attacks_types = {
        'normal': 'normal',
    'back': 'dos',
    'buffer_overflow': 'u2r',
    'ftp_write': 'r2l',
    'guess_passwd': 'r2l',
    'imap': 'r2l',
    'ipsweep': 'probe',
    'land': 'dos',
    'loadmodule': 'u2r',
    'multihop': 'r2l',
    'neptune': 'dos',
    'nmap': 'probe',
    'perl': 'u2r',
    'phf': 'r2l',
    'pod': 'dos',
    'portsweep': 'probe',
    'rootkit': 'u2r',
    'satan': 'probe',
    'smurf': 'dos',
    'spy': 'r2l',
    'teardrop': 'dos',
    'warezclient': 'r2l',
    'warezmaster': 'r2l',
    }
    df = pd.read_csv(fille,names=columns)
    df['Attack Type'] = df.target.apply(lambda r:attacks_types[r[:-1]])
    return df

def process(fille):
    df = prepare(fille)
    #Finding categorical features
    num_cols = df._get_numeric_data().columns

    cate_cols = list(set(df.columns)-set(num_cols))
    cate_cols.remove('target')
    cate_cols.remove('Attack Type')

    df = df.dropna('columns')# drop columns with NaN

    # keep columns where there are more than 1 unique values
    df = df.drop('num_outbound_cmds', 1)
    df = df.drop('is_host_login', 1)

    #This variable is highly correlated with num_compromised and should be ignored for analysis.
    #(Correlation = 0.9938277978738366)
    df.drop('num_root', axis = 1 ,inplace = True)

    #This variable is highly correlated with serror_rate and should be ignored for analysis.
    #(Correlation = 0.9983615072725952)
    df.drop('srv_serror_rate',axis = 1,inplace = True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9947309539817937)
    df.drop('srv_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_serror_rate and should be ignored for analysis.
    #(Correlation = 0.9993041091850098)
    df.drop('dst_host_srv_serror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9869947924956001)
    df.drop('dst_host_serror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9821663427308375)
    df.drop('dst_host_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9851995540751249)
    df.drop('dst_host_srv_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9865705438845669)
    df.drop('dst_host_same_srv_rate',axis = 1, inplace=True)

    #protocol_type feature mapping
    pmap = {'icmp':0,'tcp':1,'udp':2}
    df['protocol_type'] = df['protocol_type'].map(pmap)

    #flag feature mapping
    fmap = {'SF':0,'S0':1,'REJ':2,'RSTR':3,'RSTO':4,'SH':5 ,'S1':6 ,'S2':7,'RSTOS0':8,'S3':9 ,'OTH':10}
    df['flag'] = df['flag'].map(fmap)

    df.drop('service',axis = 1,inplace= True)
    df = df.drop(['target',], axis=1)
    y = df[['Attack Type']]
    X = df.drop(['Attack Type',], axis=1)

    sc = MinMaxScaler()
    X = sc.fit_transform(X)
    # Split test and train data 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    #RANDOM FOREST
    clfr = RandomForestClassifier(n_estimators=30)
    clfr.fit(X_train, y_train.values.ravel())
    data = {"model": clfr, "flag" : fmap, "protocol" : pmap, "y_train": y_train}
    with open('rf.pkl', 'wb') as file:
        pickle.dump(data,file)

    return X_test, y_test
 


def process2(df):
    num_cols = df._get_numeric_data().columns
    cate_cols = list(set(df.columns)-set(num_cols))
    cate_cols.remove('target')
    cate_cols.remove('Attack Type')
    df = df.dropna('columns')
    df = df.drop('num_outbound_cmds', 1)
    df = df.drop('is_host_login', 1)
    df.drop('num_root', axis = 1 ,inplace = True)
    df.drop('srv_serror_rate',axis = 1,inplace = True)
    df.drop('srv_rerror_rate',axis = 1, inplace=True)
    df.drop('dst_host_srv_serror_rate',axis = 1, inplace=True)
    df.drop('dst_host_serror_rate',axis = 1, inplace=True)
    df.drop('dst_host_rerror_rate',axis = 1, inplace=True)
    df.drop('dst_host_srv_rerror_rate',axis = 1, inplace=True)
    df.drop('dst_host_same_srv_rate',axis = 1, inplace=True)
    pmap = {'icmp':0,'tcp':1,'udp':2}
    df['protocol_type'] = df['protocol_type'].map(pmap)
    fmap = {'SF':0,'S0':1,'REJ':2,'RSTR':3,'RSTO':4,'SH':5 ,'S1':6 ,'S2':7,'RSTOS0':8,'S3':9 ,'OTH':10}
    df['flag'] = df['flag'].map(fmap)
    df.drop('service',axis = 1,inplace= True)
    df = df.drop(['target',], axis=1)
    y = df[['Attack Type']]
    X = df.drop(['Attack Type',], axis=1)
    sc = MinMaxScaler()
    X = sc.fit_transform(X)
    return X , y

def ptrain():
    fille = "C:\\Users\\zack\\Desktop\\dewsahan\\data.csv"
    df = prepare(fille)
    #Finding categorical features
    num_cols = df._get_numeric_data().columns

    cate_cols = list(set(df.columns)-set(num_cols))
    cate_cols.remove('target')
    cate_cols.remove('Attack Type')

    df = df.dropna('columns')# drop columns with NaN

    # keep columns where there are more than 1 unique values
    df = df.drop('num_outbound_cmds', 1)
    df = df.drop('is_host_login', 1)

    #This variable is highly correlated with num_compromised and should be ignored for analysis.
    #(Correlation = 0.9938277978738366)
    df.drop('num_root', axis = 1 ,inplace = True)

    #This variable is highly correlated with serror_rate and should be ignored for analysis.
    #(Correlation = 0.9983615072725952)
    df.drop('srv_serror_rate',axis = 1,inplace = True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9947309539817937)
    df.drop('srv_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_serror_rate and should be ignored for analysis.
    #(Correlation = 0.9993041091850098)
    df.drop('dst_host_srv_serror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9869947924956001)
    df.drop('dst_host_serror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9821663427308375)
    df.drop('dst_host_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9851995540751249)
    df.drop('dst_host_srv_rerror_rate',axis = 1, inplace=True)

    #This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
    #(Correlation = 0.9865705438845669)
    df.drop('dst_host_same_srv_rate',axis = 1, inplace=True)

    #protocol_type feature mapping
    pmap = {'icmp':0,'tcp':1,'udp':2}
    df['protocol_type'] = df['protocol_type'].map(pmap)

    #flag feature mapping
    fmap = {'SF':0,'S0':1,'REJ':2,'RSTR':3,'RSTO':4,'SH':5 ,'S1':6 ,'S2':7,'RSTOS0':8,'S3':9 ,'OTH':10}
    df['flag'] = df['flag'].map(fmap)

    df.drop('service',axis = 1,inplace= True)
    df = df.drop(['target',], axis=1)
    y = df[['Attack Type']]
    X = df.drop(['Attack Type',], axis=1)

    sc = MinMaxScaler()
    X = sc.fit_transform(X)

    # Split test and train data 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    return X_train, y_train

