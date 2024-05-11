import json
import re

def parse_system_data(system_data):
    parsed_data = {}
    for planet_name, planet_info in system_data.items():
        # Extract planet properties
        planet_type = re.search(r'PLANET TYPE (.+?)\n', planet_info).group(1)
        gravity = re.search(r'GRAVITY (.+?)\n', planet_info).group(1)
        temperature = re.search(r'TEMPERATURE (.+?)\n', planet_info).group(1)
        atmosphere = re.search(r'ATMOSPHERE (.+?)\n', planet_info).group(1)
        magnetosphere = re.search(r'MAGNETOSPHERE (.+?)\n', planet_info).group(1)
        water = re.search(r'WATER (.+?)\n', planet_info).group(1)
        day_length = re.search(r'DAY LENGTH (.+?)\n', planet_info).group(1)
        planetary_habitation = re.search(r'PLANETARY HABITATION (.+?)\n', planet_info).group(1)
        
        # Extract resources if available
        resources_match = re.findall(r'RESOURCES\n(.+)', planet_info, re.DOTALL)
        resources = []
        if resources_match:
            resources = resources_match[0].strip().split('\n')
            # Remove unwanted characters from resources
            resources = [resource.replace('\ue85f\ufe0e', '') for resource in resources]
        
        # Store planet properties in dictionary
        parsed_data[planet_name] = {
            'planet_type': planet_type,
            'gravity': gravity,
            'temperature': temperature,
            'atmosphere': atmosphere,
            'magnetosphere': magnetosphere,
            'water': water,
            'day_length': day_length,
            'planetary_habitation': planetary_habitation,
            'resources': resources
        }
    return parsed_data

# Read data from JSON file
with open('planet_data.json', 'r') as json_file:
    planet_data = json.load(json_file)

# Create a new dictionary to store parsed data for each system
parsed_system_data = {}

# Iterate over each system
for system_name in planet_data:
    # Access planet data for the current system
    system_planet_data = planet_data[system_name]
    
    # Parse the system data
    parsed_data = parse_system_data(system_planet_data)
    
    # Store the parsed data for the current system
    parsed_system_data[system_name] = parsed_data

# Save the parsed data to a new JSON file
with open('parsed_planet_data.json', 'w') as json_file:
    json.dump(parsed_system_data, json_file, indent=4)

print("Parsed data has been saved to parsed_planet_data.json")
