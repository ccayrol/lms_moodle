import csv
import PyPDF2
from PyPDF2.generic import RectangleObject
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTText
from pdfminer.layout import LTTextLine
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx2pdf import convert
import subprocess
import tkinter as tk
from tkinter import filedialog
from decimal import Decimal
import pdfplumber
import os
import re
import io


def controle_coherence(fichier_csv) :
    try : 
        with open(fichier_csv,'r') as file :
            reader = csv.reader(file, delimiter=';')
            for row in reader :
                print(row)
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
        
def choisir_fichier():
    # Ouvrir une boîte de dialogue pour choisir le fichier CSV
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])

    # Si un fichier a été sélectionné, lire son contenu
    if chemin_fichier:
        controle_coherence(chemin_fichier)
        
      
        
    
    
    
# BASE D UTILISATION DE LIBRAIRIE PyPDF2 POUR ECRIRE DU TEXTE A DES COORDONNEES BIEN PRECISES.
# OBJECTIF :
#    - Pour chaque champs à remplir, identifier les coordonnees sur le pdf
#    - Créer une liste qui se compose 
#          . En 1er élément le texte à mettre dans le pdf
#          . En 2eme une paire qui correspond aux coordonnées où il faut inserer le texte

# EXEMPLE : liste_texte_coordonnees : 
# liste_de_paires[] 
# liste_de_paires.append(("test_Prenom", (10, 20)))
# liste_de_paires.append(("test_Nom", (30, 40)))

#Une fois que cette liste est complète, parcourir cette liste en appelant la fonction write_on_existing_pdf
#exemple :
# for texte_a_inserer, coordonnees in liste_de_paires :
#    x, y = coordonnees
#    write_on_existing_pdf(input_pdf, texte_a_inserer, x, y, output_pdf)





#PERMET DE TROUVER LA POSITION DUN MOT DANS PDF --> FONCTIONNE
         
def pixels_to_mm(pixels, dpi=72):
    inches = pixels / dpi
    mm = inches * 25.4  # 1 pouce = 25.4 millimètres
    return mm

def mm_to_points(mm):
    # Conversion de millimètres en points (1 mm = 2.83465 points)
    return mm * 2.83465

def find_keyword_position(pdf_path, keyword):
    positions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            for word in page.extract_words():
                if word['text'] == keyword:
                    positions.append((page_num + 1,float(word['x0']), float(word['top'])))
    return positions

def ecrire_sur_pdf(input_pdf_path, data) :
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, "Hello world")
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PyPDF2.PdfReader(packet)
    # read your existing PDF
    existing_pdf = PyPDF2.PdfReader(open(input_pdf_path, "rb"))
    output = PyPDF2.PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    output_stream = open("destination.pdf", "wb")
    output.write(output_stream)
    subprocess.Popen(['start', '', output], shell=True)

def write_data_to_pdf(input_pdf, output_pdf, keyword, data):
    position_keyword = find_keyword_position(input_pdf ,keyword)
    try :
        with open(input_pdf, 'rb') as file :

            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                # Rechercher le mot-clé et ajouter les données supplémentaires si trouvé
                if keyword in page.extract_text():
                    print(str(keyword) + " trouve à la page "+ str(page_num)) 
                    for page_numero, x, y in position_keyword :
                        if (page_numero-1) == page_num :
                            packet = io.BytesIO()
                            can = canvas.Canvas(packet, pagesize=letter)
                            can.drawString(x+30, mm_to_points(297) - (y+5), data)  # Ajouter à une position spécifique
                            can.save()
                            packet.seek(0)
                            new_pdf = PyPDF2.PdfReader(packet)
                            page.merge_page(new_pdf.pages[0])
                writer.add_page(page)
            # Enregistrement du fichier PDF de sortie
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
                
            subprocess.Popen(['start', '', output_pdf], shell=True)
                    
    except Exception as e:
        print("Une erreur est survenue lors de l'ajout de données au PDF :", e)
        
    

 

        
def create_pdf_final(input_pdf, output_pdf, liste_paire) :
    numero_page_active = 0
    try :
        with open(input_pdf, 'rb') as file :
            reader = PdfReader(file)
            writer = PdfWriter()
            c= None
            
            for balise, texte_a_inserer, numero_de_page in liste_paire:
                position_balise = find_word_position(input_pdf, balise)
                print("position balise x = "+ position_balise[0])
                print("position balise y = "+ position_balise[1])
                position_texte_a_inserer = (position_balise[0]+10, position_balise[1])
                for page_num, page in enumerate(reader.pages):
                    writer.add_page(page)
                    page_text = page.extract_text()
                    print("texte a inserer : "+texte_a_inserer)
                    print("numero page : " + str(page_num))
                    print(page_text)
                    if c is None:
                        c = canvas.Canvas(output_pdf, pagesize=letter)
                        c.setFillColor('black')
                        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
                        c.setFont("Arial", 12)
                    x = position_texte_a_inserer[0]
                    y = position_texte_a_inserer[1]
                    print("x = "+ str(position_texte_a_inserer[0]))
                    print("y = "+ str(position_texte_a_inserer[1]))
                    c.drawString(x, y, texte_a_inserer)
                    if(numero_page_active != page_num) :
                        c.showPage()
                        numero_page_active += 1
                        c.save()
                        subprocess.Popen(['start', '', output_pdf], shell=True)
                        print("Le programme est en pause. Appuyez sur Entrée pour continuer...")
                        input()  # Attend que l'utilisateur appuie sur Entrée
                        print("L'exécution du programme continue...")
                        c = canvas.Canvas(output_pdf, pagesize=letter)
                        c.setFillColor('black')
                        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
                        c.setFont("Arial", 12)
            c.save()
            
            # Écrire le contenu final dans le fichier de sortie
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
                
            subprocess.Popen(['start', '', output_pdf], shell=True)
    
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
                    
        


        

# DEROULER DE TOUT L'ALGORITHME
# VERSION FINALE DOIT SE COMPOSER :
#   - Recupération fichier csv en passant par l'utilisateur
#   - Effectuer controle de coherence sur les donnees
#   - Implementer la liste de texte coordonnees
#   - Boucler dessus pour ajouter chaque élément au bon emplacement




# Recupération fichier csv en passant par l'utilisateur
if __name__ == "__main__":
    # Créer une fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Lire un fichier CSV")

    # Créer un bouton pour choisir le fichier CSV
    bouton_choisir = tk.Button(fenetre, text="Choisir un fichier CSV", command=choisir_fichier)
    bouton_choisir.pack(pady=10)

    # Lancer la boucle principale de l'interface graphique
    fenetre.mainloop()

    
#TODO : Effectuer controle de coherence sur les donnees




# Implementer la liste de texte coordonnees, exemple ici    
liste_de_paires = [] 
liste_de_paires.append(("Prénom","test_Prenom", 2))
liste_de_paires.append(("Nom", "test_Nom", 2))

print("ready to write on pdf\n")


positions_prenom = find_keyword_position('C:\\workspace\\s10\\lms_moodle\\Fiche_de_liaison_Licence_2023-2024.pdf', "Prénom")

print("Positions de 'Prénom':", positions_prenom)



write_data_to_pdf('C:\\workspace\\s10\\lms_moodle\\Fiche_de_liaison_Licence_2023-2024.pdf', "output.pdf", "Prénom", "Jean")

print( "traitement terminé")
