import bentoml
import bentoml.sklearn
from bentoml.io import NumpyNdarray,PandasDataFrame,JSON
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd



predictor = bentoml.sklearn.get("orderpredictor:lcjrxys4ewkvo6ty").to_runner()
service = bentoml.Service(
    "order_prediction", runners=[predictor]
)


class Features(BaseModel):

    Delivery_person_Ratings: float 
    Restaurant_latitude: float
    Restaurant_longitude: float 
    Delivery_location_latitude:float 
    Delivery_location_longitude:float
    Weatherconditions:int 
    Road_traffic_density: float
    Vehicle_condition: int
    Type_of_order:int
    Type_of_vehicle:int
    multiple_deliveries:int
    Festival:int
    City_Type:int







@service.api(input=JSON(pydantic_model=Features),output=NumpyNdarray())
def predict(features: Features) -> np.ndarray:
    df = pd.DataFrame(features.dict(),index=[0])
    features_array = np.array(df)
    result = predictor.run(features_array)
    return result

