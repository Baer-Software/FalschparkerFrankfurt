from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import os

def fill_form(reporter, vehicle, incident):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        "autofill.profile_enabled": False,
        "profile.default_content_setting_values.autofill": 2,
        "profile.default_content_setting_values.autofill_address": 2,
        "profile.default_content_setting_values.autofill_credit_card": 2
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://portal-civ.ekom21.de/civ.public/start.html?oe=00.00.PA.FFOrdA&mode=cc&cc_key=AnzeigeOwi")
        wait = WebDriverWait(driver, 10)

        def fill_by_label(label, input_value, filter_xpath=None):
            if filter_xpath:
                parent = wait.until(EC.presence_of_element_located((By.XPATH, filter_xpath)))
                label_name = parent.find_element(By.XPATH, ".//label[contains(text(), '" + label + "')]")
            else:
                label_name = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), '" + label + "')]")))
            input_name = driver.find_element(By.ID, label_name.get_attribute("for"))
            input_name.send_keys(input_value)

        def custom_select(option):
            select = wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), '" + option + "')]]")))
            select.find_element(By.XPATH, "following-sibling::span").click()
            li_option = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), '" + option + "')]")))
            li_option.click()

        def next():
            button_weiter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Weiter')]]")))
            button_weiter.click()

        next()
        label_86 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".civ-servicekonto-border-top .civ-servicekonto-radio-label")))
        label_86.click()
        next()

        # Reporter group
        custom_select(reporter['salutation'])
        fill_by_label('Name', reporter['last_name'])
        fill_by_label('Vorname', reporter['first_name'])
        fill_by_label('Postleitzahl', reporter['postal_code'])
        fill_by_label('Ort', reporter['city'])
        fill_by_label('Straße/Postfach', reporter['street'])
        fill_by_label('Nr.', reporter['house_number'])
        fill_by_label('Zusatz', reporter['additional_info'])
        fill_by_label('E-Mail-Adresse', reporter['email'])
        fill_by_label('E-Mail-Adresse bestätigen', reporter['email'])
        fill_by_label('Telefonnummer', reporter['phone_number'])
        next()

        # Vehicle group
        fill_by_label('Fahrzeugmodell', vehicle['model'])
        fill_by_label('Farbe', vehicle['color'])
        label_kz = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Kennzeichen') and not(contains(text(), 'Land'))]")))
        input_kz = driver.find_element(By.ID, label_kz.get_attribute("for"))
        input_kz.send_keys(vehicle['license_plate'])
        custom_select(vehicle['country'])
        custom_select(vehicle['vehicle_type'])
        custom_select(vehicle['manufacturer'])

        report_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{incident['type']}')]/..")))
        report_option.click()
        next()

        # Incident group
        duration_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{incident['duration']}')]")))
        duration_option.click()
        location_type_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{incident['location_type']}')]")))
        location_type_option.click()
        obstructed_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{incident['obstructed']}')]")))
        obstructed_option.click()
        if incident['obstructed'] == 'Ja':
            fill_by_label('Bitte beschreiben Sie die Behinderung.', incident['obstruction_description'])
        next()

        fill_by_label('Tatort - Straße und Hausnummer, eventuell Konkretisierung', incident['location_description'])
        fill_by_label('Tattag (Datum)', incident['date'])
        # Click somewhere else on the page to remove focus from the date field
        # driver.find_element(By.TAG_NAME, "body").click()
        fill_by_label('Tatzeit (Zeitpunkt)', incident['start_time'])
        # driver.find_element(By.TAG_NAME, "body").click()
        # fill_by_label('Ende Tatzeit', incident['end_time'])

        # Witnesses (optional)
        witnesses = incident.get('witnesses', [])
        witness_xpath = "//h2[contains(text(), 'Angaben zu weiteren Zeugen bearbeiten')]/.."
        for witness in witnesses:
            # Click "Eintrag hinzufügen" button
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Eintrag hinzufügen')]]")))
            add_btn.click()
            # Wait for modal
            wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Angaben zu weiteren Zeugen bearbeiten')]")))
            custom_select(witness['salutation'])
            fill_by_label('Name', witness['last_name'], filter_xpath=witness_xpath)
            fill_by_label('Vorname', witness['first_name'], filter_xpath=witness_xpath)
            fill_by_label('PLZ', witness['postal_code'], filter_xpath=witness_xpath)
            fill_by_label('Ort', witness['city'], filter_xpath=witness_xpath)
            fill_by_label('Strasse', witness['street'], filter_xpath=witness_xpath)
            fill_by_label('Hausnummer', witness['house_number'], filter_xpath=witness_xpath)
            fill_by_label('Hausnummerzusatz', witness['additional_info'], filter_xpath=witness_xpath)
            fill_by_label('E-Mail', witness['email'], filter_xpath=witness_xpath)
            fill_by_label('Telefonnummer', witness['phone_number'], filter_xpath=witness_xpath)
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Übernehmen')]]")))
            save_btn.click()

        # Upload images for proof_overview and proof_car
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as overview_file:
            overview_file.write(incident['proof_overview'])
            overview_path = overview_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as car_file:
            car_file.write(incident['proof_car'])
            car_path = car_file.name

        try:
            # Find the hidden file input elements by class and upload the images
            file_inputs = driver.find_elements(By.CSS_SELECTOR, "input.gwt-FileUpload[type='file']")
            file_inputs[0].send_keys(overview_path)
            upload_overview_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Beweis-Übersichtsfoto (erforderlich) Hochladen"]')
            upload_overview_btn.click()

            file_inputs[0].send_keys(car_path)
            upload_car_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Beweis-Fahrzeugfoto (erforderlich) Hochladen"]')
            upload_car_btn.click()
        finally:
            os.remove(overview_path)
            os.remove(car_path)

        next()

        obstructed_option = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Ich versichere die Richtigkeit und Vollständigkeit meiner gemachten Angaben. Mir ist bewusst, dass ich als Zeuge oder Zeugin zur wahrheitsgemäßen Angabe verpflichtet bin (§ 57 Strafprozessordnung in Verbindung mit § 46 Ordnungswidrigkeitengesetz) und auf Nachfrage zur Sache, gegebenenfalls auch vor Gericht, aussagen muss (§ 161 a Strafprozessordnung in Verbindung mit § 46 Ordnungswidrigkeitengesetz).')]")))
        obstructed_option.click()

        time.sleep(30)
    finally:
        driver.quit()
