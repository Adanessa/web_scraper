import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chromedriver_path = 'chromedriver.exe'

# Initialize Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Define the URL and XPath for the table containing all systems
url = "https://inara.cz/starfield/starsystems-list/"
table_xpath = "/html/body/div[3]/div[2]/div/div/table"

# Load the page
driver.get(url)

# Find the table element containing all systems using XPath
table_element = driver.find_element(By.XPATH, table_xpath)

# Find all rows in the table (including the header row)
rows = table_element.find_elements(By.TAG_NAME, "tr")

# Initialize a dictionary to store system details
systems_info = {}

# Iterate through each row of the table
for row in rows:
    # Find all cells in the row
    cells = row.find_elements(By.TAG_NAME, "td")
    
    # Check if the row contains system information
    if cells:
        # Extract information about the system from the cells
        system_name = cells[0].text
        system_info = {
            "Coordinates": cells[1].text,
            "Population": cells[2].text,
            "Allegiance": cells[3].text,
            "Government": cells[4].text,
            "State": cells[5].text,
            "Security": cells[6].text,
            "Economy": cells[7].text
            # Add more fields as needed
        }
        
        # Save the system information to the dictionary
        systems_info[system_name] = system_info
        
        # Now let's get information about planets for each system
        # Define the URL for the system
        system_url = "https://inara.cz/starfield/starsystem/" + system_name.replace(" ", "+") + "/"
        
        # Load the page
        driver.get(system_url)
        
        # Find the element containing planet information
        planet_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]")
        
        # Get the text content of the element
        planet_content = planet_element.text
        
        # Save the planet information to the system's dictionary
        systems_info[system_name]["Planets"] = planet_content
        
# Save the system information to a single JSON file
with open("systems_info.json", "w") as file:
    json.dump(systems_info, file, indent=4)

print("System information saved to systems_info.json.")

# Quit the WebDriver
driver.quit()
