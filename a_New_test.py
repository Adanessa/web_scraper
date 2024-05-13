import time
import random
import pygame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pygame.mixer.init()

sound_effects = [
    "sound_01.wav",
    "sound_02.wav",
    "sound_03.wav",
    "sound_04.wav",
    "sound_05.wav",
    "sound_06.wav"
]

chromedriver_path = 'chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

skip_this_stupid_url = "https://inara.cz/starfield/starsystem/35/"

solar_systems = {}

for i in range(1, 122):
    url = f"https://inara.cz/starfield/starsystem/{str(i).zfill(2)}/"

    if url == skip_this_stupid_url:
        print(f"Skipping stupid URL: {url}")
        continue

    xpath_name = "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/h2"
    xpath_planets_and_moons = "//ul[@class='treeblock']/li[@class='treeitem'] | //ul[@class='treeblock']/ul[@class='treelevel treeitem']"

    driver.get(url)

    wait = WebDriverWait(driver, 10)
    system_name_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_name)))
    system_name = system_name_element.text

    planets_and_moons = []

    # Extract planet and moon information
    elements = driver.find_elements(By.XPATH, xpath_planets_and_moons)
    current_planet = None  # Variable to keep track of the current planet being processed

    for element in elements:
        if element.get_attribute("class") == "treeitem":  # If the element is a planet
            current_planet = {"planet": element.text, "moons": []}  # Initialize current planet
            planets_and_moons.append(current_planet)
        elif element.get_attribute("class") == "treelevel treeitem":  # If the element is a moon
            if current_planet is not None:  # Ensure a planet has been initialized
                current_planet["moons"].append(element.text)

    # Convert planets and moons information to dictionaries with lists
    solar_systems[system_name] = [{"planet": planet["planet"], "moons": [moon for moon in planet["moons"]]} for planet in planets_and_moons]


    print(system_name)
    print("Planets and Moons:", planets_and_moons)

    pygame.mixer.music.stop()
    random_sound_effect = random.choice(sound_effects)
    pygame.mixer.music.load(random_sound_effect)
    pygame.mixer.music.play()
    # time.sleep(1)

driver.quit()

import json

with open("masterpiece.json", "w", encoding="utf-8") as file:
    json.dump(solar_systems, file, indent=4)

print("Scraped data have been stored as Masterpiece.json.")
