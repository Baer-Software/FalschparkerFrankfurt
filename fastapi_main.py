from fastapi import FastAPI, UploadFile, File, Depends, Form
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from models import Reporter, Vehicle, Incident
from selenium_fill import fill_form
import json

app = FastAPI(
    title="Falschparker Frankfurt API",
    description="API to fill out the Falschparker form using Selenium.",
    version="1.0.0"
)

class ReporterForm(BaseModel):
    salutation: Literal["Herr", "Frau", "Mit geschlechtsneutraler Anrede"] = Field(..., description="Anrede der meldenden Person")
    last_name: str = Field(..., description="Nachname der meldenden Person")
    first_name: str = Field(..., description="Vorname der meldenden Person")
    postal_code: str = Field(..., description="Postleitzahl der meldenden Person")
    city: str = Field(..., description="Wohnort der meldenden Person")
    street: str = Field(..., description="Straße der meldenden Person")
    house_number: str = Field(..., description="Hausnummer der meldenden Person")
    additional_info: str = Field("", description="Adresszusatz (optional)")
    email: str = Field(..., description="E-Mail-Adresse der meldenden Person")
    phone_number: str = Field(..., description="Telefonnummer der meldenden Person")

    @classmethod
    def as_form(
        cls,
        salutation: Literal["Herr", "Frau", "Mit geschlechtsneutraler Anrede"] = Form(..., description="Anrede der meldenden Person"),
        last_name: str = Form(..., description="Nachname der meldenden Person"),
        first_name: str = Form(..., description="Vorname der meldenden Person"),
        postal_code: str = Form(..., description="Postleitzahl der meldenden Person"),
        city: str = Form(..., description="Wohnort der meldenden Person"),
        street: str = Form(..., description="Straße der meldenden Person"),
        house_number: str = Form(..., description="Hausnummer der meldenden Person"),
        additional_info: str = Form("", description="Adresszusatz (optional)"),
        email: str = Form(..., description="E-Mail-Adresse der meldenden Person"),
        phone_number: str = Form(..., description="Telefonnummer der meldenden Person")
    ):
        return cls(
            salutation=salutation,
            last_name=last_name,
            first_name=first_name,
            postal_code=postal_code,
            city=city,
            street=street,
            house_number=house_number,
            additional_info=additional_info,
            email=email,
            phone_number=phone_number
        )

