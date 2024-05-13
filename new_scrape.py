import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json


# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Initialize the Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Load star system names from JSON file
with open("pro_l33t_hacker.json", "r", encoding="utf-8") as file:
    star_systems_dict = json.load(file)

# URL to the star system search page
search_url = "https://inara.cz/starfield/starsystems/"

# Navigate to the star system search page
driver.get(search_url)

# Loop through each star system and search for it
for star_system in star_systems_dict:
    print(f"Processing star system: {star_system}")
    try:
        # Wait for the search input field to be ready
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div/div/form/div[1]/div/input"))
        )
        
        # Clear the search input field
        search_input.clear()
        
        # Enter the star system name in the search input field
        search_input.send_keys(star_system)
        
        # Submit the search query
        search_input.send_keys(Keys.RETURN)
        
        print("Search query submitted")
        
        # Wait for the search results to load
        time.sleep(5)  # You may adjust the waiting time as needed
        
        print("Searching for table containing planet and resource information")
        
        # Find the table containing planet and resource information
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div/table/tbody"))
        )
        
        print("Table found")
        
        # Extract planet and resource information from each row of the table
        planets = {}
        for row in table.find_elements(By.TAG_NAME, "tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                planet_name = cells[0].text
                resources = cells[-1].text.split("\n")
                planets[planet_name] = resources
        
        # Update the star system dictionary with the planet and resource information
        star_systems_dict[star_system] = planets
        
        print("Planet and resource information collected")
    except Exception as e:
        print(f"Error occurred while processing {star_system}: {e}")
    
    # Navigate back to the star system search page
    driver.get(search_url)

# Quit the WebDriver
driver.quit()

# Save the updated star system dictionary as JSON
with open("pro_l33t_hacker.json", "w", encoding="utf-8") as file:
    json.dump(star_systems_dict, file, indent=4)

print("Planet and resource information have been collected and saved.")
