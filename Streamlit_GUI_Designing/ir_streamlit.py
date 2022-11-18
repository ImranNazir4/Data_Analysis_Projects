import streamlit as st
import pandas as pd
# from pdf2image import convert_from_path
# import easyocr
import numpy as np
import PIL
from PIL import Image
# from PIL import ImageDraw
# import spacy



st.title('Custom Information Retrieval')

col1,col2=st.columns(2)
with col1:
	st.subheader('Create Sample')
	st.text_area('Add Variables Here')
with col2:
	st.subheader('Input Overview')



uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
	st.image(uploaded_file)
    # image = Image.open(uploaded_file)
