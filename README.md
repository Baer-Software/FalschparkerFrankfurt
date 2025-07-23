# FalschparkerFrankfurt
Alternative technische Möglichkeit, Falschparker in Frankfurt anzuzeigen.

Sie können den folgenden cURL-Befehl verwenden, um den Endpunkt `/submit` zu testen. Ersetzen Sie die Dateipfade für `proof_overview.jpg` und `proof_car.jpg` durch tatsächliche Bilddateien auf Ihrem System.

```bash
curl -X POST "http://localhost:8000/submit" \
  -H "accept: application/json" \
  -F 'reporter={
    "salutation": "Herr",
    "last_name": "Mustermann",
    "first_name": "Max",
    "postal_code": "60311",
    "city": "Frankfurt",
    "street": "Musterstraße",
    "house_number": "1",
    "additional_info": "",
    "email": "max.mustermann@example.com",
    "phone_number": "0123456789"
  }' \
  -F 'vehicle={
    "model": "Golf",
    "color": "Blau",
    "license_plate": "FFM-AB123",
    "country": "Deutschland",
    "vehicle_type": "PKW",
    "manufacturer": "Volkswagen"
  }' \
  -F 'incident={
    "type": "Radweg/Radfahrstreifen",
    "duration": "Parken",
    "location_type": "auf einem Radweg (Zeichen 237).",
    "obstructed": "Ja",
    "obstruction_description": "Radweg komplett blockiert.",
    "location_description": "Musterstraße 1, 60311 Frankfurt",
    "date": "01.01.2024",
    "start_time": "12:00",
    "end_time": "12:30",
    "witnesses": [
      {
        "salutation": "Frau",
        "last_name": "Beispiel",
        "first_name": "Erika",
        "postal_code": "60311",
        "city": "Frankfurt",
        "street": "Nebenstraße",
        "house_number": "2",
        "additional_info": "",
        "email": "erika.beispiel@example.com",
        "phone_number": "0987654321"
      }
    ]
  }' \
  -F proof_overview=@/path/to/proof_overview.jpg \
  -F proof_car=@/path/to/proof_car.jpg
```
