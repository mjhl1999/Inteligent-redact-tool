import spacy
import pandas as pd
import pdfplumber
import re

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def check_regex(text):
    #RFC Persona Física
    if re.search(r'^[a-zA-Z]{4}[0-9]{6}[a-zA-Z0-9]{3}$', text):
        return text
    #CURP
    if re.search(r'^[a-zA-Z]{4}[0-9]{6}[a-zA-Z]{1}[a-zA-Z]{2}[a-zA-Z]{3}[a-zA-Z0-9]{2}$', text):
        return text
    #PASAPORTE
    if re.search(r'^(?=.*\d)[A-Z0-9]{9}\.?$', text):
        return text
    #CLAVE DE ELECTOR
    if re.search(r'^[a-zA-Z]{6}[0-9]{6}[0-9]{2}[a-zA-Z]{1}[a-zA-Z0-9]{3}$', text):
        return text
    #OCR INE
    if re.search(r'^[0-9]{13}$', text):
        return text
    if re.search(r'^[0-9]{12}$', text):
        return text
    #CLABE Interbancaria
    if re.search(r'^[0-9]{16}$', text):
        return text
    #Email
    if re.search(r'\S+@\S+', text):
        t = text.split('.')
        t = '. '.join(t)
        t = t.split('@')
        t = '@ '.join(t)
        return t
    #Números de celular
    if re.search(r'(?:0|\+?52)-\+?[\d]{2}-[\d]{4}-[\d]{4}$', text): #Reconoce +52-55-3146-3717 y +52 55 3146 3717 solo funciona con el código internacional de México
        t = text.split('+')
        t = '\+ '.join(t)
        t = t.split('-')
        t = '- '.join(t)
        return t  
    if re.search(r'(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}', text): #Reconoce 5531463717
        t = text.split('(')
        t = '\( '.join(t)
        t = t.split(')')
        t = ') '.join(t)
        t = t.split('-')
        t = '- '.join(t)
        return t
    if re.search(r'\+?[\d]{2}-[\d]{4}-[\d]{4}', text): #Reconoce 55-3146-3717
        t = text.split('-')
        t = '- '.join(t)
        return t
    if re.search(r'\+?[\d]{3}-[\d]{3}-[\d]{4}', text): #Reconoce 669-982-1312
        t = text.split('-')
        t = '- '.join(t)
        return t
    if re.search(r'(\+?[\d]{3})[\d]{3}-[\d]{4}', text): #Reconoce (669)982-1312
        t = text.split('(')
        t = '\( '.join(t)
        t = t.split(')')
        t = ') '.join(t)
        t = t.split('-')
        t = '- '.join(t)
        return t  
    #Oficios
    if re.search(r'([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/(.+)', text): #Reconoce GGD/SKS/2022
        text = text.split('/')
        text = '/ '.join(text)
        return text
    #Cedulas profesionales
    if re.search(r'^(cédula profesional número: )+[\d]', text): #Reconoce cédula profesional número: 2546986
        return text
    if re.search(r'^(cédula profesional número )+[\d]', text): #Reconoce cédula profesional número 2546986
        return text
    if re.search(r'^(cédula profesional )+[\d]', text): #Reconoce cédula profesional 2546986
        return text
    if re.search(r'^(cédula profesional: )+[\d]', text): #Reconoce cédula profesional: 2546986
        return text
    if re.search(r'^(Cédula profesional número: )+[\d]', text): #Reconoce Cédula profesional número: 2546986
        return text
    if re.search(r'^(Cédula profesional número )+[\d]', text): #Reconoce Cédula profesional número 2546986
        return text
    if re.search(r'^(Cédula profesional )+[\d]', text): #Reconoce Cédula profesional 2546986
        return text
    if re.search(r'^(Cédula profesional: )+[\d]', text): #Reconoce Cédula profesional: 2546986
        return text
    if re.search(r'^(CÉDULA PROFESIONAL NÚMERO: )+[\d]', text): #Reconoce CÉDULA PROFESIONAL NÚMERO: 2546986
        return text
    if re.search(r'^(CÉDULA PROFESIONAL NÚMERO )+[\d]', text): #Reconoce CÉDULA PROFESIONAL NÚMERO 2546986
        return text
    if re.search(r'^(CÉDULA PROFESIONAL )+[\d]', text): #Reconoce CÉDULA PROFESIONAL 2546986
        return text
    if re.search(r'^(CÉDULA PROFESIONAL: )+[\d]', text): #Reconoce CÉDULA PROFESIONAL: 2546986
        return text
    return False


