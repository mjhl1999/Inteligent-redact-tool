# Inteligent Redact Tool
 PDF redact tool that find sensitive information using a NER (named entity recognition) model and regex.
 
 ## Step 1: PDF text processing using a NER model in python
 Usign Procesador.ipynb jupyter notebook, user can change a PDF and process it. In the back, there is aux_procesador.py script 
 calling ner-spanish model to recognice and tag entities in PDF text, then it filters the important ones ('PER', 'LOC', 'ORG')
 and using regex identifies: RFC, CURP, PASPORT, OCR, CLABE, email, phone numbers, amounts, etc.; to finally create a pandas 
 df that  stores the entity and where is in the PDF, that is saved in to_redact.csv.
 
 <img
  src="https://github.com/mjhl1999/Inteligent-redact-tool/blob/main/images/procesador.png"
  title="Procesador.ipynb"
  style="display: inline-block; margin: 0 auto; max-width: 300px">
 
 ## Step 2: Review and feed back from user
 User can check to_redact.csv and remove incorrect results, or use 'terminos_exceptuados.xlsx' and 'terminos_relevantes.xlsx' to 
 give feed back about what terms are important to (or not to) redact.
 
 ## Step 3: Visualization and redact in Adobe Acrobat XI Pro
 Once user is satisfied with results, using Adobe Acrobat XI Pro action wizard they can visualize future redacts as red annotations
 in text, and check now in the PDF the redactions to be made, and then apply it.
