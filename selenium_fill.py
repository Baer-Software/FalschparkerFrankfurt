from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

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

        def fill_by_label(label, input_value):
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
        fill_by_label('Hausnr.', reporter['house_number'])
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

        report_option = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Feuerwehrzufahrt')]/..")))
        report_option.click()
        next()

        # Incident group
        location_option = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Das Fahrzeug parkte vor oder in einer amtlich gekennzeichneten Feuerwehrzufahrt.')]")))
        location_option.click()
        blocked_option = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Nein')]")))
        blocked_option.click()
        next()

        fill_by_label('Tatort - Straße und Hausnummer, eventuell Konkretisierung', incident['location_description'])
        date_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@title='Datumseingabe im Format TT.MM.JJJJ']")))
        date_input.send_keys(incident['date'])
        fill_by_label('Beginn Tatzeit', incident['start_time'])
        fill_by_label('Ende Tatzeit', incident['end_time'])

        # Witnesses (optional)
        witnesses = incident.get('witnesses', [])
        for witness in witnesses:
            # Click "Eintrag hinzufügen" button
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Eintrag hinzufügen')]]")))
            add_btn.click()
            # Wait for modal
            wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Angaben zu weiteren Zeugen bearbeiten')]")))
            # Fill modal fields
            def fill_witness_by_label(label, value):
                label_name = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'modal')]//label[contains(text(), '{label}')]")))
                input_name = driver.find_element(By.ID, label_name.get_attribute("for"))
                input_name.clear()
                input_name.send_keys(value)
            fill_witness_by_label('Anrede', witness['salutation'])
            fill_witness_by_label('Name', witness['last_name'])
            fill_witness_by_label('Vorname', witness['first_name'])
            fill_witness_by_label('PLZ', witness['postal_code'])
            fill_witness_by_label('Ort', witness['city'])
            fill_witness_by_label('Strasse', witness['street'])
            fill_witness_by_label('Hausnummer', witness['house_number'])
            fill_witness_by_label('Hausnummerzusatz', witness['additional_info'])
            fill_witness_by_label('E-Mail', witness['email'])
            fill_witness_by_label('Telefonnummer', witness['phone_number'])
            # Save/close modal (assuming a button with text 'Speichern' or similar)
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Speichern')]]")))
            save_btn.click()
        time.sleep(30)
    finally:
        driver.quit()
