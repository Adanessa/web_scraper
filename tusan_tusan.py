from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = 'chromedriver.exe'

# Create a new Chrome session
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

url = 'https://inara.cz/starfield/starsystem/25/'
driver.get(url)

# Find the mainblock for Alpha Andraste I
alpha_andraste_mainblock = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]"))
)


# Extract the text content of the mainblock for Alpha Andraste I
alpha_andraste_info = alpha_andraste_mainblock.text

# Close the browser session
driver.quit()

print(alpha_andraste_info)
