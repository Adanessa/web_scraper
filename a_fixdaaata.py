import json
import re

# Path to the file containing the plain text data
file_path = 'masterpiece.json'

# Reading the content of the file
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Extracting the star system name
system_name_match = re.search(r"STAR SYSTEM\n(.*?)\n", text)
if system_name_match:
    system_name = system_name_match.group(1)
else:
    system_name = "Unknown"

# Finding all planets and their resources
planets = []
for planet_info in re.finditer(r"(\uE053︎.*?)RESOURCES\n(.*?)(?=\uE053︎|$)", text, re.DOTALL):
    planet_data = {}
    planet_details = planet_info.group(1).split("\n")
    planet_name_match = re.match(r"^\uE053︎ (.*)", planet_details[0])
    if planet_name_match:
        planet_data['name'] = planet_name_match.group(1)

    resources = planet_info.group(2).strip().split("\n")
    planet_data['resources'] = resources
    planets.append(planet_data)

# Constructing the JSON structure
star_system = {
    'system_name': system_name,
    'planets': planets
}

# Writing to JSON
json_file_path = 'starfield_data.json'
with open(json_file_path, 'w') as file:
    json.dump(star_system, file, indent=4)

# This script reads from a specified file and writes a structured JSON file.