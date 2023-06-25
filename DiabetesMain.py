import tensorflow as tf
import sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

ct = make_column_transformer(
    (MinMaxScaler(), ['BMI', 'Income','PhysHlth','Age','GenHlth']),
    (OneHotEncoder(handle_unknown='ignore'),['HighBP','HighChol','Smoker','Stroke','HeartDiseaseorAttack','PhysActivity','Veggies','HvyAlcoholConsump','DiffWalk','Sex'])
)

diabetes = pd.read_csv("https://raw.githubusercontent.com/kuchbhi-kunal/nidan/main/diabetes_binary_5050split_health_indicators_BRFSS2015.csv")
diabetes.drop("Fruits",axis=1,inplace=True)
diabetes.drop("AnyHealthcare",axis=1,inplace=True)
diabetes.drop("NoDocbcCost",axis=1,inplace=True)
diabetes.drop("MentHlth",axis=1,inplace=True)
diabetes.drop("CholCheck",axis=1,inplace=True)
diabetes.drop("Education",axis=1,inplace=True)

X = diabetes.drop('Diabetes_binary',axis=1)
Y = diabetes['Diabetes_binary']

X_train, X_test, Y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42,stratify=Y)

ct.fit(X_train)

X_train_ct = ct.transform(X_train)

print(X_train_ct.shape)

model =  tf.keras.models.load_model("Diabetes_model_Binary_hdf5.h5")


def Predict_dia(BMI,Income,PhysHlth,Age,GenHlth,HighBP,HighChol,Smoker,Stroke,HeartDisease,PhysActivity,Veggies,HeavyAlcoholConsump,DiffWalk,Sex,ct=ct,Model=model):
    diagnose = {
        "BMI":[BMI],
        "Income":[Income],
        "PhysHlth":[PhysHlth],
        "Age":[Age],
        "GenHlth":[GenHlth],
        "HighBP":[HighBP],
        "HighChol":[HighChol],
        "Smoker":[Smoker],
        "Stroke":[Stroke],
        'HeartDiseaseorAttack':[HeartDisease],
        'PhysActivity':[PhysActivity],
        'Veggies':[Veggies],
        'HvyAlcoholConsump':[HeavyAlcoholConsump],
        'DiffWalk':[DiffWalk],
        'Sex':[Sex],
    }

    df = pd.DataFrame(diagnose)
    dia_ct=ct.transform(df)
    Result = Model.predict(dia_ct)

    result = Result.argmax(axis=1)
    return result
