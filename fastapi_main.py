from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from models import Reporter, Vehicle, Incident
from selenium_fill import fill_form
import json

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
async def submit_form(
    reporter: str = Form(...),
    vehicle: str = Form(...),
    incident: str = Form(...),
    proof_overview: UploadFile = File(...),
    proof_car: UploadFile = File(...)
):
    reporter_obj = Reporter.model_validate(json.loads(reporter))
    vehicle_obj = Vehicle.model_validate(json.loads(vehicle))
    incident_dict = json.loads(incident)
    incident_dict["proof_overview"] = await proof_overview.read()
    incident_dict["proof_car"] = await proof_car.read()
    incident_obj = Incident.model_validate(incident_dict)
    await fill_form(
        reporter=reporter_obj.model_dump(),
        vehicle=vehicle_obj.model_dump(),
        incident=incident_obj.model_dump()
    )
    return {"status": "success"}
