import json

# Load the data from the original JSON file
with open("epic_knowledge.json", "r", encoding="utf-8") as file:
    all_systems_data = json.load(file)

# Create a dictionary to store the parsed data
parsed_data = {}

# Define a function to clean up the data
def clean_data(data):
    # Remove unwanted characters and phrases
    cleaned_data = data.replace("\ue854\ufe0e", "").replace("\ue853\ufe0e", "").replace("\ue852\ufe0e", "").replace("\ue85f\ufe0e", "").replace("\n\n", "\n")
    cleaned_data = cleaned_data.replace("Craters   100%", "").replace("Boiled Seas", "").replace("Frozen Plains", "").replace("Slushy Subsurface Seas", "").replace("Seas", "")
    cleaned_data = cleaned_data.replace("Ocean", "").replace("Sandy", "").replace("Hills", "").replace("Energetic", "").replace("Mountains", "").replace("Turbulent", "").replace("Gravitational", "").replace("Rocky", "")
    cleaned_data = cleaned_data.replace("Anomaly (possible)", "").replace("100%", "")
    cleaned_data = cleaned_data.replace("\u2082", "").replace("\ue856\ufe0e", "").replace("Savanna 10%", "").replace("Frozen 15%", "").replace("Wetlands 5%", "").replace("Gaseous font", "").replace("Emerging tectonics", "").replace("Global glacial recession", "").replace("Solar storm seasons", "").replace("Deciduous forest 5%", "").replace("Ecological consortium", "").replace("Sentient microbial colonies", "").replace("Plateau 50%", "").replace("Sonorous lithosphere", "")
    cleaned_data = cleaned_data.replace("\n\n", "\n").strip()
    return cleaned_data



# Iterate through each item in the original dictionary
for key, value in all_systems_data.items():
    # Extract the system name
    system_name_start_index = value.find("PLANETS AND MOONS OF") + len("PLANETS AND MOONS OF")
    system_name_end_index = value.find("\n", system_name_start_index)
    system_name = value[system_name_start_index:system_name_end_index].strip()

    # Remove unwanted characters and phrases
    cleaned_value = clean_data(value)

    # Split the data into individual planets
    planets = cleaned_value.split("\n\ue853\ufe0e")

    # Create a dictionary to store data for this star system
    star_system_data = {}

    # Iterate through each planet in the system
    for planet_data in planets:
        # Extract planet name
        planet_name_start_index = planet_data.find("\n") + 1
        planet_name_end_index = planet_data.find("\n", planet_name_start_index)
        planet_name = planet_data[planet_name_start_index:planet_name_end_index]

        # Extract planet attributes
        attributes = planet_data[planet_name_end_index:].strip().split("\n")
        planet_attributes = {}
        for attribute in attributes:
            if "RESOURCES" in attribute:
                # Extract resources
                resources = attribute.replace("RESOURCES", "").strip().split()
                planet_attributes["RESOURCES"] = resources
            elif "DOMESTICABLE" in attribute:
                # Extract domesticable creatures
                domesticable = attribute.replace("DOMESTICABLE", "").strip().split("\n")
                planet_attributes["DOMESTICABLE"] = domesticable
            elif " " in attribute:
                # Extract other attributes if there's a space character
                key, value = attribute.split(" ", 1)
                planet_attributes[key.strip()] = [value.strip()]

        # Add planet data to the star system data
        star_system_data[planet_name] = planet_attributes

    # Add star system data to the parsed data
    parsed_data[system_name] = star_system_data

# Save the parsed data to a new JSON file
with open("parsed_data.json", "w", encoding="utf-8") as file:
    json.dump(parsed_data, file, indent=4)

print("Data saved to parsed_data.json.")
