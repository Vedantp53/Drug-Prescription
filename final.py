import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf

df = pd.read_csv("dataset_main.csv")

new_df = pd.DataFrame(columns=df.columns, index=range(len(df)*2))
for i in range(len(df)):
    new_df.iloc[i*2] = df.iloc[i]
    new_df.iloc[i*2+1] = df.iloc[i]
   
new_df.to_csv('doubled_dataset.csv', index=False)

df = new_df

df = df.drop(columns=['alcohol','no_of_reviews','medical_condition','generic_name','side_effects','Symptom_5','Symptom_6','Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10'],axis=1)

num_labels=[]
for label, content in df.items():
    if pd.api.types.is_numeric_dtype(content):
      num_labels.append(label)

others = list(df.columns)

for i in num_labels:
  others.remove(i)

y = df['drug_name']
df.drop('drug_name',axis=1,inplace=True)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size = 0.2, random_state = 1)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(y)
Y_Train = le.transform(y_train)
Y_Train

others.remove('drug_name')

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
ct = make_column_transformer(
    (MinMaxScaler(), num_labels),
    (OneHotEncoder(handle_unknown='ignore'),others))

ct.fit(X_train)

X_train_ct = ct.transform(X_train)
# print("hello")

model = tf.keras.models.load_model("Disease_newly_UPDATED_Multimodel_prescription.h5")
# print("hi")

def Predict_pres(activity,rating,Disease,Symptom_1,Symptom_2,Symptom_3,Symptom_4, ct=ct,Model=model):
  predict= {
    "activity":[activity],
    # "Alcohol":[alcohol],
    "rating":[rating],
    # "no_of_riviews":[no_of_reviews],
    "Disease":[Disease],
    "Symptom_1":[Symptom_1],
    "Symptom_2":[Symptom_2],
    "Symptom_3":[Symptom_3],
    "Symptom_4":[Symptom_4]  
  }
  
  df = pd.DataFrame(predict)
  final_ct = ct.transform(df)
  Result = Model.predict(final_ct)
  result = Result.argmax(axis =1)
  return result

# print("final")
