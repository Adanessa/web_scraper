import time
import random
import pygame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pygame.mixer.init()

sound_effects = [
    "sound_01.wav",
    "sound_02.wav",
    "sound_03.wav",
    "sound_04.wav",
    "sound_05.wav",
    "sound_06.wav"
]


chromedriver_path = 'chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

skip_this_stupid_url = "https://inara.cz/starfield/starsystem/35/"

data_contents = []


for i in range(1, 122):
    url = f"https://inara.cz/starfield/starsystem/{str(i).zfill(2)}/"
    
    if url == skip_this_stupid_url:
        print(f"Skipping stupid URL: {url}")
        continue
    
    xpath = "/html/body/div[3]/div[2]"
    driver.get(url)
    
    # if "System not found" in driver.page_source:
    #     print(f"System not found for URL: {url}")
    #     continue
    
    wait = WebDriverWait(driver, 10)
    system_info = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    data_content = system_info.text
    
    print(data_content)
    
    data_contents.append(data_content)
    
    pygame.mixer.music.stop()
    random_sound_effect = random.choice(sound_effects)
    pygame.mixer.music.load(random_sound_effect)
    pygame.mixer.music.play()
    #time.sleep(1)
    
driver.quit()

with open("masterpiece.json", "w", encoding="utf-8") as file:
    for data_content in data_contents:
        file.write(data_content + "\n")

    
print("Scraped data have been stored as Masterpiece.json.")