import streamlit as st
from datasets import load_dataset
import pandas as pd

import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY') # Replace with your actual key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])  # Correct way to configure the API key


@st.cache_data  # Cache the data to avoid reloading on every interaction

def load_leetcode_data():
    """Loads and returns the leetcode dataset as a dictionary."""
    dataset = load_dataset("greengerong/leetcode")
    return dataset['train'].to_dict()

# Load the data (only once thanks to caching)
leetcode_data = load_leetcode_data()


# takes the problem number that the user selected
problemNumber = st.number_input("Problem #", min_value=0, max_value=878, value="min", step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
#gets content of leetcode problem.
content = leetcode_data['content'][problemNumber]
title = leetcode_data['title'][problemNumber]
#prompt for gemini
prompt = "Here is a problem from leetcode:  \n  " + content + "  \n  " + "  \n  ***Respond with only the code to solve the leetcode problem in the Leetcode solution format.***"
st.header(title)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt) # Use the 'prompt' variable you constructed

if response and hasattr(response, 'text'): # Check for valid response and 'text' attribute
    st.write(response.text) 
else:
    st.error("Could not generate a response.  Check the prompt and API configuration.")

st.write(os.environ())