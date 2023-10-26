import re
import csv
from PyPDF2 import PdfReader

class Foal:
    def __init__(self, name, birthday, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year):
        self.name = name
        self.birthday = birthday
        self.sex = sex
        self.dam = dam
        self.dam_year = dam_year
        self.dam_spr = dam_spr
        self.dam_cpi = dam_cpi
        self.dam_sire = dam_sire
        self.dam_sire_year = dam_sire_year
        





def main():
    reader = PdfReader("input/AwesomeAgain.pdf")
    # if you're wondering how i did this, i don't know either. regex is wizard shit.
    #pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+))?'
    # todo: add dam_sire_year to regex, need to figure out the country code + year thing
    pattern = r'((?!=)[^\n\\]{1,23}), ([^,]+),( [\w\s\/]+)? (colt|gelding|filly) -- ([^\(]+) \((\d+)\)(?: \(SPR=(\d+); CPI=(\d+\.\d+)\))?\s([^\n\\]{1,23})'
   
    foals = []
    print("reading pdf...")
    for page in reader.pages[1:336]:
        matches = re.findall(pattern, page.extract_text())

        for match in matches:
            name, birthday, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year = match
            foals.append(Foal(name, birthday, sex, dam, dam_year, dam_spr, dam_cpi, dam_sire, dam_sire_year))

    print("writing file...")
    file = open('output/output.csv', 'w', newline='')
    writer = csv.writer(file)
    for foal in foals:
        row = [foal.name, foal.birthday, foal.sex, foal.dam, foal.dam_year, foal.dam_spr, foal.dam_cpi, foal.dam_sire, foal.dam_sire_year]
        writer.writerow(row)
    file.close()
    print("done!")


if __name__ == '__main__':
    main()