# %%
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tqdm import tqdm
import random
import seaborn as sns
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import warnings
warnings.filterwarnings('ignore')

import os
import plotly.express as px

import xgboost as xg
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# %%

mydict= {'ID': list(),
 'Delivery_person_ID': list(),
 'Delivery_person_Age': list(),
 'Delivery_person_Ratings': list(),
 'Restaurant_latitude': list(),
 'Restaurant_longitude': list(),
 'Delivery_location_latitude': list(),
 'Delivery_location_longitude': list(),
 'Order_Date': list(),
 'Time_Orderd': list(),
 'Time_Order_picked': list(),
 'Weather': list(),
 'Road_traffic_density': list(),
 'Vehicle_condition': list(),
 'Type_of_order': list(),
 'Type_of_vehicle': list(),
 'multiple_deliveries': list(),
 'Festival': list(),
 'City': list(),
 'Time_taken': list(),
 'Name:': list()}

# %%
mydict_1= {'ID': list(),
 'Delivery_person_ID': list(),
 'Delivery_person_Age': list(),
 'Delivery_person_Ratings': list(),
 'Restaurant_latitude': list(),
 'Restaurant_longitude': list(),
 'Delivery_location_latitude': list(),
 'Delivery_location_longitude': list(),
 'Order_Date': list(),
 'Time_Orderd': list(),
 'Time_Order_picked': list(),
 'Weather': list(),
 'Road_traffic_density': list(),
 'Vehicle_condition': list(),
 'Type_of_order': list(),
 'Type_of_vehicle': list(),
 'multiple_deliveries': list(),
 'Festival': list(),
 'City': list(),
 'Name:': list()}

# %%
def get_train_data(path):
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            with open(os.path.join(dirname, filename),"r") as file:
                f=file.readlines()
                for i in range(len(f)):
                    k=list(f[i].split())
                    if k[0]== "Time_taken":
                        mydict[k[0]].append(k[2])
                    else:
                        mydict[k[0]].append(k[1])
    data = pd.DataFrame(mydict)
    data = data.drop(["Name:"],axis=1)
    return data

def get_test_data(path):
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            with open(os.path.join(dirname, filename),"r") as file:
                f=file.readlines()
                for i in range(len(f)):
                    k=list(f[i].split())
                    if k[0]== "Time_taken":
                        mydict_1[k[0]].append(k[2])
                    else:
                        mydict_1[k[0]].append(k[1])
    data = pd.DataFrame(mydict_1)
    data = data.drop(["Name:"],axis=1)
    return data

train = get_train_data("/Users/vikram/Python/Food-Order-ETA-POC/dataset/train")
test = get_test_data("/Users/vikram/Python/Food-Order-ETA-POC/dataset/test")

# %%
train.head()

# %%
train.info()

# %%
test.head()

# %%
test.info()

# %%
print(train.shape)
print(test.shape)

# %%
def get_NaN(data):
    for i in data.columns:
        counter=0
        for j in range(data.shape[0]):
            if data[i].iloc[j]=="NaN":
                counter+=1
            else:
                pass
        print(i,counter)
get_NaN(train)


# %%
get_NaN(test)

# %%
def check(data):
    month,year=[],[]
    for i in range(data.shape[0]):
        d=data["Order_Date"].iloc[i].split("-")
        month.append(d[1])
        year.append(d[2])
    print("Months",set(month))
    print("Year", set(year))
print("Train : ")
check(train)
print("Test : ")
check(test)

# %%
train["Festival"].value_counts()

# %%
test["Festival"].value_counts()

# %%
l=list(train[train.Festival=="Yes"].Order_Date)
l.extend(list(test[test.Festival=="Yes"].Order_Date))
holidays=list(set(l))
print("all the Festivals date")
holidays


# %%
def fill_NaN_festival(data):
    for i in range(data.shape[0]):
        if data["Festival"].iloc[i]=="NaN":
            if data["Order_Date"].iloc[i] in holidays:
                data["Festival"].iloc[i]="Yes"
            else:
                data["Festival"].iloc[i]="No"
        else:
            pass
    data["Festival"]=data["Festival"].astype('category')
