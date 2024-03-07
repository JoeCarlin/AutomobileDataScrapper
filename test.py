import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.autolubespecs.com"

# Use Selenium to open the page
driver = webdriver.Chrome()
driver.get(url)

# Wait for the 'Year' dropdown to be present (maximum wait time of 10 seconds)
try:
    year_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'year'))
    )
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()
    exit()

# Create a CSV file to write the results
with open("car_data.csv", "w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)

    # Write the header row to the CSV file
    csv_writer.writerow(["Year", "Make", "Model", "Engine", "Oil Type", "Oil Capacity"])

    # Iterate through each year
    for year_option in Select(year_dropdown).options[1:]:  # Skip the first element ('Year')
        # Select the current year
        Select(year_dropdown).select_by_visible_text(year_option.text)

        # Wait for the 'Make' dropdown to load
        time.sleep(5.0)

        # Find and write the options for the 'Make' dropdown to the CSV file
        make_dropdown = driver.find_element(By.ID, 'make')
        make_options = [option.text for option in Select(make_dropdown).options]

        # Iterate through each make
        for make_option in make_options[1:]:  # Skip the first element ('Make')
            # Select the current make
            Select(make_dropdown).select_by_visible_text(make_option)

            # Wait for the 'Model' dropdown to load
            time.sleep(2.0)

            # Find and write the options for the 'Model' dropdown to the CSV file
            model_dropdown = driver.find_element(By.ID, 'model')
            model_options = [option.text for option in Select(model_dropdown).options]

            # Iterate through each model
            for model_option in model_options[1:]:  # Skip the first element ('Model')
                # Select the current model
                Select(model_dropdown).select_by_visible_text(model_option)

                # Wait for the 'Engine' dropdown to load
                time.sleep(2.0)

                # Find and write the options for the 'Engine' dropdown to the CSV file
                engine_dropdown = driver.find_element(By.ID, 'engine')
                engine_options = [option.text for option in Select(engine_dropdown).options]

                # Iterate through each engine
                for engine_option in engine_options[1:]:  # Skip the first element ('Engine')
                    # Select the current engine
                    Select(engine_dropdown).select_by_visible_text(engine_option)

                    # Wait for the element containing oil information to be present
                    oil_info_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'matchVehicleOil'))
                    )

                    # Find oil information
                    oil_type = oil_info_element.text if oil_info_element.is_displayed() else ''

                    # Wait for the element containing oil capacity information to be present
                    oil_capacity_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'matchVehicleOilCapacity'))
                    )

                    oil_capacity = oil_capacity_element.text if oil_capacity_element.is_displayed() else ''

                    # Write the data to the CSV file
                    csv_writer.writerow([year_option.text, make_option, model_option, engine_option, oil_type, oil_capacity])

                    # Re-select the first option in the engine dropdown for the next iteration
                    Select(engine_dropdown).select_by_index(0)
                    time.sleep(1.0)

                # Re-select the first option in the model dropdown for the next iteration
                Select(model_dropdown).select_by_index(0)
                time.sleep(1.0)

            # Re-select the first option in the make dropdown for the next iteration
            Select(make_dropdown).select_by_index(0)
            time.sleep(1.0)

        # Re-select the first option in the year dropdown for the next iteration
        Select(year_dropdown).select_by_index(0)
        time.sleep(1.0)

# Close the browser
driver.quit()
