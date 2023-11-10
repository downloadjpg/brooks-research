import re
import csv
import os
import sys
from PyPDF2 import PdfReader

from foal import Foal

input_folder = "input"
output_folder = "output"
pattern = re.compile(r'''
    ((?!=)[^\n\\]{1,23}),       # Foal name
    \ ([^,]+),                  # Foal birthday
    (\ [\w\s\/]+)?              # Foal color (optional)
    \ (colt|gelding|filly)\ --  # Foal sex
    \ ([^\(]+)                  # Dam name TODO: Add 1,23, country code?
    \ \((\d+)\)                 # Dam year
    (?:\ \(SPR=(\d+);           # Dam SPR (optional)
    \ CPI=(\d+\.\d+)\))?        # Dam CPI (optional)
    \s([^\n\\]{1,23})           # Dam sire name
    \((\d+)\)                   # Dam sire year
    ''', re.VERBOSE)

# TODO: this somehow fell to 1,293
# TODO: also the verbose pattern still doesn't work

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

    text_body = "".join(parts)
    return text_body


def remove_lines_with_text(text, text_to_remove):
    # TODO: optimize?
    lines = text.split('\n')
    cleaned_lines = (line for line in lines if line != text_to_remove)
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text


def convert_file(filename : str) -> None:
    input_path = os.path.join(input_folder, filename)
    output_name = filename[:-4] + '.csv' # removes .pdf, adds .csv
    output_name = output_name 
    output_path = os.path.join(output_folder, output_name)

    reader = PdfReader(input_path)

    print("Reading " + filename + "...")
    text = extract_body_text(input_path)
    print("Extracting data...")
    text = remove_lines_with_text(text, "Bay Horse; Mar 29, 1994")
    foals = []
    matches = re.findall(pattern, text)

    for match in matches:
        name, birthday, color, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year = match
        foals.append(Foal(
            name,
            birthday,
            sex,
            dam,
            dam_year,
            dam_spr,
            dam_cpi,
            dam_sire,
            dam_sire_year))

    print("Writing file to \'%s\'" % (output_path))
    # TODO: give information on file diff?
    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    header = ['Name', 'Year', 'Sex', 'Dam Name', 'Dam Year', 'Dam SPR', 'Dam CPI', 'Dam Sire Name', 'Dam Sire Year']
    writer.writerow(header)
    for foal in foals:
        row = [foal.name, foal.birthday, foal.sex, foal.dam, foal.dam_year, foal.dam_spr, foal.dam_cpi, foal.dam_sire, foal.dam_sire_year]
        writer.writerow(row)
    file.close()
    print("Done.")





def main():
    # get list of input pdf's
    input_files = os.listdir(input_folder)
    print("%d files found in \'%s\'" % (len(input_files), input_folder))
    for file in input_files:
        convert_file(file)


if __name__ == '__main__':
    main()