import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chromedriver_path = 'chromedriver.exe'
skip_this_stupid_url = "https://inara.cz/starfield/starsystem/35/"

# Systems where the content is located at "/html/body/div[3]/div[2]/div[4]"
systems_with_div_4 = [1, 2, 3, 4, 5, 8, 9, 10, 18, 20, 26, 27, 29, 31, 34, 37, 39, 45, 48, 52, 57, 59, 63, 70, 71, 80, 81, 91, 93, 94, 95, 107, 114, 121]

# Initialize Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Dictionary to store data for all systems
all_systems_data = {}

# Loop through all the systems
for i in range(1, 122):
    url = f"https://inara.cz/starfield/starsystem/{str(i).zfill(2)}/"

    # Skip specific URLs if needed
    if url == skip_this_stupid_url:
        print(f"Skipping stupid URL: {url}")
        continue

    # Determine the XPath based on the system
    if i in systems_with_div_4:
        xpath = "/html/body/div[3]/div[2]/div[4]"
    else:
        xpath = "/html/body/div[3]/div[2]/div[3]"

    # Load the page
    driver.get(url)

    # Find the element using the XPath
    try:
        element = driver.find_element(By.XPATH, xpath)
        specific_content = element.text
        
        # Add the fetched content to the dictionary
        all_systems_data[i] = specific_content
    except:
        print(f"No content found for system {i}. Skipping...")
        continue

# Close the WebDriver after looping through all systems
driver.quit()

# Save the data to a JSON file
with open("epic_knowledge.json", "w", encoding="utf-8") as file:
    json.dump(all_systems_data, file, indent=4)

print("Data saved to epic_knowledge.json.")
