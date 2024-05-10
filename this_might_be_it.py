import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Function to wait for the presence of element
def wait_for_element(driver, xpath, timeout=10):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False

# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL of the webpage to scrape
url = "https://game8.co/games/Starfield/archives/421780"

# Navigate to the webpage
driver.get(url)

# Wait for the table element to be present
xpath = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody"
if not wait_for_element(driver, xpath):
    print("Timeout waiting for element")
    driver.quit()
    exit()

# Get the table element
table_element = driver.find_element(By.XPATH, xpath)

# Find all rows in the table
rows = table_element.find_elements(By.TAG_NAME, "tr")

# Extract system names and links from the first column of the table
system_links = []
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:  # Check if columns exist
        system_link = columns[0].find_element(By.TAG_NAME, "a")
        system_links.append(system_link)

# Create the desired structure
solar_system = {}
for system_link in system_links:
    system_name = system_link.text.strip()
    solar_system[system_name] = {"planets": {}}

# Wrap the solar_system dictionary with another dictionary
solar_system_final = {"solar_system": solar_system}

# Loop through each system link and handle pop-ups before clicking
for system_link in system_links:
    try:
        # Wait for the system link to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='a-link']")))
        
        # Click on the system link
        system_link.click()
        
        # Wait for the planet table element to be present
        planet_table_xpath = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody"
        if not wait_for_element(driver, planet_table_xpath):
            print("Timeout waiting for planet table element")
            driver.quit()
            exit()
        
        # Find the table containing planet names
        planet_table = driver.find_element(By.XPATH, planet_table_xpath)
        
        # Find all planet names in the table
        planet_links = planet_table.find_elements(By.XPATH, "./tr/td[1]/a")
        
        # Collect planet names
        planet_names = [planet_link.text.strip() for planet_link in planet_links]
        
        # Add planet names to the solar system data
        solar_system_final["solar_system"][system_link.text.strip()]["planets"] = planet_names
        
        # Go back to the previous page to continue with the next system
        driver.back()
    
    except ElementClickInterceptedException:
        print("Element click intercepted, handling pop-up")
        # Add code here to handle the pop-up or overlay

# Save the structured data into a JSON file
output_file = "structured_data.json"
with open(output_file, "w") as file:
    json.dump(solar_system_final, file, indent=4)

print("Structured data saved to:", output_file)

# Quit the WebDriver
driver.quit()
