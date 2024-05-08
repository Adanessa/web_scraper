import json
import time
import pygame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize pygame mixer
pygame.mixer.init()

# Load epic hacker song
pygame.mixer.music.load('epic_hacker_song.mp3')

# Play the epic hacker song
pygame.mixer.music.play()

# Path ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
url = 'https://inara.cz/starfield/starsystems/'
driver.get(url)

# Find the map container
map_container = driver.find_element(By.CLASS_NAME, 'mapcontainer')

# Find all system links within the map container
system_links = map_container.find_elements(By.CSS_SELECTOR, 'span.mappoint a')

# Extract the URLs from the system links
system_urls = [link.get_attribute('href') for link in system_links]

# Create dictionary
planet_data = {}

# Iterate over each system URL
for system_url in system_urls:
    # Open the system page
    driver.get(system_url)

    # Wait until all h3 elements with class 'bodyname' are visible
    planet_names = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h3.bodyname'))
    )

    # Extract system name from URL
    system_name = system_url.split('/')[-2]
    
    # Store planet names in the dictionary
    planet_data[system_name] = [planet_name.text for planet_name in planet_names]
    
# Close the browser session
driver.quit()

# Stop the epic hacker song
pygame.mixer.music.stop()

# Save scraped data to a JSON file
with open('planet_data.json', 'w') as json_file:
    json.dump(planet_data, json_file, indent=4)

print("Collected data have bin saved and is ready for use. Behave.")