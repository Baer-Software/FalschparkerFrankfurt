from fastapi import FastAPI
from pydantic import BaseModel
from models import Reporter, Vehicle, Incident
from selenium_fill import fill_form

app = FastAPI(
    title="Falschparker Frankfurt API",
    description="API to fill out the Falschparker form using Selenium.",
    version="1.0.0"
)

class FormData(BaseModel):
    reporter: Reporter
    vehicle: Vehicle
    incident: Incident

@app.post("/submit")
def submit_form(data: FormData):
    # Convert Pydantic models to dicts for fill_form
    fill_form(
        reporter=data.reporter.model_dump(),
        vehicle=data.vehicle.model_dump(),
        incident=data.incident.model_dump()
    )
    return {"status": "success"}

