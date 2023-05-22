import pickle as pkl
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time

from multiapp import MultiApp
from apps import (cgpa_prediction)

#model = pkl.load(open("finalized_model.sav", "rb"))
#add_selectbox = st.sidebar.selectbox("Students Section",(["Select","Student Dashboard"]))

apps = MultiApp()

apps.add_app("CGPA Prediction System", cgpa_prediction.app)
apps.run()