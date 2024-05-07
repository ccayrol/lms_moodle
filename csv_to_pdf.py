import pandas as pd
from PyPDF2 import PdfReader, PdfWriter



def ecriture_csv_to_pdf(fichier_csv, pdf_a_remplir) :
    data = pd.read_csv(fichier_csv)
    with open(pdf_a_remplir, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()
        page = reader.pages[0]  # Supposons qu'il n'y ait qu'une seule page dans le PDF

    for index, row in data.iterrows():
        # Remplir les champs du formulaire en utilisant les données du CSV
        # Par exemple, si les colonnes du CSV correspondent aux champs du formulaire :
        page['champ1'] = row['colonne1']
        page['champ2'] = row['colonne2']
        # Répétez cela pour chaque champ à remplir

        # Ajouter la page remplie au fichier de sortie
        writer.add_page(page)

# Enregistrer le PDF rempli
    with open('formulaire_rempli.pdf', 'wb') as output_file:
        writer.write(output_file)
    
    
    
    
    
