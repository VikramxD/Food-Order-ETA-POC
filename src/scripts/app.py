import json
import math
import streamlit as st
import deta
from deta import Deta
import requests


API_ENDPOINT = "http://127.0.0.1:3000/predict"

deta = Deta(st.secrets["deta_key"])
db = deta.Base("UserData")
st.write("## Order Prediction Appliction Frontend POC")
data = {

}

with st.form("my_form"):

   st.write("Provide the Following Information")
   #data["Delivery_person_ID"] = st.text_input('Delivery_person_ID')
   data["Delivery_person_Ratings"] = st.number_input('Delivery_person_Ratings',min_value=1,max_value=5)
   data["Restaurant_latitude" ]= st.number_input('Restaurant_latitude')
   data["Restaurant_longitude"] = st.number_input('Restaurant_longitude')
   data["Delivery_location_latitude"] = st.number_input('Delivery_location_latitude')
   data["Delivery_location_longitude"] = st.number_input('Delivery_location_longitude')
   data["Weatherconditions"] = st.number_input('Weatherconditions',min_value=0,max_value=5)
   data["Road_traffic_density"] = st.number_input('Road_traffic_density',min_value = 0, max_value=3)
   data["Vehicle_condition"] = st.number_input('Vehicle_condition',min_value = 0,max_value=3)
   data["Type_of_order"] = st.number_input('Type_of_order',min_value=0,max_value=3)
   data["Type_of_vehicle"] = st.number_input('Type_of_vehicle',min_value=0,max_value=4)
   data["multiple_deliveries"] = st.number_input('multiple_deliveries',min_value=0, max_value=3)
   data["Festival"] = st.number_input('Festival',min_value=0 , max_value=1)
   data["City_Type"] = st.number_input('City Type',min_value=0,max_value=4)
  




   submitted = st.form_submit_button('Submit')
if submitted:
    st.write("Calculating ETA")
    #db.insert([Delivery_person_ID,Delivery_person_Age,Delivery_person_Ratings,Delivery_location_latitude,Delivery_location_longitude,Restaurant_latitude,Restaurant_longitude,Time_Order_picked,Weatherconditions,Road_traffic_density,Vehicle_condition,Type_of_order,Type_of_vehicle,multiple_deliveries,Festival,City,Time_taken,pickup_time])
    data_json = json.dumps(data)
    prediction = requests.post(
            API_ENDPOINT,
            headers={"content-type": "application/json"},
            data=data_json, 
        ).text
    st.write(f"The Estimated Time of Arrival would be  {prediction} minutes" )
    st.write(data_json)
