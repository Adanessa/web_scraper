import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

# Counter to track the number of star systems processed
star_systems_processed = 0

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
        
        print("Searching for table containing planet information")
        
        # Find the table containing planet information
        table_planets = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div/table/tbody"))
        )
        
        print("Table containing planet information found")
        
        # Extract planet names
        planets = {}
        for row in table_planets.find_elements(By.TAG_NAME, "tr"):
            planet_name = row.find_element(By.TAG_NAME, "td").text
            planets[planet_name] = {"resources": []}  # Initialize resources as an empty list
        
        print("Planet names collected")
        
        print("Searching for table containing resource links")
        
        # Find the table containing resource links
        table_links = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[5]/div'))
        )
        
        print("Table containing resource links found")
        
       # Extract resource links
        for idx, row in enumerate(table_links.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div/table/tbody/tr')):
            print(row.text)  # Print the row text for debugging
    
            # Check if the row contains hab level information
            hab_rank_cell = row.find_elements(By.TAG_NAME, 'td')[-1]
            hab_rank_text = hab_rank_cell.text
    
            if hab_rank_text:  # If hab level information exists
                try:
                    resource_link = row.find_element(By.XPATH, './td[5]/div/a').get_attribute('href')
                except NoSuchElementException:
                    resource_link = "N/A"  # Placeholder for missing resource link
            else:  # If hab level information doesn't exist
                resource_link = "N/A"
    
            planet_name = list(planets.keys())[idx]  # Get the planet name corresponding to the current row

    # Add the resource link to the respective planet dictionary
            planets[planet_name]['resources'].append(resource_link)




        print("Resource links collected")

        # Update the star system dictionary with the planet names and resource links
        star_systems_dict[star_system] = planets
        
        print("Planet and resource information collected")
        
        # Increment the counter
        star_systems_processed += 1
        
        # Break the loop if 10 star systems have been processed
        if star_systems_processed >= 10:
            print("Processed 10 star systems, breaking the loop")
            break
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
