from pydantic import BaseModel
from typing import Literal


class Witness(BaseModel):
    salutation: Literal["Herr", "Frau", "Mit geschlechtsneutraler Anrede"]
    last_name: str
    first_name: str
    postal_code: str
    city: str
    street: str
    house_number: str
    additional_info: str
    email: str
    phone_number: str

class Reporter(BaseModel):
    salutation: Literal["Herr", "Frau", "Mit geschlechtsneutraler Anrede"]
    last_name: str
    first_name: str
    postal_code: str
    city: str
    street: str
    house_number: str
    additional_info: str
    email: str
    phone_number: str

class Vehicle(BaseModel):
    model: str
    color: str
    license_plate: str
    country: Literal["Deutschland", "Österreich", "Schweiz"]
    vehicle_type: Literal["PKW", "LKW", "Bus", "Motorrad"]
    manufacturer: Literal["Audi", "BMW", "Mercedes-Benz", "Volkswagen", "Ford", "Opel", "Renault", "Peugeot", "Fiat", "Toyota", "Honda", "Nissan", "Mazda", "Subaru", "Suzuki", "Hyundai", "Kia", "Skoda", "Seat"]

class Incident(BaseModel):
    type: Literal["Radweg/Radfahrstreifen", "Gehweg/Fußgängerüberweg/Fußgängerfurt", "Haltverbot/Anlieger/Bewohner/Schwerbehindertenparkfläche/Elektrofahrzeuge", "Grünstreifen/Verkehrsinsel/Sperrfläche/Grenzmarkierung/verkehrsberuhigter Bereich", "Feuerwehrzufahrt", "Taxi/Haltestellen/zweite Reihe", "Bordsteinabsenkung/Grundstückszufahrten/Kreuzungen und Einmündungen"]
    duration: Literal["Halten", "Parken", "Parken länger als 1 Stunde"]
    location_type: Literal["auf einem Radweg (Zeichen 237).", "mit einem Kraftfahrzeug auf dem gemeinsamen Geh- und Radweg (Zeichen 240), der durch dieses Zeichen gesperrt war.", "mit einem Kraftfahrzeug auf dem Radweg eines getrennten Rad- und Gehwegs (Zeichen 241), der durch dieses Zeichen gesperrt war.", "auf einer Fahrradstraße (Zeichen 244.1).", "verbotswidrig auf einem Schutzstreifen für den Radverkehr (Zeichen 340)."]
    obstructed: Literal["Ja", "Nein"]
    obstruction_description: str
    location_description: str
    date: str
    start_time: str
    end_time: str
    witnesses: list[Witness] = []
    proof_overview: bytes
    proof_car: bytes
