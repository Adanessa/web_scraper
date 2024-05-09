import json
import re
import time
import pygame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

pygame.mixer.init()
pygame.mixer.music.load('epic_hacker_song.mp3')
pygame.mixer.music.play()

def scroll_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()



# Function to scrape system and planet names
def scrape_systems_and_planets(url):
    # Initialize Chrome driver
    chromedriver_path = 'chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # Dictionary to store system and planet names
    system_planets = {}

    try:
        # Open the URL
        driver.get(url)

        # Find all system links
        system_links = driver.find_elements(By.CSS_SELECTOR, 'span.mappoint a')

        # Iterate over each system link
        for link in system_links:
            # Extract system name from link text
            system_name = None
            attempts = 0
            while attempts < 3:
                try:
                    system_name = link.text.strip()
                    break
                except StaleElementReferenceException:
                    time.sleep(1)
                    attempts += 1

            if system_name is None:
                continue

            scroll_and_click(driver, link)

            # Wait for planet names to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.bodyname')))

            # Find all planet names
            planet_names = driver.find_elements(By.CSS_SELECTOR, 'h3.bodyname')

            # Extract cleaned planet names
            cleaned_planet_names = [re.sub(r'^[^\w\s]+', '', planet_name.text.strip()) for planet_name in planet_names]

            # Store system and planet names in dictionary
            system_planets[system_name] = cleaned_planet_names

            # Go back to the star systems page
            driver.execute_script("window.history.go(-1)")

        return system_planets

    finally:
        # Close the browser
        driver.quit()

# Main function
def main():
    url = 'https://inara.cz/starfield/starsystems/'
    system_planets = scrape_systems_and_planets(url)

    # Close the music
    pygame.mixer.music.stop()

    # Save the system and planet names to a JSON file
    with open('system_planets.json', 'w') as json_file:
        json.dump(system_planets, json_file, indent=4)

    print("Scraped data has been saved to system_planets.json")

if __name__ == "__main__":
    main()
