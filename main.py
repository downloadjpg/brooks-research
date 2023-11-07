import re
import csv
import os
import sys
from PyPDF2 import PdfReader

from foal import Foal

input_folder = "input"
output_folder = "output"
 # if you're wondering how i did this, i don't know either. regex is wizard shit.
#pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+))?
pattern = re.compile(r'''
    (                # Group 1: Name
    (?!=)            # Ensure there's no newline or backslash before this part
    [\w\s^\n\\]      # Match up to 23 characters that are word characters, whitespace, and 
    {1,23}           #      not newline or backslash 
    ),\              # Match a comma and a space

    (                # Group 2: DOB (2000/03/11)
    [^,]+            # Match one or more characters that are not a comma
    ),\              # Match a comma and a space

    (                # Group 3: Color * (b, w, brown? idk it's not used)
    [\w\s\/]         # Match word characters, whitespace, and slashes
    \ )?              # This part is optional.

    (                # Group 4: Gender (colt, gelding, or filly)
    colt|gelding|filly
    )                

    \ --\            # Match two hyphens and surrounding spaces
                    
    (                # Group 5: Dam Name 
    [^\(]+
    )                # Wedged between '---' and the '()' from year or SPR (ERROR CAUSED BY COUNTRY CODES)

    \(               # Match an open parenthesis
    (\d+)            # Group 6: Dam Year
    \)               # Match a closing parenthesis

    (?:              # Start a non-capturing group
    \s               # Match a space
    (                # Group 7: Dam SPR (optional)
    [^\n\\]{1,23}    # Match up to 23 characters that are not newline or backslash
    )
    )?               # This part is optional
    \s               # Newline character
    ''', re.VERBOSE)
pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+)\))?\s([^\n\\]{1,23})'


def extract_body_text(input_path : str, y_margin) -> str:
    reader = PdfReader(input_path)
    parts = []

    # This 'visitor function' is passed in to extract_text(), and should take out any headers.
    # https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html
    # TODO: doesn't remove the 'Bay Horse; Mar 29 1994' subtitle
    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > y_margin and y < 720: ## so many magic numbers, changed from 50-55 to remove 'Bay Horse' Subheader
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
    output_path = os.path.join(output_folder, filename)

    reader = PdfReader(input_path)

    foals = []
    print("Reading " + filename)
    for page in reader.pages[1:336]:
        matches = re.findall(pattern, page.extract_text())

        for match in matches:
            name, birthday, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year = match
            foals.append(Foal(name, birthday, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year))

    print("Writing file to \'%s\'" % (output_path))
    file = open('output/output.csv', 'w', newline='')
    writer = csv.writer(file)
    for foal in foals:
        row = [foal.name, foal.birthday, foal.sex, foal.dam, foal.dam_year, foal.dam_spr, foal.dam_cpi, foal.dam_sire, foal.dam_sire_year]
        writer.writerow(row)
    file.close()
    print("Written!")





def main():
    # get list of input pdf's
    input_files = os.listdir(input_folder)
    print("%d files found in \'%s\'" % (len(input_files), input_folder))
    for file in input_files:
        convert_file(file)


if __name__ == '__main__':
    main()