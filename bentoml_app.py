import bentoml
import bentoml.sklearn
from bentoml.io import NumpyNdarray,PandasDataFrame
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
predictor = bentoml.sklearn.get("orderpredictor:lcjrxys4ewkvo6ty").to_runner()
service = bentoml.Service(
    "order_prediction", runners=[predictor]
)











@service.api(input=NumpyNdarray(),output=NumpyNdarray())
def predict(input: np.ndarray) -> np.ndarray:
    result = predictor.run(input)
    return np.array(result)

