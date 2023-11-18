import re
from scripts.foal import Foal

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

# Uses a less restrictive part of the regex to count all names.
def count_names(text) -> int:
    
    pattern = re.compile(r'''
    ((?!=)[^\n\\]{1,23}),       # Foal name
    \ ([^,]+),                  # Foal birthday
    (\ [\w\s\/]+)?              # Foal color (optional)
    \ (colt|gelding|filly)      # Sex
    ''', re.VERBOSE)

    foals = []
    matches = re.findall(pattern, text)
    return len(matches)

# this takes the pruned text and extracts foal information
def extract_foal_data(text: str) -> list[Foal]:
    foals = []
    matches = re.findall(pattern, text)
    for match in matches:
        foals.append(Foal(*match))
    return foals