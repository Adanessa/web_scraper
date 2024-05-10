import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to wait for the presence of element
def wait_for_element(driver, xpath, timeout=10):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False

# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL of the webpage to scrape
url = "https://game8.co/games/Starfield/archives/421780"

# Navigate to the webpage
driver.get(url)

# Wait for the table element to be present
xpath = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody"
if not wait_for_element(driver, xpath):
    print("Timeout waiting for element")
    driver.quit()
    exit()

# Get the table element
table_element = driver.find_element(By.XPATH, xpath)

# Find all rows in the table
rows = table_element.find_elements(By.TAG_NAME, "tr")

# Extract system names from the first column of the table
system_names = []
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:  # Check if columns exist
        system_name_element = columns[0].find_element(By.TAG_NAME, "a")
        system_name = system_name_element.text.strip()  # Get system name from the first column
        system_names.append(system_name)

# Create the desired structure
solar_system = {}
for system_name in system_names:
    solar_system[system_name] = {"planets": {}}

# Wrap the solar_system dictionary with another dictionary
solar_system_final = {"solar_system": solar_system}

# Save the structured data into a JSON file
output_file = "structured_data.json"
with open(output_file, "w") as file:
    json.dump(solar_system_final, file, indent=4)

print("Structured data saved to:", output_file)

# Quit the WebDriver
driver.quit()
