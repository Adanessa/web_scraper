def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

def split_sections(data):
    sections = data.split('\n\n')
    return sections

file_path = 'data.txt'
data = read_data(file_path)
sections = split_sections(data)

print(f"Number of sections: {len(sections)}")
