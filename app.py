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

#use knn to display 3 restaurants for each day of the based on the budget and city selected
def get_restaurants(df, city, r_budget):
    df = df[df['location'] == city]
    df = df[df['R_price'] <= (r_budget)]
    df = df.sort_values(by='R_price', ascending=False)
    df = df[['R_name', 'R_price', 'R_rating']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df.iloc[:3]
    
def get_city(df, placetype):
    df = df[df['P_type'] == placetype]
    df = df.groupby('location').count().reset_index()
    df = df.sort_values(by='P_type', ascending=False)
    return df.iloc[0]['location']

def hotel_knn_model(df, city, h_budget):
    df = df[df['location'] == city]
    df = df[df['H_price'] <= (h_budget)]
    df = df.sort_values(by='H_price', ascending=False)
    df = df[['H_name', 'H_price', 'H_rating']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df = df.iloc[:3]
    return df
    
#use clustering to get the top 5 attractions in the city based on the type of attraction and rating
def get_attractions(df, city):
    df = df[df['location'] == city]
    df = df[['P_name', 'P_type', 'P_rating']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df = df.sort_values(by='P_rating', ascending=False)
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
            source_city=st.selectbox('Select the city you want to travel from -',df['location'].sort_values().unique())
            placetype=st.selectbox('Select the type of attractions you want to see -',df['P_type'].sort_values().unique())
            budget=st.slider('Select your Total budget', 0, 150000, 50000)
            days=st.slider('Select the duration of travel (days)', 0, 6, 2)
            submit_button=st.form_submit_button(label='Submit')
            
        if submit_button:
            flightcost=budget*0.25
            flightcost=round(flightcost, 2)
            r_budget=(budget*0.35)/days
            r_budget=round(r_budget, 2)
            h_budget=(budget-flightcost-r_budget)/days
            h_budget=round(h_budget, 2)
            
            st.write("### We reccomend you visit -")
            #display the city name in stylized format using markdown big font and bold text with red color
            city=get_city(df, placetype)
            st.markdown(f"""<span style="font-size: 40px; font-weight: bold; color: #eb4034;">{city}</span>""", unsafe_allow_html=True)
            st.write("### Your budget has been divided as follows -")
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Travel cost from {source_city} to {city} is (includes the flight/train and cab): </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;"><br>Rs. {flightcost}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Hotel Budget: </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;"><br>Rs. {h_budget}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 20px; font-weight: bold; color: #ffffff;">Food Budget: </span>"""f"""<span style="font-size: 20px; font-weight: bold; color: #ffd000;"><br>Rs. {r_budget}</span>""", unsafe_allow_html=True)
            
            
            
            st.write("### Here are the top 3 hotels we recommend:")
            df2=hotel_knn_model(df, city, h_budget)
            df2.columns=['Hotel Name', 'Price(/day)', 'Rating']
            #round the and rating to 2 decimal places
            df2['Rating']=df2['Rating'].apply(lambda x: round(x, 2))
            st.table(df2)
            
            st.write("### Top attractions of",city,":")
            new_attr=get_attractions(df, city)
            new_attr.columns=['Attraction Name', 'Type', 'Rating']
            st.table(new_attr)
            
            st.write("### Top restraunts of",city,":")
            st.write("#### Note: The price is for a family of 4")
            rest=get_restaurants(df, city, r_budget)
            rest.columns=['Restraunt Name', 'Price(/meal)', 'Rating']
            rest['Price(/meal)']=rest['Price(/meal)'].apply(lambda x: round(x, 2))
            st.table(rest)
            
            
        else:
            st.write("## Select a type of attraction to get started")
    except:
        st.write("## Wew")

page()