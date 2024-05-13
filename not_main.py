import json
import re
import time
import pygame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pygame.mixer.init()
pygame.mixer.music.load('epic_hacker_song.mp3')
pygame.mixer.music.play()

chromedriver_path = 'chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

url = 'https://inara.cz/starfield/starsystems/'
driver.get(url)

map_container = driver.find_element(By.CLASS_NAME, 'mapcontainer')

# Find all system links within the map container
system_links = map_container.find_elements(By.CSS_SELECTOR, 'span.mappoint a')

# Extract the system names and URLs from the system links
system_data = [(link.text.strip(), link.get_attribute('href')) for link in system_links]

planet_data = {}

for system_name, system_url in system_data:
    driver.get(system_url)
    
    planet_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]")
    
    # Extract text content of the planet element
    planet_text = planet_element.text
    
    # Remove unwanted characters from the system name
    cleaned_system_name = re.sub(r'^[^\w\s]+', '', system_name)
    
    # Create a dictionary to store planet data for this system
    planet_data[cleaned_system_name] = {}
    
    # Split the planet text into individual lines
    planet_lines = planet_text.split('\n')
    
    # Iterate over each line in the planet text
    for line in planet_lines:
        # Check if the line contains a colon
        if ':' in line:
        # Split each line into planet name and resources
            planet_name, planet_resources = line.split(':')
        
        # Add planet name and resources to the system's planet data dictionary
            planet_data[cleaned_system_name][planet_name.strip()] = planet_resources.strip()


# Close the browser session
driver.quit()

pygame.mixer.music.stop()

# Save the planet data to a JSON file
with open('planet_data.json', 'w') as json_file:
    json.dump(planet_data, json_file, indent=4)

print("Scraped data has been saved to planet_data.json")
