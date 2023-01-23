import streamlit as st
st.set_page_config(page_title="LesGo | Travel itinerary maker", page_icon=":desert island:", layout="centered", initial_sidebar_state="auto", menu_items=None)
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import streamlit.components.v1 as components
# streamlit app to create a travel itinerary based on location and budget constraints
# data
def load_data():
    df1 = pd.read_csv('data/joined_data.csv')
    return df1

df=load_data()

# k nearest neigbour model to take in location and budget and return top 5 recommendations based on distance, price of hotel and rating

def knn_model(df,location,budget):
    df1=df.copy()
    df1=df1[df1['location']==location]
    df1=df1[df1['H_price']<=budget]
    df1=df1[['H_name','H_price','H_rating','distance','location','R_name','R_rating']]
    df1=df1.dropna()
    df1=df1.reset_index(drop=True)
    X=df1[['distance','R_rating']]
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='kd_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    return df1.iloc[indices[0]]

def page():
    title=st.title("LesGo | Travel itinerary maker")
    st.write("This app will help you create a travel itinerary based on your location and budget constraints")
    st.markdown("##")
    with st.form(key='my_form'):
        location=st.selectbox('Select your location',df['location'].unique())
        budget=st.slider('Select your budget',min_value=0,max_value=30000,step=100)
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        st.write('Here are top 5 recommendations based on your location and budget constraints')
        st.markdown("##")
        knn_model(df,location,budget)
        #write the recommendations in a new dataframe and display it as a table in streamlit
        #change the column names to make it more readable
        df2=knn_model(df,location,budget)
        df2.drop(['distance','location'],axis=1,inplace=True)
        df2.columns=['Hotel name','Hotel price(/day)','Hotel rating','Restaurant name','Restaurant rating']
        df2=df2.reset_index(drop=True)
        st.table(df2)
        
    else:
        st.write('Please select your location and budget')
    st.markdown("##")

page()