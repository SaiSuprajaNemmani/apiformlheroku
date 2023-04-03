from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json


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
diabetes_model = pickle.load(open('diabetes_model.sav','rb'))

@app.get("/{name}")
def hello(name):
    return {"hello {} and welcome to this API".format(name)}

@app.route('/')
@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters : model_input):
  
    preg = json.dumps('Pregnancies')     
    glu = json.dumps('Glucose')
    bp = json.dumps('BloodPressure')
    skin = json.dumps('SkinThickness')
    insulin = json.dumps('Insulin')
    bmi = json.dumps('BMI')
    dpf = json.dumps('DiabetesPedigreeFunction')
    age = json.dumps('Age')

    input_list = [preg, glu, bp, skin, insulin, bmi, dpf, age]
    
    prediction = diabetes_model.predict([input_list])
    
    if prediction[0] == 0:
        return 'The person is not Diabetic'
    
    else:
        return 'The person is Diabetic'
