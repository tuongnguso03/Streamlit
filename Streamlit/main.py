import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Uber pickups in NYC')

st.image("https://scontent.fhan2-3.fna.fbcdn.net/v/t39.30808-6/429749738_739324458295463_4085893500664758911_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=5f2048&_nc_ohc=p3MEeBRlbsUAX96R1hh&_nc_ht=scontent.fhan2-3.fna&oh=00_AfBWgrV6uELyPxTw_JNBA6Tw3c_NLe9R3qGHIRhwAgQomA&oe=65ECADDD")

st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

animal = st.text_input('Type an animal')
animal

import streamlit as st

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

with st.sidebar.form(key ='Form1'):
    user_word = st.text_input("Enter a keyword", "habs")  
    select_language = st.radio('Tweet language', ('All', 'English', 'French'))
    include_retweets = st.checkbox('Include retweets in data')
    num_of_tweets = st.number_input('Maximum number of tweets', 100)
    submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')

row1 = st.columns(3)
row2 = st.columns(3)

for col in row1 + row2:
    tile = col.container(height=120)
    tile.title(":balloon:"*15)

with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   print("spaap")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")