class VehicleForm(BaseModel):
    model: str = Field(..., description="Fahrzeugmodell")
    color: str = Field(..., description="Farbe des Fahrzeugs")
    license_plate: str = Field(..., description="Kennzeichen des Fahrzeugs")
    country: Literal["Deutschland", "Österreich", "Schweiz"] = Field(..., description="Zulassungsland")
    vehicle_type: Literal["PKW", "LKW", "Bus", "Motorrad"] = Field(..., description="Fahrzeugtyp")
    manufacturer: Literal[
        "Alfa Lancia", "Alfa Romeo", "Aston Martin", "Audi", "Austin", "BMW", "Bugatti", "Chevrolet", "Chrysler",
        "Citroën", "Dacia", "Daewoo", "DAF", "Daihatsu", "Delta Motor", "Ferrari", "Fiat", "Ford", "General Motors",
        "Harley-Davidson", "Honda", "Husqvarna", "Hyundai", "Isuzu", "Iveco", "Jaguar", "Jeep", "Kässbohrer",
        "Kawasaki", "Kia", "Lamborghini", "Lancia", "MAN", "Maserati", "Mazda", "mbk", "Mercedes-Benz", "MG",
        "Mitsubishi", "Moto Guzzi", "Nissan", "Opel", "Peugeot", "Piaggio", "Pontiac", "Porsche", "Renault",
        "Rolls-Royce", "Rover", "Saab", "Samsung", "Scania", "Seat", "Skoda", "Smart", "Subaru", "Suzuki", "Tesla",
        "Toyota", "Vespa", "Volvo", "Volkswagen ", "Yamaha", "Sonstiges"
    ] = Field(..., description="Hersteller des Fahrzeugs")

    @classmethod
    def as_form(
        cls,
        model: str = Form(..., description="Fahrzeugmodell"),
        color: str = Form(..., description="Farbe des Fahrzeugs"),
        license_plate: str = Form(..., description="Kennzeichen des Fahrzeugs"),
        country: Literal["Deutschland", "Österreich", "Schweiz"] = Form(..., description="Zulassungsland"),
        vehicle_type: Literal["PKW", "LKW", "Bus", "Motorrad"] = Form(..., description="Fahrzeugtyp"),
        manufacturer: Literal[
            "Alfa Lancia", "Alfa Romeo", "Aston Martin", "Audi", "Austin", "BMW", "Bugatti", "Chevrolet", "Chrysler",
            "Citroën", "Dacia", "Daewoo", "DAF", "Daihatsu", "Delta Motor", "Ferrari", "Fiat", "Ford", "General Motors",
            "Harley-Davidson", "Honda", "Husqvarna", "Hyundai", "Isuzu", "Iveco", "Jaguar", "Jeep", "Kässbohrer",
            "Kawasaki", "Kia", "Lamborghini", "Lancia", "MAN", "Maserati", "Mazda", "mbk", "Mercedes-Benz", "MG",
            "Mitsubishi", "Moto Guzzi", "Nissan", "Opel", "Peugeot", "Piaggio", "Pontiac", "Porsche", "Renault",
            "Rolls-Royce", "Rover", "Saab", "Samsung", "Scania", "Seat", "Skoda", "Smart", "Subaru", "Suzuki", "Tesla",
            "Toyota", "Vespa", "Volvo", "Volkswagen ", "Yamaha", "Sonstiges"
        ] = Form(..., description="Hersteller des Fahrzeugs")
    ):
        return cls(
            model=model,
            color=color,
            license_plate=license_plate,
            country=country,
            vehicle_type=vehicle_type,
            manufacturer=manufacturer
        )

class WitnessForm(BaseModel):
    salutation: Literal["Herr", "Frau", "Mit geschlechtsneutraler Anrede"] = Field(..., description="Anrede der Zeug*in")
    last_name: str = Field(..., description="Nachname der Zeug*in")
    first_name: str = Field(..., description="Vorname der Zeug*in")
    postal_code: str = Field(..., description="Postleitzahl der Zeug*in")
    city: str = Field(..., description="Wohnort der Zeug*in")
    street: str = Field(..., description="Straße der Zeug*in")
    house_number: str = Field(..., description="Hausnummer der Zeug*in")
    additional_info: str = Field("", description="Adresszusatz der Zeug*in (optional)")
    email: str = Field(..., description="E-Mail-Adresse der Zeug*in")
    phone_number: str = Field(..., description="Telefonnummer der Zeug*in")

