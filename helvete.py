import json

# Load the JSON file
with open('restructured_data.json', 'r') as file:
    data = json.load(file)

# Function to remove backslashes recursively
def remove_backslashes(obj):
    if isinstance(obj, dict):
        return {remove_backslashes(k): remove_backslashes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_backslashes(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace('\\', '')
    else:
        return obj

# Remove backslashes from the JSON data
data_without_backslashes = remove_backslashes(data)

# Write the modified data back to the JSON file
with open('your_file_without_backslashes.json', 'w') as file:
    json.dump(data_without_backslashes, file, indent=4)
