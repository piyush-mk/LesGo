import streamlit as st
st.set_page_config(page_title="LesGo | Travel itinerary maker", page_icon="🏝️", layout="centered", initial_sidebar_state="auto", menu_items=None)
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import streamlit.components.v1 as components
# streamlit app to create a travel itinerary based on location and budget constraints
# data
def load_data():
    df1 = pd.read_csv('data/joined_data.csv')
    return df1

# knn model to generate recommendation for one hotel and three restaurants for breakfast lunch and dinner ranked by rating based on user input of location and budget