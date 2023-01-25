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
    df = df.iloc[:3]
    return df
    
#dictionary for each day of the trip with hours of the day as keys and the activities/restaurants as values
def itinerary(df, city, r_budget, days):
    itinerary = {}
    df = df[df['location'] == city]
    df = df.sort_values(by='R_price', ascending=False)
    df = df[['R_name', 'R_price', 'R_rating']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    #get the total number of restaurants in the city
    total_restaurants = df.shape[0]
    #get the number of restaurants to be visited in a day
    restaurants_per_day = int(total_restaurants / days)
    #get the total budget for restaurants in a day
    r_budget_per_day = r_budget / days
    #get the number of restaurants to be visited in a day based on the budget constraint
    restaurants_per_day = int(r_budget_per_day / df.iloc[0]['R_price'])
    #get the number of restaurants to be visited in a day based on the total number of restaurants in the city
    restaurants_per_day = min(restaurants_per_day, total_restaurants)
    #get the list of restaurants to be visited in a day
    restaurants_list = df.iloc[:restaurants_per_day]['R_name'].to_list()
    #get the list of timings for the restaurants
    restaurants_timings = ['12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']
    #get the timings for the restaurants based on the number of restaurants to be visited in a day
    restaurants_timings = restaurants_timings[:restaurants_per_day]
    #get the dictionary for the day with the timings as keys and the restaurants as values
    for i in range(len(restaurants_timings)):
        itinerary[restaurants_timings[i]] = restaurants_list[i]
    return itinerary
    
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
            source_city=st.selectbox('Select your source city',df['location'].sort_values().unique())
            placetype=st.selectbox('Select the type of attractions you want to see',df['P_type'].sort_values().unique())
            budget=st.slider('Select your Total budget', 0, 150000, 500)
            submit_button=st.form_submit_button(label='Submit')
            days=st.slider('Select the duration of travel', 0, 15, 5)
        if submit_button:
            flightcost=budget*0.25
            r_budget=budget*0.4
            h_budget=(budget-flightcost-r_budget)/days
            
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
            st.table(df2)
            
            st.write("### Here is your itinerary for the day:")
            itinerary_dict=itinerary(df, city, r_budget, days)
            df6=pd.DataFrame([itinerary_dict])
            #transpose the dataframe to get the timings as columns and the restaurants as rows
            df6=df6.T
            df6.columns=['Restaurant Name']
            st.write(df6)
            
        else:
            st.write("## Select a type of attraction to get started")
    except:
        st.write("## Wew")

page()