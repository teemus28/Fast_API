from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
from fastapi.responses import JSONResponse

app = FastAPI()

# create class
class patient(BaseModel):
    id:Annotated[str, Field(...,description = 'Id of the patient', examples = ['P001'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City in which patient is living")]
    age:Annotated[int,Field(..., gt=0, lt=120, description="Age of the patient")]
    gender:Annotated[Literal['male','female','other'],
                     Field(...,description = 'Gender of patient')]
    height:Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight:Annotated[float, Field(..., gt=0, description="Weight of the patient in Kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Overweight'
        else:
            return "Obese"
    
# update class - all fields are optional
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# CRUD operations 
# 1. create - post method
# 2. retrive - get method
# 2. update - put method
# 4. delete - delete method 

@app.get("/")
def greet():
    return {'message':"Welcome to patients record system"}

@app.get("/about")
def about():
    return {"message":"It was a very useful app to maintain patients records"}

@app.get('/view')
def view():
    data = load_data()
    return data

# create
@app.post('/create')
def create_patient(patient:patient):  #pydantic base class ad datatype
        # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


#3 update method - put
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

# delete
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})



# CTRL+S ->  uvicorn patients:app -- reload  -> CTRL+C (cut terminal)
# for installing library - python -m pip install ...

