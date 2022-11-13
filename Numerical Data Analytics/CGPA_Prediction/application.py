import pickle as pkl
import numpy as np
import streamlit as st

model = pkl.load(open("finalized_model.sav", "rb"))

st.title("CGPA Prediction")

with st.form("my_form", clear_on_submit=True):
   st.header("Enter Details")
   hour = st.number_input("Enter study hours per week")
   sem1 = st.number_input("Enter Semester 1 GPA")
   sem2 = st.number_input("Enter Semester 2 GPA")
   sem3 = st.number_input("Enter Semester 3 GPA")

   data = np.array([hour, sem1, sem2, sem3]).reshape((1, -1))
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       res = model.predict(data)
       st.subheader(f"Predicted CPGA is {round(res[0], 3)}")
