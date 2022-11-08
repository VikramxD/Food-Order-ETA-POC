import streamlit as st
import deta
from deta import Deta





deta = Deta(st.secrets["deta_key"])
db = deta.Base("UserData")
st.write("## Order Prediction Appliction Frontend POC")

with st.form("my_form"):
   st.write("Provide the Following Information")
   Delivery_person_ID = st.text_input('Delivery_person_ID')
   Delivery_person_Age = st.number_input('Delivery_person_Age')
   Delivery_person_Ratings = st.number_input('Delivery_person_Ratings')
   Restaurant_latitude = st.number_input('Restaurant_latitude')
   Restaurant_longitude = st.number_input('Restaurant_longitude')
   Delivery_location_latitude = st.number_input('Delivery_location_latitude')
   Delivery_location_longitude = st.number_input('Delivery_location_longitude')
   Time_Order_picked = st.number_input('Time_Order_picked')
   Weatherconditions = st.text_input('Weatherconditions')
   Road_traffic_density = st.text_input('Road_traffic_density')
   Vehicle_condition = st.text_input('Vehicle_condition')
   Type_of_order = st.text_input('Type_of_order')
   Type_of_vehicle = st.text_input('Type_of_vehicle')
   multiple_deliveries = st.number_input('multiple_deliveries')
   Festival = st.text_input('Festival')
   City = st.text_input('City')
   Time_taken = st.number_input('Time_taken')
   pickup_time = st.number_input('pickup_time')
   submitted = st.form_submit_button('Submit')
if submitted:
    st.write("Calculating ETA")
    db.put({"key": 0 [Delivery_person_ID,Delivery_person_Age,Delivery_person_Ratings,Delivery_location_latitude,Delivery_location_longitude,Restaurant_latitude,Restaurant_longitude,Time_Order_picked,Weatherconditions,Road_traffic_density,Vehicle_condition,Type_of_order,Type_of_vehicle,multiple_deliveries,Festival,City,Time_taken,pickup_time]})




