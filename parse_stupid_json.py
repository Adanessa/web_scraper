import json
import urllib.request

# Read JSON data from the URL
url = "https://pastebin.com/raw/Zm1nWEfX"
response = urllib.request.urlopen(url)
data = response.read().decode("utf-8")

# Remove backslashes from the JSON data string
data = data.replace("\\", "")

# Parse JSON data into a Python dictionary
original_data = json.loads(data)

# Dictionary to store the restructured data
restructured_data = {}

# Iterate through the original data
for key, value in original_data.items():
    # Split the key into system, planet, and type
    system, body, body_type = key.split(".")
    
    # Create system if it doesn't exist
    if system not in restructured_data:
        restructured_data[system] = {"planets": {}}
    
    # Create planets/moons dictionary if it doesn't exist
    if "planets" not in restructured_data[system]:
        restructured_data[system]["planets"] = {}
    
    # Construct resource string with square brackets
    resources_str = "[" + ", ".join([f'"{resource}"' for resource in value]) + "]"
    
    # Add the formatted list of resources to the restructured data
    restructured_data[system]["planets"][body] = resources_str

# Write the restructured data into a new JSON file named "restructured_data.json"
with open("restructured_data.json", "w") as json_file:
    json.dump(restructured_data, json_file, indent=4)

print("Restructured data has been successfully written to restructured_data.json")
