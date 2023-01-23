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
    df1 = pd.read_csv('joined_data.csv')
    return df1

df=load_data()

# k nearest neigbour model to take in location and budget and return top 5 recommendations based on distance, price of hotel and rating

def knn_model(df,location,budget):
    df1=df.copy()
    df1=df1[df1['city']==location]
    df1=df1[df1['price']<=budget]
    df1=df1[['name','price','rating','distance','city']]
    df1=df1.dropna()
    df1=df1.reset_index(drop=True)
    X=df1[['distance','price','rating']]
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    return df1.iloc[indices[0]]

def page():
    title=st.title("Travel itinerary maker")
    st.write("This app will help you create a travel itinerary based on your location and budget constraints")
    st.markdown("##")
    with st.form(key='my_form'):
        location=st.selectbox('Select your location',df['city'].unique())
        budget=st.slider('Select your budget',min_value=0,max_value=150000,step=100)
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        st.write('Here are your top 5 recommendations')
        st.markdown("##")
        knn_model(df,location,budget)
        st.write(knn_model(df,location,budget))
        
    else:
        st.write('Please select your location and budget')
    st.markdown("##")

page()