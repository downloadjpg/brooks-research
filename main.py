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
    pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+)\))?\s([^\n\\]{1,23})'
   
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