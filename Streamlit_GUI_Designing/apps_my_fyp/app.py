#dependencies
import sqlite3                   #python package for creating local database
import streamlit as slt          #python package for creating GUI    
import pandas as pd              #python package for data analysis
import hashlib                   #python package for encryption of the password
#dependency for creating multi-page streamlit application
from multiapp import MultiApp
from apps import (
    home,
    text_redactor,
    text_extractor,
    prod_review_analyzer,
    whatsapp_chat_analyzer,
    ner_tagging,
    resume_ranking,
    text_summarizer
)
#creating local database with name of 'users_db'
conn= sqlite3.connect('users_db.db')
# connecting to the data base
c = conn.cursor()
# creating user table
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
#adding users into the database
def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()
#finding loged-in user
def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data
#method for creating all the users
def view_all_users():
    c.execute("SELECT * FROM userstable")
    data=c.fetchall()
    return data
#method for pasword encryption
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

#application titile
slt.title("Text Analysis Application")
#login/signup menu
slt.sidebar.subheader("Login Menu")
menu=["Login","SignUp","Admin"]

choice=slt.sidebar.selectbox("Menu",menu)
#login options
if choice=="Login" or choice=="Admin":
    slt.sidebar.subheader("Login Section")
    username=slt.sidebar.text_input("Enter User Name")
    password=slt.sidebar.text_input("Enter Password",type='password')
    if slt.sidebar.checkbox("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result=login_user(username,check_hashes(password,hashed_pswd))
        if result:
            #adding sub-applications to the main applications
            apps = MultiApp()
            apps.add_app("Home", home.app)
            apps.add_app("Text Summarization", text_summarizer.app)
            apps.add_app("Named Entity Recognition", ner_tagging.app)
            apps.add_app("Text Redactor", text_redactor.app)
            apps.add_app("Text Extractor", text_extractor.app)
            apps.add_app("Resumes Ranking", resume_ranking.app)
            apps.add_app("Whatsapp Chat Analysis", whatsapp_chat_analyzer.app)
            apps.add_app("Reviews Sentiments Analysis", prod_review_analyzer.app)
            slt.sidebar.info("Welcome to Text Analysis Application")

            del password
            del username

            apps.run()
            #admin login
            if choice == "Admin":
                slt.sidebar.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                slt.sidebar.dataframe(clean_db)
        else:
            slt.sidebar.warning("Incorrect Username or Password")
#signup option
elif choice=="SignUp":
    slt.sidebar.subheader("Create New Account")
    new_user=slt.sidebar.text_input("Username")
    new_password=slt.sidebar.text_input("Password",type="password")
    if slt.sidebar.button("SignUp"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        slt.sidebar.success("Account Created Successfully")
        slt.sidebar.info("Goto To login Menu")
