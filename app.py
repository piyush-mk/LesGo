import streamlit as st
st.set_page_config(page_title="LesGo | Travel itinerary maker", page_icon="🏝️", layout="centered", initial_sidebar_state="auto", menu_items=None)
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import streamlit.components.v1 as components
# streamlit app to create a travel itinerary based on location and budget constraints
# data
def load_data():
    df = pd.read_csv('data/joined_data.csv')
    return df
df=load_data()
#return one city name based on the highest count of the particular type of attraction in the city from the placetype csv
    
def get_city(df, placetype):
    df = df[df['P_type'] == placetype]
    df = df.groupby('location').count().reset_index()
    df = df.sort_values(by='P_type', ascending=False)
    return df.iloc[0]['location']

# knn model to recommend the top 5 hotels based on the location, budget and the rating of the hotel
def hotel_knn_model(df, city, h_budget):
    df = df[df['location'] == city]
    df = df[df['H_price'] <= (h_budget)]
    df = df.sort_values(by='H_price', ascending=False)
    df = df[['H_name', 'H_price', 'H_rating']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df = df.iloc[:5]
    return df
    

def page():
    st.markdown("""
    <style>
    .css-15zrgzn {display: none}
    </style>
    """, unsafe_allow_html=True)
    title=st.title("LesGo | Travel itinerary maker")
    st.write("## Create your travel itinerary based on location and budget constraints")
    #catch nan error for the form
    try:
        with st.form(key='myform'):
            placetype=st.selectbox('Select the type of attractions you want to see',df['P_type'].sort_values().unique())
            budget=st.slider('Select your Total budget', 0, 150000, 500)
            submit_button=st.form_submit_button(label='Submit')
            days=st.slider('Select the duration of travel', 0, 15, 5)
        if submit_button:
            flightcost=budget*0.4
            r_budget=budget*0.1
            h_budget=(budget-flightcost-r_budget)/days
            
            st.write("### We reccomend you visit -")
            #display the city name in stylized format using markdown big font and bold text with red color
            city=get_city(df, placetype)
            st.markdown(f"""<span style="font-size: 40px; font-weight: bold; color: #eb4034;">{city}</span>""", unsafe_allow_html=True)
            st.write("### Your budget has been divided as follows:")
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Flight Budget: </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;">Rs. {flightcost}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Hotel Budget: </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;">  Rs. {h_budget}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Food Budget: </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;"> Rs. {r_budget}</span>""", unsafe_allow_html=True)
            
            
            
            st.write("### Here are the top 5 hotels we recommend:")
            df2=hotel_knn_model(df, city, h_budget)
            df2.columns=['Hotel Name', 'Price(/day)', 'Rating']
            st.table(df2)
        else:
            st.write("## Select a type of attraction to get started")
    except:
        st.write("## Wew")

page()