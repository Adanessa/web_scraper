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

# URL of the main webpage to scrape
main_url = "https://game8.co/games/Starfield/archives/421780"

# Navigate to the main webpage
driver.get(main_url)

# Wait for the table element containing system names and links to be present
system_table_xpath = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody"
if not wait_for_element(driver, system_table_xpath):
    print("Timeout waiting for system table element")
    driver.quit()
    exit()

# Get the system table element
system_table = driver.find_element(By.XPATH, system_table_xpath)

# Find all rows in the system table
system_rows = system_table.find_elements(By.TAG_NAME, "tr")

# Extract system names and links from the first column of the system table
systems = {}
for row in system_rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:  # Check if columns exist
        system_name = columns[0].text.strip()
        system_link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        systems[system_name] = system_link

# Create the desired structure to store scraped data
structured_data = {}

# Iterate through each system and collect planet information
for system_name, system_link in systems.items():
    # Visit the system page
    driver.get(system_link)
    
    # Wait for the planet table element to be present
    planet_table_xpath = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody"
    if not wait_for_element(driver, planet_table_xpath):
        print("Timeout waiting for planet table element")
        continue  # Skip to the next system if planet table not found
    
    # Get the planet table element
    planet_table = driver.find_element(By.XPATH, planet_table_xpath)
    
    # Find all planet rows in the planet table
    planet_rows = planet_table.find_elements(By.TAG_NAME, "tr")
    
    # Extract planet names and links from the first column of the planet table
    planets = {}
    for planet_row in planet_rows:
        columns = planet_row.find_elements(By.TAG_NAME, "td")
        if columns:  # Check if columns exist
            planet_name = columns[0].text.strip()
            planet_link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")
            planets[planet_name] = planet_link
    
    # Add planet information to the structured data
    structured_data[system_name] = {"planets": planets}

# Save the structured data into a JSON file
output_file = "structured_data.json"
with open(output_file, "w") as file:
    json.dump(structured_data, file, indent=4)

print("Structured data saved to:", output_file)

# Quit the WebDriver
driver.quit()