class IncidentForm(BaseModel):
    type: Literal[
        "Radweg/Radfahrstreifen",
        "Gehweg/Fußgängerüberweg/Fußgängerfurt",
        "Haltverbot/Anlieger/Bewohner/Schwerbehindertenparkfläche/Elektrofahrzeuge",
        "Grünstreifen/Verkehrsinsel/Sperrfläche/Grenzmarkierung/verkehrsberuhigter Bereich",
        "Feuerwehrzufahrt",
        "Taxi/Haltestellen/zweite Reihe",
        "Bordsteinabsenkung/Grundstückszufahrten/Kreuzungen und Einmündungen"
    ] = Field(..., description="Art des Verstoßes")
    duration: Literal["Halten", "Parken", "Parken länger als 1 Stunde"] = Field(..., description="Dauer des Verstoßes")
    location_type: Literal[
        "auf einem Radweg (Zeichen 237).",
        "mit einem Kraftfahrzeug auf dem gemeinsamen Geh- und Radweg (Zeichen 240), der durch dieses Zeichen gesperrt war.",
        "mit einem Kraftfahrzeug auf dem Radweg eines getrennten Rad- und Gehwegs (Zeichen 241), der durch dieses Zeichen gesperrt war.",
        "auf einer Fahrradstraße (Zeichen 244.1).",
        "verbotswidrig auf einem Schutzstreifen für den Radverkehr (Zeichen 340)."
    ] = Field(..., description="Art des Ortes")
    obstructed: Literal["Ja", "Nein"] = Field(..., description="Wurde jemand behindert?")
    obstruction_description: str = Field(..., description="Beschreibung der Behinderung")
    location_description: str = Field(..., description="Beschreibung des Ortes")
    date: str = Field(..., description="Datum des Vorfalls (YYYY-MM-DD)")
    start_time: str = Field(..., description="Startzeit des Vorfalls (HH:MM)")
    end_time: str = Field(..., description="Endzeit des Vorfalls (HH:MM)")
    witnesses: list[WitnessForm] = Field(default_factory=list, description="Liste der Zeug*innen")
    # proof_overview and proof_car are handled as files

    @classmethod
    def as_form(
        cls,
        type: Literal[
            "Radweg/Radfahrstreifen",
            "Gehweg/Fußgängerüberweg/Fußgängerfurt",
            "Haltverbot/Anlieger/Bewohner/Schwerbehindertenparkfläche/Elektrofahrzeuge",
            "Grünstreifen/Verkehrsinsel/Sperrfläche/Grenzmarkierung/verkehrsberuhigter Bereich",
            "Feuerwehrzufahrt",
            "Taxi/Haltestellen/zweite Reihe",
            "Bordsteinabsenkung/Grundstückszufahrten/Kreuzungen und Einmündungen"
        ] = Form(..., description="Art des Verstoßes"),
        duration: Literal["Halten", "Parken", "Parken länger als 1 Stunde"] = Form(..., description="Dauer des Verstoßes"),
        location_type: Literal[
            "auf einem Radweg (Zeichen 237).",
            "mit einem Kraftfahrzeug auf dem gemeinsamen Geh- und Radweg (Zeichen 240), der durch dieses Zeichen gesperrt war.",
            "mit einem Kraftfahrzeug auf dem Radweg eines getrennten Rad- und Gehwegs (Zeichen 241), der durch dieses Zeichen gesperrt war.",
            "auf einer Fahrradstraße (Zeichen 244.1).",
            "verbotswidrig auf einem Schutzstreifen für den Radverkehr (Zeichen 340)."
        ] = Form(..., description="Art des Ortes"),
        obstructed: Literal["Ja", "Nein"] = Form(..., description="Wurde jemand behindert?"),
        obstruction_description: str = Form(..., description="Beschreibung der Behinderung"),
        location_description: str = Form(..., description="Beschreibung des Ortes"),
        date: str = Form(..., description="Datum des Vorfalls (YYYY-MM-DD)"),
        start_time: str = Form(..., description="Startzeit des Vorfalls (HH:MM)"),
        end_time: str = Form(..., description="Endzeit des Vorfalls (HH:MM)"),
        witnesses: str = Form("[]", description="JSON-Liste von Zeug*innen, z.B. '[{\"salutation\": \"Herr\", ...}]'")
    ):
        try:
            witnesses_list = [WitnessForm(**w) for w in json.loads(witnesses)]
        except Exception:
            witnesses_list = []
        return cls(
            type=type,
            duration=duration,
            location_type=location_type,
            obstructed=obstructed,
            obstruction_description=obstruction_description,
            location_description=location_description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            witnesses=witnesses_list
        )

@app.post("/submit")
async def submit_form(
    reporter: Annotated[ReporterForm, Depends(ReporterForm.as_form)],
    vehicle: Annotated[VehicleForm, Depends(VehicleForm.as_form)],
    incident: Annotated[IncidentForm, Depends(IncidentForm.as_form)],
    proof_overview: UploadFile = File(..., description="Übersichtsbild als Beweis"),
    proof_car: UploadFile = File(..., description="Fahrzeugbild als Beweis")
):
    await fill_form(
        reporter=reporter.model_dump(),
        vehicle=vehicle.model_dump(),
        incident=incident.model_dump(),
        proof_overview=await proof_overview.read(),
        proof_car=await proof_car.read()
    )
    return {"status": "success"}
