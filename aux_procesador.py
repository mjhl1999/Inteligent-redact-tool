import spacy
import pandas as pd
import pdfplumber

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def process(path):
    redact = pd.DataFrame(columns=['Término', 'Página'])

    with pdfplumber.open(abs_path) as pdf:
    for pdf_page in pdf.pages:
        single_page_text = pdf_page.extract_text()
        text= nlp(single_page_text)
        page = pdf_page.page_number
        for word in text.ents:
            if (word.label_ == 'PER' or word.label_ == 'LOC' or word.label_ == 'ORG'):
                if (len(word) != 1):
                    word = word.text.replace('\n', '')
                    df = pd.DataFrame([[word, page]], columns=['Término', 'Página'])
                    redact = pd.concat([redact, df])


    path_to_save = path[:find_nth(path, '\\', 3)]

    try:
        redact.to_excel(path_to_save + "\\" + "Escritorio" + "\\" + "to_redact.xlsx", index = False)
    except:
        redact.to_excel(path_to_save+ "\\" + "Desktop" + "\\" + "to_redact.xlsx", index = False)

    print('El documento ha sido procesado.')