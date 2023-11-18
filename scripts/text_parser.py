import re
from pypdf import PdfReader

from foal import Foal
import main

def extract_body_text(input_path, pbar) -> str:

    reader = PdfReader(input_path)
    parts = []
    # This 'visitor function' is passed in to extract_text(), and should take out any headers.
    # https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html

    # TODO: This is slow!!!!!! Is it looping through every character???
    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720:
            parts.append(text)
    
    pbar_increment_value = 1.0/len(reader.pages)
    for page in reader.pages: # TODO: first page errors?
        pbar.increment(pbar_increment_value)
        page.extract_text(visitor_text=visitor_body) # we don't actually use this return value?

    text = "".join(parts)
    text = remove_subheader(text)
    return text

def remove_lines_with_string(text, string_to_remove) -> None:
    lines = text.split('\n')
    cleaned_lines = (line for line in lines if line != string_to_remove)
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text

def remove_subheader(text: str) -> None:
    # Find it
    pattern = r"(\w+ Horse; \w+ \d{1,2}, \d{4})"
    match = re.search(pattern, text)
    # Remove it
    if match:
        subheader = match.group(0)
        main.log("Removing subheader: \'{subheader}\'")
        text = remove_lines_with_string(text, subheader)
    return text

