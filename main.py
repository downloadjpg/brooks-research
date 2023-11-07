import re
import csv
import os
from PyPDF2 import PdfReader

from foal import Foal

input_folder = "input"
output_folder = "output"


        

def convert_file(filename : str) -> None:
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    reader = PdfReader("input/AwesomeAgain.pdf")
    # if you're wondering how i did this, i don't know either. regex is wizard shit.
    #pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+))?'
    
    

# todo: add dam_sire_year to regex, need to figure out the country code + year thing
# create full list of potential names and patterns and such
pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+)\))?\s([^\n\\]{1,23})'
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
    ''', re.VERBOSE)

# Test the pattern
text = "Example input here"
match = pattern.match(text)
if match:
    print("Valid match")
else:
    print("No match")

   
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