import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to chromedriver executable
chromedriver_path = 'chromedriver.exe'

# Initialize Chrome WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL of the webpage
url = 'https://hardcoregamer.com/db/starfield-all-locations-systems-planets-moons/464902/#all-planets-amp-moons-in-starfield'

# Open the webpage
driver.get(url)

# Wait for a few seconds for the page to load
time.sleep(5)

try:
    # Find all tables on the page
    tables = driver.find_elements(By.TAG_NAME, 'table')
    
    # Print the number of tables found
    print("Number of tables found:", len(tables))

    # Loop through each table and print its text
    for table in tables:
        print(table.text)
    
except Exception as e:
    print("An error occurred:", e)

# Quit the WebDriver
driver.quit()
