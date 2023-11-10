import main

def extract_body_text_height_test(filename="input/AwesomeAgain.pdf"):
    for i in range(100,200,5):
        with open(('output/test%d.txt') % i, 'w') as f:
            f.write(main.extract_body_text(filename, i))

def print_pdf(filename="input/AwesomeAgain.pdf"):
    reader = main.PdfReader(filename)
    text = ''
    for page in reader.pages[1:336]:
        text += ('\n------------\n')


