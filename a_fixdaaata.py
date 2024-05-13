def clean_data(text):
    return text.strip().replace("︎", "").replace("︎", "").replace("︎", "").strip()


def parse_data(filename):
    starsystem_data = {}
    current_system = None
    current_planet = None
    current_moon = None

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = clean_data(line)
            if line.startswith("STAR SYSTEM"):
                parts = line.split(":")
                if len(parts) > 1:
                    current_system = parts[1].strip()
                    starsystem_data[current_system] = {"planets": {}}
            elif line.startswith("PLANETS AND MOONS OF"):
                parts = line.split(":")
                if len(parts) > 1:
                    current_planet = parts[1].strip()
                    current_moon = None
                    starsystem_data[current_system]["planets"][current_planet] = {}
            elif line.startswith("\uFFFD"):
                parts = line.split(":")
                if len(parts) > 1:
                    current_moon = parts[0].strip()
                    starsystem_data[current_system]["planets"][current_planet][current_moon] = {}
            elif line:
                parts = line.split(":", 1)
                if len(parts) > 1:
                    key = clean_data(parts[0])
                    value = clean_data(parts[1])
                    if current_moon:
                        starsystem_data[current_system]["planets"][current_planet][current_moon][key] = value
                    elif current_planet:
                        starsystem_data[current_system]["planets"][current_planet][key] = value
                    elif current_system:
                        starsystem_data[current_system][key] = value

    return starsystem_data



def main():
    filename = "masterpiece.json"
    starsystem_data = parse_data(filename)
    print(starsystem_data)


if __name__ == "__main__":
    main()
