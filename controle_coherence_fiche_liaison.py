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


def controle_coherence(fichier_csv, liste_coordonnees_texte) :
    try : 
        cpt = 0
        cpt_liste_coordonnees = 0 
        with open(fichier_csv,'r') as file :
            reader = csv.reader(file, delimiter=',')
            for ligne in reader :
                for element in ligne : 
                    cpt += 1 
                    print("cpt = "+ str(cpt)) 
                    if cpt >= 33 and cpt_liste_coordonnees < len(liste_coordonnees_texte) :
                        num_page, coordonnees, _ = liste_coordonnees_texte[cpt_liste_coordonnees]
                        nouvel_element = (num_page,coordonnees,element)
                        liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
                        cpt_liste_coordonnees += 1
                
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
        
    return liste_coordonnees_texte
        
def choisir_fichier():
    # Ouvrir une boîte de dialogue pour choisir le fichier CSV
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])

    # Si un fichier a été sélectionné, lire son contenu
    if chemin_fichier:
        liste_de_paires = [] 
        liste_de_paires.append((2, (51,63), "numetud"))
        liste_de_paires.append((2, (36,69),"test_Nom"))
        liste_de_paires.append((2, (112,69), "test_Prenom"))
        liste_de_paires.append((2, (43,74), "Francais"))

        print("ready to write on pdf\n")

        write_data_to_pdf('C:\\workspace\\s10\\lms_moodle\\Fiche_de_liaison_Licence_2023-2024.pdf', "output.pdf", chemin_fichier, liste_de_paires)

        print( "traitement terminé")
        
        



         
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


def write_data_to_pdf(input_pdf, output_pdf, chemin_fichier, liste_coordonnees_texte):
    liste_coordonnees_texte = controle_coherence(chemin_fichier, liste_coordonnees_texte)
    try :
        with open(input_pdf, 'rb') as file :

            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                # Rechercher le mot-clé et ajouter les données supplémentaires si trouvé
                for page_numero, coordonnees, texte_a_inserer in liste_coordonnees_texte :
                    x,y = coordonnees
                    if page_numero == page_num :    
                        packet = io.BytesIO()
                        can = canvas.Canvas(packet, pagesize=letter)
                        can.drawString(mm_to_points(x)+10, mm_to_points(297) - mm_to_points(y) - 5, texte_a_inserer)  # Ajouter à une position spécifique
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

