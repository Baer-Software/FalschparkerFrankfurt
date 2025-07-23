from playwright.async_api import async_playwright
import tempfile
import os
import asyncio

async def fill_form(reporter, vehicle, incident):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://portal-civ.ekom21.de/civ.public/start.html?oe=00.00.PA.FFOrdA&mode=cc&cc_key=AnzeigeOwi")

        async def fill_by_label(label, input_value, filter_selector=None):
            if filter_selector:
                label_elem = page.locator(f"{filter_selector} label:text-is('{label}')")
            else:
                label_elem = page.locator(f"label:text-is('{label}')")
            input_id = await label_elem.get_attribute("for")
            await page.locator(f"#{input_id}").fill(input_value)

        async def custom_select(option):
            select_elem = page.locator(f"select:has(option:text-is('{option}'))")
            select_elem = await select_elem.evaluate_handle("el => el.nextElementSibling")
            await select_elem.click()
            await page.locator(f"li:text-is('{option}')").click()

        async def next_btn():
            await page.locator("button:has(span:text('Weiter'))").click()

        await next_btn()
        await page.locator(".civ-servicekonto-border-top .civ-servicekonto-radio-label").click()
        await next_btn()

        # Reporter group
        await custom_select(reporter['salutation'])
        await fill_by_label('Name', reporter['last_name'])
        await fill_by_label('Vorname', reporter['first_name'])
        await fill_by_label('Postleitzahl', reporter['postal_code'])
        await fill_by_label('Ort', reporter['city'])
        await fill_by_label('Straße/Postfach', reporter['street'])
        await fill_by_label('Nr.', reporter['house_number'])
        await fill_by_label('Zusatz', reporter['additional_info'])
        await fill_by_label('E-Mail-Adresse', reporter['email'])
        await fill_by_label('E-Mail-Adresse bestätigen', reporter['email'])
        await fill_by_label('Telefonnummer', reporter['phone_number'])
        await next_btn()

        # Vehicle group
        await fill_by_label('Fahrzeugmodell', vehicle['model'])
        await fill_by_label('Farbe', vehicle['color'])
        label_kz = page.locator("label:text-is('Kennzeichen'):not(:text-is('Land'))")
        input_id = await label_kz.get_attribute("for")
        await page.locator(f"#{input_id}").fill(vehicle['license_plate'])
        await custom_select(vehicle['country'])
        await custom_select(vehicle['vehicle_type'])
        await custom_select(vehicle['manufacturer'])
        await page.locator(f"label:text-is('{incident['type']}')").click()
        await next_btn()

        # Incident group
        await page.locator(f"label:text-is('{incident['duration']}')").click()
        await page.locator(f"span:text-is('{incident['location_type']}')").click()
        await page.locator(f"label:text-is('{incident['obstructed']}')").click()
        if incident['obstructed'] == 'Ja':
            await fill_by_label('Bitte beschreiben Sie die Behinderung.', incident['obstruction_description'])
        await next_btn()

        await fill_by_label('Tatort - Straße und Hausnummer, eventuell Konkretisierung', incident['location_description'])
        await fill_by_label('Tattag (Datum)', incident['date'])
        await fill_by_label('Tatzeit (Zeitpunkt)', incident['start_time'])
        # await fill_by_label('Ende Tatzeit', incident['end_time']) # Uncomment if needed
        await page.locator('body').click()
        tattag_label = page.locator(f"label:text-is('Tattag (Datum)')")
        tattag_element_id = await tattag_label.get_attribute("for")
        await page.locator(f"#{tattag_element_id}").click()
        await page.locator('body').click()
        tattag_label = page.locator(f"label:text-is('Tattag (Datum)')")
        tattag_element_id = await tattag_label.get_attribute("for")
        await page.locator(f"#{tattag_element_id}").click()
        await page.locator('.datePickerDayIsValue').click()

        # Witnesses (optional)
        witnesses = incident.get('witnesses', [])
        witness_selector = "div:has(h2:text-is('Angaben zu weiteren Zeugen bearbeiten'))"
        for witness in witnesses:
            await page.locator("button:has(span:text('Eintrag hinzufügen'))").click()
            await page.wait_for_selector("h2:text-is('Angaben zu weiteren Zeugen bearbeiten')")
            await custom_select(witness['salutation'])
            await fill_by_label('Name', witness['last_name'], filter_selector=witness_selector)
            await fill_by_label('Vorname', witness['first_name'], filter_selector=witness_selector)
            await fill_by_label('PLZ', witness['postal_code'], filter_selector=witness_selector)
            await fill_by_label('Ort', witness['city'], filter_selector=witness_selector)
            await fill_by_label('Strasse', witness['street'], filter_selector=witness_selector)
            await fill_by_label('Hausnummer', witness['house_number'], filter_selector=witness_selector)
            await fill_by_label('Hausnummerzusatz', witness['additional_info'], filter_selector=witness_selector)
            await fill_by_label('E-Mail', witness['email'], filter_selector=witness_selector)
            await fill_by_label('Telefonnummer', witness['phone_number'], filter_selector=witness_selector)
            await page.locator("button:has(span:text('Übernehmen'))").click()

        # Upload images for proof_overview and proof_car
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as overview_file:
            overview_file.write(incident['proof_overview'])
            overview_path = overview_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as car_file:
            car_file.write(incident['proof_car'])
            car_path = car_file.name

        await page.locator('button[aria-label="Beweis-Übersichtsfoto (erforderlich) Hochladen"]').click()
        file_input = page.locator('input[type="file"]').last
        await file_input.wait_for(state="attached")
        await file_input.set_input_files(overview_path)

        await asyncio.sleep(5)

        await page.locator('button[aria-label="Beweis-Fahrzeugfoto (erforderlich) Hochladen"]').click()
        car_file_input = page.locator('input[type="file"]').last
        await car_file_input.wait_for(state="attached")
        await car_file_input.set_input_files(car_path)

        labels = page.locator('label:text-is("Dateiname")')
        await labels.nth(0).wait_for(state="visible")
        await labels.nth(1).wait_for(state="visible")

        await next_btn()

        await page.locator("label:text-is('Ich versichere die Richtigkeit und Vollständigkeit meiner gemachten Angaben. Mir ist bewusst, dass ich als Zeuge oder Zeugin zur wahrheitsgemäßen Angabe verpflichtet bin (§ 57 Strafprozessordnung in Verbindung mit § 46 Ordnungswidrigkeitengesetz) und auf Nachfrage zur Sache, gegebenenfalls auch vor Gericht, aussagen muss (§ 161 a Strafprozessordnung in Verbindung mit § 46 Ordnungswidrigkeitengesetz).')").click()

        await asyncio.sleep(5)

        await next_btn()

        await page.locator("button:has(span:text('Absenden'))").click()

        await asyncio.sleep(120)

        await browser.close()