fill_NaN_festival(train)
fill_NaN_festival(test)


# %%
train["Festival"].value_counts()


# %%
test["Festival"].value_counts()

# %%
def clean_multiple_deliveries(data):
    for i in tqdm(range(data.shape[0])):
        if data.multiple_deliveries.iloc[i] != "NaN":
            data.multiple_deliveries.iloc[i] = int(str(data.multiple_deliveries.iloc[i])[0])
            pass
        else:
            # replace NaN with 1
            data.multiple_deliveries.iloc[i] = 1
    data["multiple_deliveries"]=data["multiple_deliveries"].astype('int64')
clean_multiple_deliveries(train)
clean_multiple_deliveries(test)

# %%
def clean_delivery_person_age(data):
    for i in tqdm(range(data.shape[0])):
        if data.Delivery_person_Age.iloc[i] != "NaN":
            data.Delivery_person_Age.iloc[i] = int(str(data.Delivery_person_Age.iloc[i])[:2])
        else:
            # replace NaN with median
            data.Delivery_person_Age.iloc[i] = data.Delivery_person_Age.median()
            # replace NaN with mode
            #data.Delivery_person_Age.iloc[i] = data.Delivery_person_Age.mode()
#train["Delivery_person_Age"]=pd.to_numeric(train["Delivery_person_Age"], downcast='float')
clean_delivery_person_age(train)
clean_delivery_person_age(test)
train["Delivery_person_Age"]=train["Delivery_person_Age"].astype('int64')
test["Delivery_person_Age"]=test["Delivery_person_Age"].astype('int64')


# %%
def clean_Delivery_person_Ratings(data):
    mod = data.Delivery_person_Ratings.mode()
    for i in tqdm(range(data.shape[0])):
        #print(i)
        if data.Delivery_person_Ratings.iloc[i] != "NaN":
            data.Delivery_person_Ratings.iloc[i] = float(str(data.Delivery_person_Ratings.iloc[i])[:3])
        else:
            # replace NaN with median
            data.Delivery_person_Ratings.iloc[i] = data.Delivery_person_Ratings.median()
            
            #replace NaN with mode
            # data.Delivery_person_Ratings.iloc[i] = data.Delivery_person_Ratings.mode()
    data["Delivery_person_Ratings"]=pd.to_numeric(data["Delivery_person_Ratings"], downcast='float')
            
clean_Delivery_person_Ratings(train)
clean_Delivery_person_Ratings(test)

# %%
train[(train.City=="NaN") & (train.Road_traffic_density=="NaN")]

# %%
temp={ "Metropolitian" : ['Jam', 'Low', 'Medium'] ,
        "Urban" : ['Low' , 'Jam' , 'Medium'] ,
      "Semi-Urban" : ["Jam"]
}

def clean_Road_traffic_density(data):
    for i in tqdm(range(data.shape[0])):
        if data.Road_traffic_density.iloc[i] == 'NaN':
            if data.City.iloc[i] == 'Metropolitian':
                data.Road_traffic_density.iloc[i] = random.choice(temp['Metropolitian'])
            elif data.City.iloc[i] == 'Urban':
                data.Road_traffic_density.iloc[i] = random.choice(temp['Urban'])
            elif data.City.iloc[i] == 'Semi-Urban':
                data.Road_traffic_density.iloc[i] = random.choice(temp['Semi-Urban'])
            else:
                data.Road_traffic_density.iloc[i] = random.choice(temp['Metropolitian'])
        else:
            pass
    data["Road_traffic_density"]=data["Road_traffic_density"].astype('category')
clean_Road_traffic_density(train)
clean_Road_traffic_density(test)

# %%
t= test["ID"]

# %%
train = train.drop(["City", "Time_Orderd", "ID", "Delivery_person_ID"],axis=1)
test = test.drop(["City", "Time_Orderd", "ID", "Delivery_person_ID" ],axis=1)


