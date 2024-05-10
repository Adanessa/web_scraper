import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

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

            # Visit the system page
            link.click()

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

# Function to scrape resources for each planet
def scrape_planet_resources(system_planets, base_url):
    # Initialize Chrome driver
    chromedriver_path = 'chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # Dictionary to store planet resources
    planet_resources = {}

    try:
        # Iterate over each system and its planets
        for system, planets in system_planets.items():
            # Dictionary to store resources for each planet
            system_planet_resources = {}

            # Iterate over each planet
            for planet in planets:
                # Construct planet URL
                planet_url = f"{base_url}/{planet}"

                # Visit planet page
                driver.get(planet_url)

                # Wait for resources to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'treeblock')))

                # Find planet resources
                resources = driver.find_elements(By.CSS_SELECTOR, 'li.treeitem')

                # Extract and store planet resources
                system_planet_resources[planet] = [resource.text.strip() for resource in resources]

            # Store system's planet resources in main dictionary
            planet_resources[system] = system_planet_resources

        return planet_resources

    finally:
        # Close the browser
        driver.quit()

# Main function to orchestrate scraping
def main():
    # URL for star systems page
    url = 'https://inara.cz/starfield/starsystems/'

    # Base URL for planet pages
    base_url = 'https://inara.cz/starfield/starsystem/14'

    # Phase 1: Scrape system and planet names
    system_planets = scrape_systems_and_planets(url)

    # Phase 2: Scrape planet resources
    planet_resources = scrape_planet_resources(system_planets, base_url)

    # Print and save the scraped data
    print(json.dumps(planet_resources, indent=4))
    with open('planet_data.json', 'w') as json_file:
        json.dump(planet_resources, json_file, indent=4)

if __name__ == "__main__":
    main()
