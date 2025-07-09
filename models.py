from pydantic import BaseModel
from typing import Literal

class Reporter(BaseModel):
    salutation: Literal["Herr", "Frau"]
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
    location_description: str
    date: str
    start_time: str
    end_time: str