def process(path):
    redact = pd.DataFrame(columns=['Término', 'Página'])
    path_to_save = path[:find_nth(path, '\\', 3)]
    try:
        terminos_exceptuados = pd.read_excel(path_to_save + "\\" + "Escritorio" + "\\" + 'terminos_exceptuados.xlsx')
    except:
        terminos_exceptuados = pd.read_excel(path_to_save + "\\" + "Desktop" + "\\" + 'terminos_exceptuados.xlsx')

    try:
        terminos_relevantes = pd.read_excel(path_to_save + "\\" + "Escritorio" + "\\" + 'terminos_relevantes.xlsx')
    except:
        terminos_relevantes = pd.read_excel(path_to_save + "\\" + "Desktop" + "\\" + 'terminos_relevantes.xlsx')


    nlp = spacy.load("es_core_news_lg")

    with pdfplumber.open(path) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            text= nlp(single_page_text)
            page = pdf_page.page_number
            for word in text.ents:
                save = True
                if (word.label_ == 'PER' or word.label_ == 'LOC' or word.label_ == 'ORG'):
                    word = word.text.replace('\n', '')
                    if (len(word) != 1):
                        for j in range(len(terminos_exceptuados)):
                            termino = terminos_exceptuados['Término'][j]
                            if (word.casefold() == termino.casefold()):
                                save = False
                        if (save):
                            if("\\" in word):
                                word = word.split('\\')
                                word = '\\ '.join(word)
                            if("/" in word):
                                word = word.split('/')
                                word = '/ '.join(word)
                            df = pd.DataFrame([[word, page]], columns=['Término', 'Página'])
                            redact = pd.concat([redact, df])
    
            page_words = pdf_page.extract_words()
            
            for w in range(len(page_words)):
                word = page_words[w]
                regexx = check_regex(word['text'])
                if(regexx != False):
                    df = pd.DataFrame([[regexx, page]], columns=['Término', 'Página'])
                    redact = pd.concat([redact, df])
                else:
                    for term in terminos_relevantes['Término']:
                        tem_arr = term.split()
                        if (len(tem_arr) == 1):
                            if (word['text'].casefold() == term.casefold()):
                                df = pd.DataFrame([[word['text'], page]], columns=['Término', 'Página'])
                                redact = pd.concat([redact, df])
                        else:
                            term_i = tem_arr[0]
                            if (word['text'].casefold() == term_i.casefold()):
                                term_f = tem_arr[-1]
                                if (page_words[w + len(tem_arr) -1]['text'].casefold() == term_f.casefold()):
                                    df = pd.DataFrame([[term, page]], columns=['Término', 'Página'])
                                    redact = pd.concat([redact, df])


    redact = redact.reset_index(drop=True)
    redact = redact.drop_duplicates()

    try:
        try:
                redact.to_csv(path_to_save + "\\" + "Escritorio" + "\\" + "to_redact.csv", index = False, encoding = 'utf-8', errors = 'ignore', escapechar='\\')
        except:
                redact.to_csv(path_to_save+ "\\" + "Desktop" + "\\" + "to_redact.csv", index = False, encoding = 'utf-8', errors = 'ignore', escapechar='\\')
    except:
        raise Exception('Por favor cierra Adobe Acrobat para poder continuar.') from None
        
    print('El documento ha sido procesado.')
