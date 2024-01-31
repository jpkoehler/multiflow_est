from PIL import Image
import streamlit as st
import utils as utl

# Custom imports
from multipage import MultiPage
from pages import equipment  # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
# st.title("Field Design")
utl.local_css("style.css")

app.add_page("Chen Correlation", equipment.app)

# The main app
app.run()