# %%
def lat_long(data):
    """for i in tqdm(range(data.shape[0])):
        data["Restaurant_latitude"].iloc[i]= float(str(data["Restaurant_latitude"].iloc[i]))
        data["Restaurant_longitude"].iloc[i]= float(str(data["Restaurant_longitude"].iloc[i]))
        data["Delivery_location_latitude"].iloc[i]= float(str(data["Delivery_location_latitude"].iloc[i]))    
        data["Delivery_location_longitude"].iloc[i]= float(str(data["Delivery_location_longitude"].iloc[i]))
    """
    data["Restaurant_longitude"]=pd.to_numeric(data["Restaurant_longitude"], downcast='float')
    data["Delivery_location_latitude"]=pd.to_numeric(data["Delivery_location_latitude"], downcast='float')
    data["Delivery_location_longitude"]=pd.to_numeric(data["Delivery_location_longitude"], downcast='float')
    data["Restaurant_latitude"]=pd.to_numeric(data["Restaurant_latitude"], downcast='float')
lat_long(train)
lat_long(test)

# %%
train.info()

# %%
train.head()

# %%
train=train.drop(['Order_Date'],axis=1)
test=test.drop(['Order_Date'],axis=1)


# %%
def config_Time_Order_picked(data):
    for i in tqdm(range(data.shape[0])):
        data.Time_Order_picked.iloc[i] = float(str(data.Time_Order_picked.iloc[i]).replace(":","."))
    data["Time_Order_picked"]=pd.to_numeric(data["Time_Order_picked"], downcast='float')
config_Time_Order_picked(train)
config_Time_Order_picked(test)

# %%
def prepocess_Time_taken(data):
   
    data["Time_taken"]=pd.to_numeric(data["Time_taken"], downcast='integer')
prepocess_Time_taken(train)


# %%
def change_types(data):
    data["Weather"]=data["Weather"].astype('category')
    data["Vehicle_condition"]=data["Vehicle_condition"].astype('int64')
    data["Type_of_order"]=data["Type_of_order"].astype('category')
    data["Type_of_vehicle"]=data["Type_of_vehicle"].astype('category')
change_types(train)
change_types(test)

# %%
train.head()

# %%
train.info()

# %%
train=pd.get_dummies(train)
test=pd.get_dummies(test)

# %%
print(train.shape)
print(test.shape)

# %%
X,y = train.drop(["Time_taken"],axis=1),train["Time_taken"]

# %%
train_X, test_X, train_y, test_y = train_test_split(X, y,
                      test_size = 0.3, random_state = 123)

# %%
import xgboost as xgb
#=========================================================================
# XGBoost regression: 
# Parameters: 
# n_estimators  "Number of gradient boosted trees. Equivalent to number 
#                of boosting rounds."
# learning_rate "Boosting learning rate (also known as “eta”)"
# max_depth     "Maximum depth of a tree. Increasing this value will make 
#                the model more complex and more likely to overfit." 
#=========================================================================
regressor=xgb.XGBRegressor(eval_metric=r2_score)

#=========================================================================
# exhaustively search for the optimal hyperparameters
#=========================================================================
from sklearn.model_selection import GridSearchCV
# set up our search grid
param_grid = {"max_depth":    [5, 6, 7],
              "n_estimators": [800, 600, 700],
              "learning_rate": [0.01, 0.02,0.03,0.05,0.10,0.15]}

# try out every combination of the above values
search = GridSearchCV(regressor, param_grid, cv=5).fit(train_X, train_y)

print("The best hyperparameters are ",search.best_params_)


# %%
xgb_r = xg.XGBRegressor(n_estimators=800, max_depth=6, learning_rate = 0.02)

  
# Fitting the model
xgb_r.fit(train_X, train_y)
  
# Predict the model
pred = xgb_r.predict(test_X)
  
# RMSE Computation
r2= r2_score(test_y, pred)
print("r2_score : % f" %(r2))

# %%
result= {"ID":t, "Time_taken (min)":list(xgb_r.predict(test))}
res = pd.DataFrame(result)
res["Time_taken (min)"]=pd.to_numeric(res["Time_taken (min)"], downcast='float')
for i in tqdm(range(res.shape[0])):
    res["Time_taken (min)"].iloc[i]= round(float(round(res["Time_taken (min)"].iloc[i])),1)

# %%
res.head()

# %%
res.to_csv("result1.csv", index=False)


