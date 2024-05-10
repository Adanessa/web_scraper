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

# Find the body element
body_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[4]/div[2]/div/div/div/div[1]/ul")

# Get the text content of the body element
scraped_data = body_element.text

# Split the scraped data into individual system names
system_names = scraped_data.split('\n')

# Remove the "Starfield:" prefix and " System" suffix, and create the desired structure
solar_system = {}
for system_name in system_names:
    system_name = system_name.replace("Starfield:", "").replace(" System", "")
    solar_system[system_name] = {"planets": {}}

# Wrap the solar_system dictionary with another dictionary
solar_system_final = {"solar_system": solar_system}

# Save the structured data into a JSON file
output_file = "structured_data.json"
with open(output_file, "w") as file:
    json.dump(solar_system_final, file, indent=4)

print("Structured data saved to:", output_file)

# Quit the WebDriver
driver.quit()
