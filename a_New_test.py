import time
import random
import pygame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

# List of sound effects
sound_effects = [
    "sound_01.wav",
    "sound_02.wav",
    "sound_03.wav",
    "sound_04.wav",
    "sound_05.wav",
    "sound_06.wav"
]

# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Initialize the Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL to skip (if needed)
skip_this_stupid_url = "https://inara.cz/starfield/starsystem/35/"

# Dictionary to store scraped data
solar_systems = {}

# Loop through star system URLs
for i in range(1, 122):
    url = f"https://inara.cz/starfield/starsystem/{str(i).zfill(2)}/"

    # Skip specific URL if needed
    if url == skip_this_stupid_url:
        print(f"Skipping URL: {url}")
        continue

    # XPath to locate the system name
    xpath_name = "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/h2"

    # XPath to locate planets and moons
    xpath_planets_and_moons = "//ul[@class='treeblock']/li[@class='treeitem']"

    # Navigate to the star system URL
    driver.get(url)

    # Wait for the system name element to load
    wait = WebDriverWait(driver, 10)
    system_name_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_name)))
    system_name = system_name_element.text

    # Extract planet and moon information
    planets_and_moons = [element.text for element in driver.find_elements(By.XPATH, xpath_planets_and_moons)]

    # Store the information in the dictionary
    solar_systems[system_name] = planets_and_moons

    # Print system name and planets/moons
    print(system_name)
    print("Planets and Moons:", planets_and_moons)

    # Play a random sound effect
    pygame.mixer.music.stop()
    random_sound_effect = random.choice(sound_effects)
    pygame.mixer.music.load(random_sound_effect)
    pygame.mixer.music.play()

# Quit the WebDriver
driver.quit()

# Save the scraped data as JSON
with open("masterpiece.json", "w", encoding="utf-8") as file:
    json.dump(solar_systems, file, indent=4)

print("Scraped data have been stored as Masterpiece.json.")

