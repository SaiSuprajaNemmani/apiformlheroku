# -*- coding: utf-8 -*-
"""

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
import asyncio


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    
    Pregnancies : int
    Glucose : int
    BloodPressure : int
    SkinThickness : int
    Insulin : int
    BMI : float
    DiabetesPedigreeFunction :  float
    Age : int
    

# loading the saved model
async def read_file():
    async with open('diabetes_model.sav','rb') as file:
        diabetes_model = await file.read()
        delay = 5
        await asyncio.sleep(delay)
        print(diabetes_model) 

asyncio.run(read_file())

@app.get("/{name}")
def hello(name):
    return {"hello {} and welcome to this API".format(name)}

@app.route('/')
@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters : model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.load(input_data)
    
    preg = input_dictionary['Pregnancies']
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    skin = input_dictionary['SkinThickness']
    insulin = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    dpf = input_dictionary['DiabetesPedigreeFunction']
    age = input_dictionary['Age']


    input_list = [preg, glu, bp, skin, insulin, bmi, dpf, age]
    
    prediction =  diabetes_model.predict([input_list])
    
    if prediction[0] == 0:
        return 'The person is not Diabetic'
    
    else:
        return 'The person is Diabetic'

if __name__=="__main__":
    uvicorn.run(app)
