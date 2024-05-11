import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

url = 'https://inara.cz/starfield/starsystems/'
driver.get(url)

map_container = driver.find_element(By.CLASS_NAME, 'mapcontainer')

# Find all system links within the map container
system_links = map_container.find_elements(By.CSS_SELECTOR, 'span.mappoint a')

# Extract the system names and URLs from the system links
system_data = [(link.text.strip(), link.get_attribute('href')) for link in system_links]

# Create an empty dictionary to store planet data
planet_data = {}

# Iterate over each system
for system_name, system_url in system_data:
    driver.get(system_url)
    
    # Wait until all planet names are visible
    planet_names = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h3.bodyname'))
    )
    
    # Extract cleaned planet names
    cleaned_planet_names = [re.sub(r'^[^\w\s]+', '', planet_name.text.strip()) for planet_name in planet_names]
    
    # Remove unwanted characters from the system name
    cleaned_system_name = re.sub(r'^[^\w\s]+', '', system_name)
    
    # Create a dictionary to store planet resources for this system
    system_planet_resources = {}
    
    # Find all mainblocks
    mainblocks = driver.find_elements(By.CLASS_NAME, 'mainblock')
    
    # Iterate over each planet name and corresponding mainblock, skipping the first planet
    for i in range(1, len(cleaned_planet_names)):  # Start from index 1 to skip the first planet
        planet_name = cleaned_planet_names[i]
        mainblock = mainblocks[i]
        # Extract the text content of the mainblock
        mainblock_text = mainblock.text
        
        # Store the entire mainblock text for the planet
        system_planet_resources[planet_name] = mainblock_text

    # Store the planet resources for this system in the main planet data dictionary
    planet_data[cleaned_system_name] = system_planet_resources

# Close the browser session
driver.quit()

# Save the planet data to a JSON file
with open('planet_data.json', 'w') as json_file:
    json.dump(planet_data, json_file, indent=4)

print("Scraped data has been saved to planet_data.json")
