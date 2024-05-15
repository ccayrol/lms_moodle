import csv
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import subprocess
import tkinter as tk
from tkinter import filedialog
import io
import os



def simplification_fichier_csv(fichier_csv) : 
    return

def controle_coherence(fichier_csv, liste_coordonnees_texte) :
    try : 
        cpt = 0
        cpt_liste_coordonnees = 0 
        with open(fichier_csv,'r') as file :
            reader = csv.reader(file, delimiter=',')
            for ligne in reader :
                for element in ligne : 
                    cpt += 1 
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
        repertoire_fichier = os.path.dirname(chemin_fichier)
        print("repertoire fichier = "+repertoire_fichier)
        output_fichier = repertoire_fichier +"\\output.pdf"
        liste_de_paires = [] 
        
        ########## PAGE 1 #######################################################
        
        liste_de_paires.append((2, (51,63), "numetud"))             #1
        liste_de_paires.append((2, (36,69),"test_Nom"))             #2
        liste_de_paires.append((2, (112,69), "test_Prenom"))        #3
        liste_de_paires.append((2, (43,74), "Francais"))            #4
        liste_de_paires.append((2, (54,84),""))     # ETAPE D ETUDE   5 
        liste_de_paires.append((2, (68,89),""))     # VOTRE UF 6
        liste_de_paires.append((2, (72,100),""))    # ADRESSE PERMARNENTE ETUDIANT 7
        liste_de_paires.append((2, (45,105),""))    # CODE POSTAL 8
        liste_de_paires.append((2, (42,110),""))    # COMMUNE 9
        liste_de_paires.append((2, (36,115),""))    # PAYS 10
        liste_de_paires.append((2, (42,121),""))    # TELEPHONE 11
        liste_de_paires.append((2, (54,126),""))    # TELEPHONE PORTABLE 12
        liste_de_paires.append((2, (72,131),""))    # COURRIEL ETUDIANT 13
        liste_de_paires.append((2, (54,136),""))    # COURRIEL PERSONNEL 14
        liste_de_paires.append((2, (57,165),""))    # DATE FIN DE VALIDITE 15
        liste_de_paires.append((2, (60,170),""))    # COMPAGNIE ASSURANCE 16
        liste_de_paires.append((2, (28,201),""))    # CAISSE PRIMIRE ASSURANCE MALADIE 17
        liste_de_paires.append((2, (27,221),""))    # RAPPORT AVEC OFFRE DE STAGE DIFFUSE PAR UNIVERSITE = OUI 18
        liste_de_paires.append((2, (42,221),""))    # RAPPORT AVEC OFFRE DE STAGE DIFFUSE PAR UNIVERSITE = NON 19
        
        
        ############ PAGE 2 ################################################################################
        
        ############# ETABLISSEMENT ACCUEIL ##############################################
        liste_de_paires.append((3, (73, 48),""))    # SIREN 20
        liste_de_paires.append((3, (82, 53),""))    # RAISON SOCIALE ENTREPRISE 21
        liste_de_paires.append((3, (68, 58),""))    # CODE APE 22
        liste_de_paires.append((3, (103, 58),""))   # EFFECTIF 23
        liste_de_paires.append((3, (63, 63),""))    # ACTIVITE DE L ETABLISSEMENT 24
        liste_de_paires.append((3, (81, 68),""))    # TYPE D ETABLISSEMENT 25
        liste_de_paires.append((3, (77, 72),""))    # ADRESSE ETABLISSEMENT 26
        liste_de_paires.append((3, (47, 77),""))    # CODE POSTAL 27
        liste_de_paires.append((3, (95, 77),""))    # COMMUNE 28
        liste_de_paires.append((3, (38, 82),""))    # PAYS 29 
        liste_de_paires.append((3, (73, 87),""))    # NUMERO TEL ETABLISSEMENT 30
        liste_de_paires.append((3, (71, 92),""))    # SERVICE ET LIEUX PRECIS STAGE 31
        
        
        ############## TUTEUR DE STAGE DANS ORGANISME ACCUEIL ###########################3
        
        liste_de_paires.append((3, (27, 107),""))    # CASE "MONSIEUR" 32
        liste_de_paires.append((3, (38.3, 107),""))    # CASE "MADAME" 33
        liste_de_paires.append((3, (71, 107),""))    # NOM PRENOM 34
        liste_de_paires.append((3, (51, 113),""))    # TELEPHONE 35
        liste_de_paires.append((3, (90, 113),""))    # MEL 36
        liste_de_paires.append((3, (44, 120),""))    # FONCTION 37
    
        ############# CONTENU DU STAGE ###################################################
        
        liste_de_paires.append((3, (47.5, 135),""))    # STAGE OBLIGATOIRE 38
        liste_de_paires.append((3, (72.5, 135),""))    # STAGE OPTIONNEL 39
        liste_de_paires.append((3, (96.5, 135),""))    # STAGE EN FRANCE 40
        liste_de_paires.append((3, (120.8, 135),""))    # STAGE A L ETRANGER 41
        
        liste_de_paires.append((3, (61, 141),""))    # CODE UE 42
        liste_de_paires.append((3, (125, 141),""))    # NOMBRE ECTS 43
        liste_de_paires.append((3, (58, 148),""))    # THEMATIQUE DU STAGE 44
        # SI THEMATIQUE TROP LONG CHANGER DE LIGNE ET PASSER A (30,152)
        liste_de_paires.append((3, (113, 154.5),""))    # SUJET DE STAGE  45
        # SI SUJET TROP LONG CHANGER DE LIGNE ET PASSER A (30,159)
        liste_de_paires.append((3, (133, 160.5),""))    # FONCTION ET TACHES CONFIEES AU STAGIAIRE 46
        # SI TROP LONG PASSER A (30,165), PUIS (30,168)
        liste_de_paires.append((3, (103, 170),""))  # COMETENCES A ACQUERIR PENDANT STAGE 47
        # SI TROP LONG, (30,174) PUIS (30, 178)
        
        
        
        ############ DATE HORAIRES DEROULEMENT DU STAGE ###################################
        
        liste_de_paires.append((3, (53, 190.5),""))    # DEBUT DE STAGE 48
        liste_de_paires.append((3, (50, 194),""))    # FIN DU STAGE 49
        liste_de_paires.append((3, (67.3, 197.5),""))    # INTERUPTION EN COURS DU STAGE OUI 50
        liste_de_paires.append((3, (74.7, 197.5),""))    # INTERUPTION EN COURS DU STAGE NON 51
        liste_de_paires.append((3, (77, 201),""))    # DATE DEBUT INTERRUPTION 52
        liste_de_paires.append((3, (74, 204),""))    # DATE FIN INTERRUPTION 53
        liste_de_paires.append((3, (112, 211),""))    # DUREE EFFECTIF DU STAGES EN HEURES 54
        liste_de_paires.append((3, (85.5, 224),""))    # NOMBRE DE JOUR DE TRAVAIL HEBDO 55
        liste_de_paires.append((3, (50.5, 228.1),""))    # TEMPS DE TRAVAIL = TEMPS PLEINS 56
        liste_de_paires.append((3, (69.3, 228.1),""))    # TEMPS DE TRAVAIL = TEMPS PARTIEL 57
        liste_de_paires.append((3, (73, 234),""))    # NOMBRE D HEURE HEBDOMADAIRE 58
        liste_de_paires.append((3, (78, 244),""))    # COMMENTAIRE SUR LE TEMPS DE TRAVAIL 59
        # SI TROP LONG, (30,248)
        liste_de_paires.append((3, (78, 257),""))    # NOMBRE JOUR DE CONGES AUTORISES 60
        
        
        print("ready to write on pdf\n")

        write_data_to_pdf('C:\\workspace\\s10\\lms_moodle\\Fiche_de_liaison_Licence_2023-2024.pdf', output_fichier, chemin_fichier, liste_de_paires)

        print( "traitement terminé")
        fenetre.quit()  # Quitter la boucle principale de l'interface graphique
        fenetre.destroy()  # Détruire la fenêtre principale
        
        



         
def mm_to_points(mm):
    # Conversion de millimètres en points (1 mm = 2.83465 points)
    return mm * 2.83465


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
                        can.setFont('Helvetica', 10)
                        can.drawString(mm_to_points(x)+ 5, mm_to_points(297) - mm_to_points(y) - 5, texte_a_inserer)  # Ajouter à une position spécifique
                        can.save()
                        packet.seek(0)
                        new_pdf = PyPDF2.PdfReader(packet)
                        page.merge_page(new_pdf.pages[0])
                writer.add_page(page)
            # Enregistrement du fichier PDF de sortie
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
                
           # subprocess.Popen(['start', '', output_pdf], shell=True)
                    
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
 

