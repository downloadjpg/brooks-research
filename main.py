import re
import csv
import os
import sys
from PyPDF2 import PdfReader
from tqdm import tqdm

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

# There are 1,365 foals in AwesomeAgain.pdf
input_folder = "input"
output_folder = "output"
pattern = re.compile(r'''
    ((?!=)[^\n\\]{1,23}),       # Foal name
    \ ([^,]+),                  # Foal birthday
    (\ [\w\s\/]+)?              # Foal color (optional)
    \ (colt|gelding|filly)\ --  # Foal sex
    (?:                         # Anything below this can fail and still go through.
    \ ([^\(]+)                  # Dam name TODO: Add 1,23, country code?
    \ \((\d+)\)                 # Dam year
    (?:\ \(SPR=(\d+);           # Dam SPR (optional)
    \ CPI=(\d+\.\d+)\))?        # Dam CPI (optional)
    \s([^\n\\]{1,23})           # Dam sire name
    \ \((\d+)\)                 # Dam sire year
    \s
    # TODO: died capture, 'stands in ___'
    #(?:Died\ in\ [\d+]{4}\s)?
    (?:[^\n()]*)?
    \(SPR=(\d+);                # Foal SPR
    \ CPI=(\d+\.\d+)\)          # Foal CPI
    )?                          
    ''', re.VERBOSE)

# TODO: this somehow fell to 1,293
# Uses a less restrictive part of the regex to count all names.
def count_names(input_path) -> int:
    pattern = re.compile(r'''
    ((?!=)[^\n\\]{1,23}),       # Foal name
    \ ([^,]+),                  # Foal birthday
    (\ [\w\s\/]+)?              # Foal color (optional)
    \ (colt|gelding|filly)      # Sex
    ''', re.VERBOSE)
    text = extract_body_text(input_path)
    foals = []
    matches = re.findall(pattern, text)
    return len(matches)

def convert_file(filename : str) -> None:
    # Get input and output path variables
    input_path = os.path.join(input_folder, filename)
    output_name = filename[:-4] + '.csv' # removes .pdf, adds .csv
    output_name = output_name 
    output_path = os.path.join(output_folder, output_name)

    # Construct reader, open file.
    reader = PdfReader(input_path)
    print("Reading " + filename + "...")

    print("Filtering out headers...")
    text = extract_body_text(input_path)

    # Process data
    print("Extracting foal data...")
    foals = []
    matches = re.findall(pattern, text)
    for match in matches:
        foals.append(Foal(*match))

    # Output
    print("Writing file to \'%s\'" % (output_path))
    # TODO: give information on file diff?
    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    header = [column['title'] for column in columns]
    writer.writerow(header)
    for foal in foals:
        row = row = [getattr(foal, column['key']) for column in columns]
        writer.writerow(row)
    file.close()
    print("Done.")


def extract_body_text(input_path) -> str:
    reader = PdfReader(input_path)
    parts = []
    # This 'visitor function' is passed in to extract_text(), and should take out any headers.
    # https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html
    # TODO: doesn't remove the 'Bay Horse; Mar 29 1994' subtitle
    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720:
            parts.append(text)
    
    for page in reader.pages[1:336]:
        page.extract_text(visitor_text=visitor_body) # we don't actually use this return value?

    text = "".join(parts)
    text = remove_subheader(text)
    return text

def remove_lines_with_string(text, string_to_remove) -> None:
    lines = text.split('\n')
    cleaned_lines = (line for line in lines if line != string_to_remove)
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text

def remove_subheader(text: str) -> str:
    # Find it
    pattern = r"(\w+ Horse; \w+ \d{1,2}, \d{4})"
    match = re.search(pattern, text)
    # Remove it
    if match:
        subheader = match.group(0)
        print("Removing subheader: \'", subheader, "\'")
        text = remove_lines_with_string(text, subheader)
    return text


def main():
    # get list of input pdf's
    input_files = os.listdir(input_folder)
    print("%d files found in \'%s\'" % (len(input_files), input_folder))
    for file in input_files:
        convert_file(file)


if __name__ == '__main__':
    main()