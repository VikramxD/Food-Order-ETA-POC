import json
import math
import streamlit as st
import deta
from deta import Deta
import requests
import numpy as np
import re


service_url = "http://127.0.0.1:3000/predict"



#deta = Deta(st.secrets["deta_key"])
#db = deta.Base("UserData")
st.write("## Order Prediction Appliction Frontend POC")
data = {}


def make_request_to_bentoml_service(service_url:str ,input_dict :dict)->str:
    serialized_input_data = {'data':input_dict}
    response = requests.post(
    service_url,
    data = serialized_input_data,
    headers = {"content-type":"application/json"}
    )
    return response.text



with st.form("my_form"):
    st.write("Provide the Following Information")
    data['Delivery_person_Ratings'] = st.number_input('Delivery_person_Ratings',min_value=1,max_value=5)
    data['Restaurant_latitude']= st.number_input('Restaurant_latitude')
    data['Delivery_location_latitude']= st.number_input('Delivery_location_latitude')
    data['Delivery_location_longitude'] = st.number_input('Delivery_location_longitude')
    data['Weatherconditions'] = st.number_input('Weatherconditions',min_value=0,max_value=5)
    data['Road_traffic_density'] = st.number_input('Road_traffic_density',min_value = 0, max_value=3)
    data['Type_of_order'] = st.number_input('Type_of_order',min_value=0,max_value=3)
    data['Type_of_vehicle'] = st.number_input('Type_of_vehicle',min_value=0,max_value=4)
    data['multiple_deliveries']= st.number_input('multiple_deliveries',min_value=0, max_value=3)
    data['Festival']= st.number_input('Festival',min_value=0 , max_value=1)
    data['City_Type']= st.number_input('City Type',min_value=0,max_value=4)
    submitted = st.form_submit_button('Submit')
    if submitted:
        st.write("Calculating ETA")
        prediction  = make_request_to_bentoml_service(service_url,input_dict=data)
        st.write(prediction)
        st.code(data)
        st.code([list(data.values())])

