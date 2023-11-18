import csv
from foal import Foal

# Define the column information
columns = [
    {'title': 'Foal Name', 'key': 'name'},
    {'title': 'Year', 'key': 'birthday'},
    {'title': 'Sex', 'key': 'sex'},
    {'title': 'SPR', 'key': 'spr'},
    {'title': 'CPI', 'key': 'cpi'},
    {'title': 'Dam Name', 'key': 'dam'},
    {'title': 'Dam Year', 'key': 'dam_year'},
    {'title': 'Dam SPR', 'key': 'dam_spr'},
    {'title': 'Dam CPI', 'key': 'dam_cpi'},
    {'title': 'Dam Sire Name', 'key': 'dam_sire'},
    {'title': 'Dam Sire Year', 'key': 'dam_sire_year'},
]

def write_txt(path, text):
    file = open(path, 'w')
    file.write(text)
    file.close

def write_csv(path, foal_data: list[Foal]):
    file = open(path, 'w', newline='')
    writer = csv.writer(file)
    header = [column['title'] for column in columns]
    writer.writerow(header)
    for foal in foal_data:
        row = row = [getattr(foal, column['key']) for column in columns]
        writer.writerow(row)
    file.close()