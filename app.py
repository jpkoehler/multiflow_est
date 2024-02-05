from PIL import Image
import streamlit as st
import utils as utl

# Custom imports
from multipage import MultiPage
from src import correlations  # import your pages here

# Create an instance of the app


# Title of the main page
# st.title("Field Design")
utl.local_css("style.css")

correlations.app()