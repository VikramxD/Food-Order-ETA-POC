import bentoml
from sklearn.base import BaseEstimator

model: BaseEstimator = bentoml.sklearn.load_model("/Users/vicariousvision/Analytics Stuff/amazon_ml_challenge/src/models/bentoml/models/best:ex6ry6s3x6rcm6ty")