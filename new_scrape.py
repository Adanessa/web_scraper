import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json

chromedriver_path = 'chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

with open("pro_l33t_hacker.json", "r", encoding="utf-8") as file:
    star_systems_dict = json.load(file)

search_url = "https://inara.cz/starfield/starsystems/"

driver.get(search_url)

star_systems_processed = 0

for star_system in star_systems_dict:
    print(f"Processing star system: {star_system}")
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div/div/form/div[1]/div/input"))
        )
        
        search_input.clear()

        search_input.send_keys(star_system)

        search_input.send_keys(Keys.RETURN)
        
        print("Search query submitted")
        
        time.sleep(5)
        
        print("Searching for table containing planet information")

        table_planets = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div/table/tbody"))
        )
        
        print("Table containing planet information found")
        
        planets = {}
        for row in table_planets.find_elements(By.TAG_NAME, "tr"):
            planet_name = row.find_element(By.TAG_NAME, "td").text
            planets[planet_name] = {"resources": []}  
        
        print("Planet names collected")
        
        print("Searching for table containing resource links")
        
        table_links = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[5]/div'))
        )
        
        print("Table containing resource links found")
        
        for idx, row in enumerate(table_links.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div/table/tbody/tr')):
            print(row.text)
    
            span_tags = row.find_elements(By.TAG_NAME, 'span')
            
            for span_tag in span_tags:
                resource_name = span_tag.text
                if not resource_name.isdigit() and "days" and "hours" not in resource_name:
                    planets[list(planets.keys())[idx]]['resources'].append(resource_name)

        print("Resource names collected")

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
    
    driver.get(search_url)

driver.quit()

with open("pro_l33t_hacker.json", "w", encoding="utf-8") as file:
    json.dump(star_systems_dict, file, indent=4)

print("Planet and resource information have been collected and saved.")