import requests
from bs4 import BeautifulSoup

# Ange URL:en för sidan
url = 'https://inara.cz/starfield/starsystem/9/'

# Definiera en användaragent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# Begär sidans HTML-innehåll med användaragenten
response = requests.get(url, headers=headers)

# Kontrollera om begäran lyckades (HTTP-statuskod 200 betyder att allt är OK)
if response.status_code == 200:
    html_content = response.text

    # Skapa ett BeautifulSoup-objekt för att analysera HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Hitta den div där resurslänkarna finns
    tag_container = soup.find('div', class_='tagcontainer')

    # Om div med klassen "tagcontainer" hittades
    if tag_container:
        # Hitta alla länkar inom div och loopa över dem
        resources = tag_container.find_all('a', class_='tag')
        for resource in resources:
            # Extrahera resursnamnet från länken
            resource_name = resource.text
            print(resource_name)
    else:
        print("Kunde inte hitta resursinformationen på sidan.")
else:
    print("Fel vid hämtning av sidans innehåll. Statuskod:", response.status_code)
