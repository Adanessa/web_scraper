import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL of the webpage to scrape
url = "https://starfieldwiki.net/wiki/Category:Starfield-Places-Star_Systems"

# Navigate to the webpage
driver.get(url)

# Find the system links
system_links = driver.find_elements(By.XPATH, "//div[@class='mw-category']/ul/li/a")

# Dictionary to store scraped data
solar_system = {}

# Loop through system links
for link in system_links:
    system_name = link.text.strip()
    system_url = link.get_attribute("href")
    print(f"Scraping system: {system_name}")
    
    # Navigate to the system page
    driver.get(system_url)
    
    # Find and collect information about each planet within the system
    planets_info = driver.find_elements(By.CLASS_NAME, "mw-parser-output")
    print(f"Number of planet sections found: {len(planets_info)}")
    
    # Dictionary to store planet data for the current system
    system_planets = {}
    for planet_info in planets_info:
        planet_name_element = planet_info.find_element(By.TAG_NAME, "h2")
        planet_name = planet_name_element.text.strip()
        print(f"Scraping planet: {planet_name}")
        
        resources = [resource.text.strip() for resource in planet_info.find_elements(By.TAG_NAME, "li")]
        print(f"Resources found for {planet_name}: {resources}")
        
        system_planets[planet_name] = resources
    
    # Store planet data for the current system in the solar_system dictionary
    solar_system[system_name] = {"planets": system_planets}

# Save the scraped data into a JSON file
output_file = "scraped_data.json"
with open(output_file, "w") as file:
    json.dump(solar_system, file, indent=4)

print("Scraped data saved to:", output_file)

# Quit the WebDriver
driver.quit()
