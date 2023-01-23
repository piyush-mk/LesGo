import streamlit as st
st.set_page_config(page_title="Travel itinerary maker", layout="wide")
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
# streamlit app to create a travel itinerary based on location and budget constraints
# data
def load_data():
    df = pd.read_csv('joined_data.csv')
    return df

data=load_data()

