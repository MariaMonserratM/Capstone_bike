from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import uvicorn
import os


app = FastAPI()

model = None

class PredictionRequest(BaseModel):
    input: list

class PredictionResponse(BaseModel):
    prediction: list

def load_model():
    global model
    if model is None:
        model = joblib.load('model.pkl')


@app.get("/")
async def root():
    return {"message": "Welcome to our ML prediction algorithm! "}



@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    load_model()  # Ensure the model is loaded
   
    prediction = model.predict(request.input)
    return PredictionResponse(prediction=prediction.tolist())

@app.get("/healthcheck/")
def healthcheck():
    return 'Health - OK'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get('PORT', 8000))