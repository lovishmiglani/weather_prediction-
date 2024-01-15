from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class InputData(BaseModel):
    precipitation: float
    temp_max: float
    temp_min: float
    wind: float
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
@app.post("/letspredict")
async def predict_weather(data: InputData):
    try:
        # Load the pre-trained model
        model = pickle.load(open("Weather_Prediction_ensemble_model.pkl", "rb"))

        # Prepare the input data for prediction
        input_data = np.array([[data.precipitation, data.temp_max, data.temp_min, data.wind]])

        # Make predictions
        prediction = model.predict(input_data)

        # Map predictions to weather categories
        weather_mapping = {0: 'Drizzle', 1: 'Fog', 2: 'Rain', 3: 'Snow', 4: 'Sun'}
        weather_result = weather_mapping.get(prediction[0])

        return {"prediction": weather_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
