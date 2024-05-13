import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chromedriver_path = 'chromedriver.exe'

# Initialize Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Define the URL and XPath
url = "https://inara.cz/starfield/starsystem/14/"
xpath = "/html/body/div[3]/div[2]/div[3]"

# Load the page
driver.get(url)

# Find the element using XPath
element = driver.find_element(By.XPATH, xpath)

# Get the text content of the element
specific_content = element.text

# Close the WebDriver
driver.quit()

# Save the data to a JSON file
with open("epic_knowledge.json", "w", encoding="utf-8") as file:
    file.write(specific_content)

print("Data saved to epic_knowledge.json.")
