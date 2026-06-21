# 🚀 FastAPI CRUD Application with Streamlit Frontend

> **Live Demo:** https://insurance-frontend-gcol.onrender.com/
>
> **Backend API:** https://render-demo-smitzz.onrender.com/


---

# 📌 Project Overview

This project demonstrates a complete **FastAPI CRUD application** integrated with a **Streamlit frontend** and deployed on **Render**.



# 🏗️ Project Architecture

```text
┌──────────────┐
│   Streamlit  │
│   Frontend   │
└──────┬───────┘
       │ HTTP Request
       ▼
┌──────────────┐
│   FastAPI    │
│   Backend    │
└──────┬───────┘
       │
       ▼
 ┌────────────┐
 │ Data Layer │
 └────────────┘
```

---

## What is FastAPI?

FastAPI is a modern Python web framework used for building APIs.

### Features

✅ High Performance

✅ Automatic Swagger Documentation

✅ Type Validation

✅ Async Support

✅ Easy Integration with ML Models

---

# FastAPI Application Structure

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Hello World"}
```

### Key Components

| Component     | Purpose              |
| ------------- | -------------------- |
| FastAPI()     | Creates API instance |
| @app.get()    | GET endpoint         |
| @app.post()   | POST endpoint        |
| @app.put()    | UPDATE endpoint      |
| @app.delete() | DELETE endpoint      |

---

# 🔄 CRUD Operations Revision

CRUD =

| Operation | HTTP Method |
| --------- | ----------- |
| Create    | POST        |
| Read      | GET         |
| Update    | PUT         |
| Delete    | DELETE      |

---

## 1️⃣ CREATE

Used to insert new data.

```python
@app.post("/items")
def create_item(item: Item):
    return item
```

### Notes

* Receives data from request body
* Uses Pydantic model validation
* Returns created object

---

## 2️⃣ READ

Used to fetch data.

```python
@app.get("/items")
def get_items():
    return items
```

### Notes

* No data modification
* Most common endpoint
* Returns JSON response

---

## 3️⃣ UPDATE

Used to modify existing records.

```python
@app.put("/items/{id}")
def update_item(id: int):
    pass
```

### Notes

* Uses Path Parameters
* Updates existing record

---

## 4️⃣ DELETE

Used to remove data.

```python
@app.delete("/items/{id}")
def delete_item(id: int):
    pass
```

### Notes

* Removes resource permanently
* Usually returns success message

---

# 🧠 Pydantic Model 

```python
from pydantic import BaseModel

class User(BaseModel):
    age:int
    salary:float
    city:str
```

### Why Pydantic?

* Data Validation
* Type Checking
* Automatic Serialization

Example:

```json
{
    "age":25,
    "salary":50000,
    "city":"Raipur"
}
```

---

# 📍 Path Parameters

```python
@app.get("/user/{id}")
def get_user(id:int):
    return id
```

URL:

```text
/user/10
```

Output:

```json
10
```

---

# 📍 Query Parameters

```python
@app.get("/search")
def search(name:str):
    return name
```

URL:

```text
/search?name=sumeet
```

---

# 📍 Request Body

```python
@app.post("/predict")
def predict(data: User):
    return data
```

FastAPI automatically converts JSON → Python Object.

---

# 🌐 Streamlit Frontend

The frontend is built using Streamlit.

### Responsibilities

* User Input Collection
* Form Submission
* Calling FastAPI Endpoint
* Displaying Results

Example Flow:

```python
response = requests.post(
    API_URL,
    json=user_data
)
```

---

# 🔗 Frontend ↔ Backend Flow

```text
User Input
     │
     ▼
Streamlit Form
     │
 POST Request
     ▼
FastAPI Endpoint
     │
 Prediction / CRUD Logic
     ▼
JSON Response
     │
     ▼
Streamlit UI
```

---

# 🚀 Deployment on Render

## Backend Deployment

1. Push code to GitHub
2. Create Web Service in Render
3. Connect Repository
4. Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Frontend Deployment

Create another Web Service.

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0
```

---


# 🎯 FastAPI Interview Revision Sheet

### FastAPI vs Flask

| FastAPI         | Flask     |
| --------------- | --------- |
| Async Support   | Limited   |
| Type Validation | Built-in  |
| Swagger Docs    | Automatic |
| Faster          | Slower    |

---

### Common Interview Questions

#### Why use FastAPI?

* High performance
* Easy API development
* Auto documentation
* Validation using Pydantic

---

#### Difference between PUT and PATCH?

PUT

* Replaces complete resource

PATCH

* Updates specific fields

---

#### What is Pydantic?

A validation library used by FastAPI to validate incoming request data.

---

#### What are Path Parameters?

Parameters passed directly in URL.

Example:

```text
/employee/5
```

---

#### What are Query Parameters?

Parameters passed after `?`.

Example:

```text
/search?name=sumeet
```



