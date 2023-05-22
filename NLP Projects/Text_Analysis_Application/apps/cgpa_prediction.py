import pickle as pkl
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time


def app():
   model = pkl.load(open("finalized_model.sav", "rb"))
   #with st.form("my_form", clear_on_submit=False):
   st.header("Enter Details")
   credit_hour = st.number_input("Enter study hours per week",min_value=15, max_value=30)
   sem1 = st.number_input("Enter GPA of  1st Semester",min_value=2.0, max_value=4.0)
   sem2 = st.number_input("Enter GPA of  2nd Semester",min_value=2.0, max_value=4.0)
   sem3 = st.number_input("Enter GPA of  3rd Semester",min_value=2.0, max_value=4.0)

   data = np.array([credit_hour, sem1, sem2, sem3]).reshape((1, -1))

   # Every form must have a submit button.
   #  submitted = st.form_submit_button("Submit")
   if st.button("Submit"):
      with st.spinner("Loading..."):
           time.sleep(1)
      res = model.predict(data)
      st.subheader(f"Predicted CPGA is {round(res[0], 3)}")



      x=["Cdt Hrs","Semester 1","Semester 2","Semester 3","CGPA"]
      y=[credit_hour,sem1,sem2,sem3,round(res[0], 3)]
      fig,ax=plt.subplots()
      ax.bar(x,y)
      for container in ax.containers:
         ax.bar_label(container)
      plt.title("Student Summary")
      st.pyplot(fig)

   #if add_selectbox=="Student Dashboard":
    #  st.title("Welcome to Students Section")