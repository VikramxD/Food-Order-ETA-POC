import bentoml
import bentoml.sklearn
from bentoml.io import NumpyNdarray,JSON
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd






predictor = bentoml.sklearn.get("orderpredictor:lcjrxys4ewkvo6ty").to_runner()
service = bentoml.Service(
    "order_prediction", runners=[predictor]
)


class Order_Features(BaseModel):
     Delivery_person_Ratings:float
     Restaurant_latitude:float
     Delivery_location_latitude:float
     Delivery_location_longitude:float
     Weatherconditions :int
     Road_traffic_density :int
     Type_of_order:int
     Type_of_vehicle:int
     multiple_deliveries:float
     Festival:int
     City_Type:int

input_specifications = JSON(pydantic_model=Order_Features)



@service.api(input=input_specifications, output=NumpyNdarray())
def predict(input_data: Order_Features) -> np.array:
    input_list = list(input_data.values())
    input_array = np.array(input_list)
    result = predictor.run(list(input_array))
    return result



