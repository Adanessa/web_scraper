import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def parse_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data
    
def structure_data(data):
    structured_data = {}
    
    for table_name, table_content in data.items():
        # Split table content into lines
        lines = table_content.split('\n')
        # Iterate over each line to extract information
        for i in range(0, len(lines), 4):
            planet_name = lines[i]
            level = lines[i + 1]
            planet_type = lines[i + 2]
            system = lines[i + 3]
            if system not in structured_data:
                structured_data[system] = []
            structured_data[system].append({
                "name": planet_name,
                "level": level,
                "type": planet_type
            })
    return structured_data

def get_system_links(driver):
    # Locate the table containing system information
    system_table = driver.find_element(By.XPATH, '//*[@id="article-body"]/div[1]/div[5]/table')
    # Find all links to system pages within the table
    system_links = system_table.find_elements(By.TAG_NAME, 'a')
    # Extract the href attribute from each link
    system_links_href = [link.get_attribute('href') for link in system_links]
    return system_links_href

def get_resource_info(driver):
    try:
        # Locate the resource information on the system page
        resource_info = driver.find_element(By.CLASS_NAME, 'entry-content').text
        return resource_info
    except NoSuchElementException:
        return None

chromedriver_path = 'chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

url = 'https://hardcoregamer.com/db/starfield-all-locations-systems-planets-moons/464902/#all-planets-amp-moons-in-starfield'
driver.get(url)

time.sleep(5)

try:
    # Get system links
    system_links = get_system_links(driver)
    
    # Initialize dictionary to store data
    data = {}

    # Visit each system page to gather resource information
    for system_link in system_links:
        driver.get(system_link)
        time.sleep(3)  # Add a delay to allow the page to load
        
        # Get the resource information for the current system
        resource_info = get_resource_info(driver)
        
        if resource_info is not None:
            # Add the resource information to the data dictionary
            data[system_link] = resource_info
        else:
            print(f"No resource information found for system: {system_link}")
    
    # Save the data to a JSON file
    with open('system_resource_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("System resource data saved to system_resource_data.json successfully!")
    
except Exception as e:
    print("An error occurred:", e)

# Quit the WebDriver
driver.quit()
