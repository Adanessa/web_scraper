from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage with the interactive map
url = 'https://inara.cz/starfield/starsystems/'
driver.get(url)

# Find the map container
map_container = driver.find_element(By.CLASS_NAME, 'mapcontainer')

# Find all system links within the map container
system_links = map_container.find_elements(By.CSS_SELECTOR, 'span.mappoint a')

# Extract the URLs from the system links
system_urls = [link.get_attribute('href') for link in system_links]

# Iterate over each system URL
for system_url in system_urls:
    # Open the system page
    driver.get(system_url)

    # Wait until all h3 elements with class 'bodyname' are visible
    planet_names = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h3.bodyname'))
    )

    # Print the number of planet names found for this system
    print(f"Number of planet names found for {system_url}: {len(planet_names)}")

    # Iterate over each planet name and print it
    for planet_name in planet_names:
        print("Planet Name:", planet_name.text)

# Close the browser session
driver.quit()
