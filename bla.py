import time
import json
import unicodedata
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

chromedriver_path = 'chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)


search_url = "https://inara.cz/starfield/starsystems/?formbrief=1&ps1=bessel&pi10=0&pi1=0&pi2=100&pi9=0&pi12=0&pi11=0"

driver.get(search_url)





element = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[5]/td[5]/div/a[1]/span')
al_text = element.text
print(al_text)
