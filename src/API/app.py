from fastapi import FastAPI, File, Form
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
from io import StringIO

app = FastAPI()


class Features(BaseModel):
     Delivery_person_Ratings : float
     Restaurant_latitude : float
     Delivery_location_latitude: float
     Delivery_location_longitude :float
     Weatherconditions :  int
     Road_traffic_density : int
     Vehicle_condition :  int
     Type_of_order : int
     Type_of_vehicle :  int
     multiple_deliveries :  float
     Festival: int
     City :  int

@app.post('/predict')
async def estimate_time(features: Features):
    data =  features.dict()
    
    loaded_model = pickle.load(open('/Users/vicariousvision/Analytics Stuff/amazon_ml_challenge/src/models/model.pkl', 'rb'))
    data_in = { 0 : data['Delivery_person_Ratings' ], 1: data['Restaurant_latitude']  , 2: data['Delivery_location_latitude'], 3: data['Delivery_location_longitude'],4 :data['Weatherconditions'],5: data['Road_traffic_density'] ,6: data['Vehicle_condition'],7: data['Type_of_order'], 8:data['Type_of_vehicle'],9:data['multiple_deliveries'], 10: data['Festival'],11:data['City']}
    values_list = list(data_in.values())
    
    prediction = loaded_model.predict([values_list])
   
            
    return {
        'Estimated Time For Delivery': prediction,
        
    }

@app.post("/files/")
async def create_file(file: bytes = File(...), token: str = Form(...)):
    s=str(file,'utf-8')
    data = StringIO(s)
    df=pd.read_csv(data)
    print(df)
    #return df
    return {
        "file": df,
        "token": token,
    }