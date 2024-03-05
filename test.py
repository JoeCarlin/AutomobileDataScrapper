import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

url = "https://www.autolubespecs.com"

# Use Selenium to open the page
driver = webdriver.Chrome()  # You may need to download the ChromeDriver executable
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

# Create a DataFrame to store the data
data = []

# Iterate through each year
for year_option in Select(year_dropdown).options[1:]:
    # Select the current year
    Select(year_dropdown).select_by_visible_text(year_option.text)

    # Give some time for the 'Make' dropdown to load
    time.sleep(5.0)

    # Find the 'Make' dropdown and get options
    make_dropdown = driver.find_element(By.ID, 'make')
    make_options = [make_option.text for make_option in Select(make_dropdown).options]

    # Iterate through each make
    for make_option in make_options[1:]:
        # Select the current make
        Select(make_dropdown).select_by_visible_text(make_option)

        # Give some time for the 'Model' dropdown to load
        time.sleep(0)

        # Find the 'Model' dropdown and get options
        model_dropdown = driver.find_element(By.ID, 'model')
        model_options = [model_option.text for model_option in Select(model_dropdown).options]

        # Iterate through each model
        for model_option in model_options[1:]:
            # Select the current model
            Select(model_dropdown).select_by_visible_text(model_option)

            # Give some time for the 'Engine' dropdown to load
            time.sleep(0)

            # Find the 'Engine' dropdown and get options
            engine_dropdown = driver.find_element(By.ID, 'engine')
            engine_options = [engine_option.text for engine_option in Select(engine_dropdown).options]

            # Append data to the list
            data.append([year_option.text, make_option, model_option, ', '.join(engine_options)])

# Create a DataFrame from the list of data
df = pd.DataFrame(data, columns=['Year', 'Make', 'Model', 'Engine'])

# Display the DataFrame (table) with lines separating each column and row
for _, row in df.iterrows():
    print(f"{row['Year']:<10}| {row['Make']:<30}| {row['Model']:<30}| {row['Engine']}")

# Save the DataFrame to a CSV file
df.to_csv('car_data.csv', index=False)

# Close the browser
driver.quit()
