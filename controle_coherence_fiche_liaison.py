import csv
import PyPDF2
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from verification import Verification
import tkinter as tk
from tkinter import filedialog
import io
import os
from traitementAlternance import remplir_fichier_excel, creer_dossier,write_error_report_to_csv
import time
import pandas as pd



###################  FONCTION DE CONTROLE  ######################################################################
def controle_coherence(liste_coordonnees_texte) :
    liste_retour = []
    liste_fonctions_verification = [
        (Verification.verify_numero_etudiant,(0,"numero_etudiant")),
        (Verification.verify_nom,(1,"nom")),
        (Verification.verify_prenom,(2,"prenom")),
        (Verification.verify_code_postal,(7,"code_postal")), 
        (Verification.verify_numero_telephone_france,(10,"numero telephone")),
        (Verification.verify_numero_telephone_france,(11,"numero telephone")),
        (Verification.verify_numero_telephone_france,(34,"numero telephone")),
        (Verification.verify_numero_telephone_france,(97,"numero telephone")),
        (Verification.verify_email_etudiant, (12, "email_etudiant")),
        (Verification.verify_email_personnel, (13, "email_personnel")),
        (Verification.nombre_jour_travail_hebdomadaire,(60, "jour travail hebdomadaire")),
        (Verification.nombre_heure_hebdomadaire,(63, "nombre d'heures hebdomadaires"))
        #(Verification.verify_siren_ou_siret,(19, "siret"))
        
        ]
    
    for fonction_verif, (index,label) in liste_fonctions_verification :
        resultat_verif = fonction_verif(liste_coordonnees_texte[index][2])
        if not resultat_verif :
            liste_retour.append("erreur au niveau : " + label)
    
    resultat_verif = Verification.verify_date_periode_stage(liste_coordonnees_texte[53][2],liste_coordonnees_texte[54][2]) # position dans la liste des coordonnees de debut/fin de stage
    
    if not resultat_verif :
        liste_retour.append("erreur au niveau : date periode du stage")
    
    return liste_retour
    

def controle_coherence_ecriture_sur_pdf(input_pdf, output_pdf, fichier_csv, liste_coordonnees_texte) :
    try : 
        
        cpt = 0
        cpt_liste_coordonnees = 0 
        numero_ligne = 0
        nom_etudiant = ""
        prenom_etudiant = ""
        chemin_fichier = output_pdf
        output_pdf = ""
        error_report = []
        
        #############################   LECTURE DU FICHIER CSV   ####################################################
        with open(fichier_csv,'r') as file :
            reader = csv.reader(file, delimiter=',')
            for ligne in reader :
                for element in ligne : 
                    cpt += 1 
                    
                    ####################   l'indice 96 est l'indice a partir duquel les elements du csv commencent a nous interesser, avant ce sont des metadonnees qui nous interesse pas 
                    if cpt >= 96 and cpt_liste_coordonnees < len(liste_coordonnees_texte) :
                        print("cpt et son element : " + str(cpt_liste_coordonnees) + "" + str(element))
                        if cpt == 97 :
                            nom_etudiant = element
                        elif cpt == 98 :
                            prenom_etudiant = element
                        cpt_liste_coordonnees,liste_coordonnees_texte = remplir_case(element, cpt, cpt_liste_coordonnees,liste_coordonnees_texte)
                if numero_ligne >= 1 :
                    today = datetime.date.today()
                    formatted_today = today.strftime("%Y%m%d")
                    output_pdf += chemin_fichier + "//"+ str(formatted_today) + "_" + nom_etudiant + "_" + prenom_etudiant + "_FL_L3" + ".pdf"
                    print("Le fichier "+ output_pdf + " est en cours d'ecriture...")
                    retour_controle_coherence = controle_coherence(liste_coordonnees_texte)
                    if (retour_controle_coherence == []) :
                        write_data_to_pdf(input_pdf, output_pdf, liste_coordonnees_texte)
                    else :
                        print("le fichier n'a pas pu être généré, voici les erreurs rencontrées :")
                        for erreur in retour_controle_coherence :
                            print(erreur)
                        error_report.append({
                            "Nom": nom_etudiant,
                            "Email": liste_coordonnees_texte[12][2],
                            "error": retour_controle_coherence})
                        filename = f"{nom_dossier_fiche_liaison}\\error_report.csv"
                        write_error_report_to_csv(error_report, filename)                
                    # RE INITIALISATION DE TOUTE LES VARIABLE POUR COMMENCER A REMPLIR UN NOUVEAU PDF
                    for i, (num, coords, champ) in enumerate(liste_coordonnees_texte):  
                        if isinstance(champ, str):
                            liste_coordonnees_texte[i] = (num, coords, "")
                    output_pdf = ""
                    cpt_liste_coordonnees = 0
                       # 10 de moins de là on commence a recupere les donnees --> 10 metadonnees que l'on ne veut pas recuperer en debut de ligne
                cpt = 86
                numero_ligne += 1                               
                
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
        
    return liste_coordonnees_texte, nom_etudiant, prenom_etudiant


def remplir_plusieurs_ligne_a_partir_un_string(element,cpt_liste_coordonnees,liste_coordonnees, cpt) :
    
    taille_element = len(element)
    taille_max_premiere_ligne = 0
    taille_max_deuxieme_ligne = 0
    premiere_partie = ""
    deuxieme_partie = ""
    troisieme_partie = ""
    
    if cpt == 137 :
        taille_max_premiere_ligne = 80
    elif cpt == 138 :
        taille_max_premiere_ligne = 40 
    elif cpt == 139 :
        taille_max_premiere_ligne = 30
        taille_max_deuxieme_ligne = 105
    elif cpt == 140 :
        taille_max_premiere_ligne = 45
        taille_max_deuxieme_ligne = 105
    elif cpt == 150 :
        taille_max_premiere_ligne = 80
    
    if taille_element > taille_max_premiere_ligne :
        premiere_partie = element[:taille_max_premiere_ligne]
        if (taille_element > taille_max_premiere_ligne + taille_max_deuxieme_ligne and taille_max_deuxieme_ligne != 0) :
            deuxieme_partie = element[taille_max_premiere_ligne:taille_max_premiere_ligne+taille_max_deuxieme_ligne]
            troisieme_partie = element[taille_max_deuxieme_ligne+taille_max_premiere_ligne:]
        else :
            deuxieme_partie = element[taille_max_premiere_ligne:]
        
        
        num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
        nouvel_element = (num_page,coordonnees,premiere_partie)
        liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
        cpt_liste_coordonnees += 1
        num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
        nouvel_element = (num_page,coordonnees,deuxieme_partie)
        liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
        cpt_liste_coordonnees += 1
        if taille_max_deuxieme_ligne > 0 :
            if troisieme_partie != "" :
                num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
                nouvel_element = (num_page,coordonnees,troisieme_partie)
                liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
            cpt_liste_coordonnees += 1
            
    else :
        num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
        nouvel_element = (num_page,coordonnees,element)
        liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
        if taille_max_deuxieme_ligne != 0 :
            cpt_liste_coordonnees + 3
        else :
            cpt_liste_coordonnees += 2
    
    return (cpt_liste_coordonnees, liste_coordonnees)   
    
             


def case_a_cocher(element, cpt_liste_coordonnees, liste_coordonnees_texte, numeric, cpt) :
    
# Quand finctionne pas par string
    if (numeric) :
        if cpt == 113 : 
            if element == '0' :
                cpt_liste_coordonnees += 1
                num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
                nouvel_element = (num_page,coordonnees,"x")
                liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
                cpt_liste_coordonnees += 1
            else : 
                num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
                nouvel_element = (num_page,coordonnees,"x")
                liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
                cpt_liste_coordonnees += 2
        else : 
            if element == '0' :
                return (cpt_liste_coordonnees+1, liste_coordonnees_texte)
            else : 
                num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
                nouvel_element = (num_page,coordonnees,"x")
                liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
                cpt_liste_coordonnees += 1
    
    else : 
        if element == '1' :
            num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
            nouvel_element = (num_page,coordonnees,"x")
            liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
            cpt_liste_coordonnees += 2
            
        elif element == '2' :
            cpt_liste_coordonnees += 1
            num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
            nouvel_element = (num_page,coordonnees,"x")
            liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
            cpt_liste_coordonnees += 1
            
        elif element == '3' :
            cpt_liste_coordonnees += 2
            num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
            nouvel_element = (num_page,coordonnees,"x")
            liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
            cpt_liste_coordonnees += 1 
                
        else :
            cpt_liste_coordonnees += 3
            num_page, coordonnees,_ = liste_coordonnees_texte[cpt_liste_coordonnees]
            nouvel_element = (num_page,coordonnees,"x")
            liste_coordonnees_texte[cpt_liste_coordonnees] = nouvel_element
            cpt_liste_coordonnees += 1   
          
    return (cpt_liste_coordonnees, liste_coordonnees_texte)    

def remplir_case(element,cpt, cpt_liste_coordonnees, liste_coordonnees) :
    
    numeric = False
    
    if cpt in (99,100,105, 123) :
        diviser_element = element.split(":")
        element = diviser_element[1].strip()
        num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
        nouvel_element = (num_page,coordonnees,element)
        liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
        cpt_liste_coordonnees += 1
    
    
    #stage en rapport avec offre de stage diffuse par univerite : oui ou non
    elif cpt == 113 :
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees,numeric, cpt)
        
    # Tuteur de stage monsieur ou madame
    elif cpt == 126 :
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero ,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
            
    #type de stage
    elif cpt == 131 :
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
    elif cpt == 132 :
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees , numeric, cpt)     
    elif cpt == 133 :
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
    elif cpt == 134 :
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
    
    
    elif cpt == 143 :   #Interruption au cours du stage
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
    
    
    # GESTION TEXTE SUR PLUSIEURS LIGNES
    elif cpt in (137,138,139,140,150) : 
        cpt_liste_coordonnees,liste_coordonnees = remplir_plusieurs_ligne_a_partir_un_string(element,cpt_liste_coordonnees,liste_coordonnees, cpt)
    
    
    
    
    elif cpt == 148 : 
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
    elif cpt == 152 : 
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
        
        
    elif cpt in (154,155,156,157) : # MONTANT GRATIFICATION par heure/mois brut/net
        numeric = True
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(element,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
      
    elif cpt in (159,160) : # modalite versement/stage trouve/confidentialite stage
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
        if numero in('1', '2') :
            cpt_liste_coordonnees += 1
            
    elif cpt == 161 : 
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
            
    elif cpt in (164,165) :
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
   
    elif cpt == 167 :
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
        if numero in ('1','2') :
            cpt_liste_coordonnees += 2
        if numero == '3' :
            cpt_liste_coordonnees += 1
            
    elif cpt == 168 :
        numero = element.split(':')[0].strip()
        cpt_liste_coordonnees,liste_coordonnees = case_a_cocher(numero,cpt_liste_coordonnees,liste_coordonnees, numeric, cpt)
        
    else : 
        num_page, coordonnees, _ = liste_coordonnees[cpt_liste_coordonnees]
        nouvel_element = (num_page,coordonnees,element)
        liste_coordonnees[cpt_liste_coordonnees] = nouvel_element
        cpt_liste_coordonnees += 1
        
    return(cpt_liste_coordonnees,liste_coordonnees)


        
        
def choisir_fichier():
    # Ouvrir une boîte de dialogue pour choisir le fichier CSV
    fichier_csv = filedialog.askopenfilename(title = "Choisir le fichier CSV contenant les informations des étudiants",filetypes=[("Fichiers CSV", "*.csv")])
    input_pdf = filedialog.askopenfilename(title="Choisir la fiche de liaison L1/L2/L3 vierge", filetypes=[("PDF files", "*.pdf")])
    
    # Si un fichier a été sélectionné, lire son contenu
    if fichier_csv:
        repertoire_fichier = os.path.dirname(fichier_csv)
        print("repertoire fichier = "+repertoire_fichier)
        output_pdf = nom_dossier_fiche_liaison
        liste_de_paires = [] 
        start_time = time.time()
        
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
        liste_de_paires.append((3, (63, 61.9),""))    # ACTIVITE DE L ETABLISSEMENT 24
        liste_de_paires.append((3, (81, 66.9),""))    # TYPE D ETABLISSEMENT 25
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
        liste_de_paires.append((3, (27.5, 150.8),""))   # SI THEMATIQUE TROP LONG CHANGER DE LIGNE ET PASSER A (30,152)
        
        liste_de_paires.append((3, (113, 154.5),""))    # SUJET DE STAGE  45
        liste_de_paires.append((3, (28, 157.5),"")) # SI SUJET TROP LONG CHANGER DE LIGNE ET PASSER A (30,159) 46
        
        liste_de_paires.append((3, (133, 160.5),""))    # FONCTION ET TACHES CONFIEES AU STAGIAIRE 47
        liste_de_paires.append((3, (28, 164),"")) #48
        liste_de_paires.append((3, (28, 167),"")) #49
        # SI TROP LONG PASSER A (30,165), PUIS (30,168)
        liste_de_paires.append((3, (103, 170),""))  # COMETENCES A ACQUERIR PENDANT STAGE 50
        liste_de_paires.append((3, (28, 174),"")) #51
        liste_de_paires.append((3, (28, 177),""))#52
        # SI TROP LONG, (30,174) PUIS (30, 178)
        
        
        
        ############ DATE HORAIRES DEROULEMENT DU STAGE ###################################
        
        liste_de_paires.append((3, (53, 190.5),""))    # DEBUT DE STAGE 53
        liste_de_paires.append((3, (50, 194),""))    # FIN DU STAGE 54
        liste_de_paires.append((3, (67.3, 197.5),""))    # INTERUPTION EN COURS DU STAGE OUI 50
        liste_de_paires.append((3, (74.7, 197.5),""))    # INTERUPTION EN COURS DU STAGE NON 51
        liste_de_paires.append((3, (77, 201),""))    # DATE DEBUT INTERRUPTION 52
        liste_de_paires.append((3, (74, 204),""))    # DATE FIN INTERRUPTION 53
        liste_de_paires.append((3, (112, 211),""))    # DUREE EFFECTIF DU STAGES EN HEURES 54
        liste_de_paires.append((3, (85.5, 224),""))    # NOMBRE DE JOUR DE TRAVAIL HEBDO 55
        liste_de_paires.append((3, (50.5, 228),""))    # TEMPS DE TRAVAIL = TEMPS PLEINS 56
        liste_de_paires.append((3, (69.4, 228),""))    # TEMPS DE TRAVAIL = TEMPS PARTIEL 57
        liste_de_paires.append((3, (73, 234),""))    # NOMBRE D HEURE HEBDOMADAIRE 58
        liste_de_paires.append((3, (78, 243),""))    # COMMENTAIRE SUR LE TEMPS DE TRAVAIL 59
        liste_de_paires.append((3, (28, 248),""))
        # SI TROP LONG, (30,248)
        liste_de_paires.append((3, (78, 257),""))    # NOMBRE JOUR DE CONGES AUTORISES 60
        
        
        
        
        ########### PAGE 3 ##########################################################################################
        
        ########### GRATIFICATION ################################################################################
        
        
        liste_de_paires.append((4, (67.35, 39.3),""))    #  GRATIFICATION AU COURS DU STAGE OUI 61
        liste_de_paires.append((4, (75.35, 39.3),""))    #  GRATIFICATION AU COURS DU STAGE NON 62
        liste_de_paires.append((4, (100, 45.3),""))    #  MONTANT DE LA GRATIFICATION EN EUROS 63
        liste_de_paires.append((4, (27.1, 49.1),""))    #  PAR HEURE 64
        liste_de_paires.append((4, (47, 49.1),""))    #  PAR MOIS 65
        liste_de_paires.append((4, (61.5, 49.1),""))    #  EN NET 66
        liste_de_paires.append((4, (73, 49.1),""))    #  EN BRUT 67
        liste_de_paires.append((4, (85, 56),""))    #  MONTANT DE LA GRATIFICATION EN DEVISE LOCALE 68
        liste_de_paires.append((4, (81.5, 62.2),""))    #  EN CHEQUE 69
        liste_de_paires.append((4, (95.1, 62.2),""))    #  VIREMENT BANCAIRE 70
        liste_de_paires.append((4, (122.1, 62.3),""))    #  ESPECES 71
        
        
        ############# DIVERS ####################################################################################
        
        liste_de_paires.append((4, (26, 85),""))    #  REPONSE A UNE OFFRE DE STAGE 72
        liste_de_paires.append((4, (71, 85),""))    #  CANDIDATURE SPONTANEE 73
        liste_de_paires.append((4, (108, 85),""))    #  RESEAU DE CONNAISSANCE 74
        liste_de_paires.append((4, (76.1, 91.1),""))    #  CONFIDENTIALITE DU SUJET OUI 75 
        liste_de_paires.append((4, (84, 91.1),""))    #  CONFIDENTIALITE DU SUJET NON 76
        liste_de_paires.append((4, (131, 96.4),""))    #  MODALITE DU SUIVI 77
        liste_de_paires.append((4, (124, 103),""))    #  LISTE DES AVANTAGES EN NATURE 78
        liste_de_paires.append((4, (77.1, 110),""))    #  NATURE DU TRAVAIL A FOURNIR MEMOIRE 79
        liste_de_paires.append((4, (97.2, 110),""))    #  NATURE DU TRAVAIL A FOURNIR RAPPORT DE STAGE 80
        liste_de_paires.append((4, (67.7, 116.2),""))    #  MODALITE DE VALIDATION STAGE SOUTENANCE 81
        liste_de_paires.append((4, (87.1, 116.2),""))    #  MODALITE DE VALIDATION STAGE SUIVI STAGE 82
        liste_de_paires.append((4, (124, 122),""))    #  SI STAGIAIRE DOIT ETRE PRESENT LA NUIT 83
        liste_de_paires.append((4, (25.2, 132.6),""))    #  LANGUE DE LA CONVENTION FRANCAIS 84
        liste_de_paires.append((4, (25.4, 135.7),""))    #  LANGUE DE LA CONVENTION ALLEMAND 86
        liste_de_paires.append((4, (105.2, 132.55),""))    #  LANGUE DE LA CONVENTION ANGLAIS 85 
        liste_de_paires.append((4, (105.1, 136),""))    #  LANGUE DE LA CONVENTION ESPAGNOL 87
        
        
     
        
        ########### ENSEIGNANT REFERENT STAGES ######################################################################
        
    #    liste_de_paires.append((4, (38, 151),""))    #  NOM 88
    #    liste_de_paires.append((4, (42, 158),""))    #  PRENOM 89
    #    liste_de_paires.append((4, (36, 166),""))    #  TEL 90
    #    liste_de_paires.append((4, (93, 1166),""))    #  MAIL 91
    #    liste_de_paires.append((4, (70, 171),""))    #  FONCTION DISCIPLINES ENSEIGNEES 92
        
          
        
        
        ##########REPRESENTANT LEGAL ETABLISSEMENT ACCUEIL #############################################################
        
        liste_de_paires.append((4, (28, 187),""))    #  MONSIEUR 93
        liste_de_paires.append((4, (38.6, 187),""))    #  MADAME 94
        liste_de_paires.append((4, (30, 190),""))    #  NOM PRENOM 95
        #SI TROP LONG, (30,194)
        liste_de_paires.append((4, (36, 200),""))    #  tel 97
        liste_de_paires.append((4, (92, 200),""))    #  MAIL 98
        liste_de_paires.append((4, (45, 207),""))    #  FONCTION 99
        liste_de_paires.append((4, (36, 217),""))    #  DATE 100
        
        
        print("ready to write on pdf\n")

        controle_coherence_ecriture_sur_pdf(input_pdf, output_pdf, fichier_csv, liste_de_paires)

        print( "traitement terminé")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Temps écoulé :", elapsed_time, "secondes")
        fenetre_initiale.quit()  # Quitter la boucle principale de l'interface graphique
        fenetre_initiale.destroy()  # Détruire la fenêtre principale
        
        

         
def mm_to_points(mm):
    # Conversion de millimètres en points (1 mm = 2.83465 points)
    return mm * 2.83465


def write_data_to_pdf(input_pdf, output_pdf, liste_coordonnees_texte):
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
            
            print("le fichier " + output_pdf + " a ete généré avec succés")
            
                
           # subprocess.Popen(['start', '', output_pdf], shell=True)
           
                    
    except Exception as e:
        print("Une erreur est survenue lors de l'ajout de données au PDF :", e)
        
        

# DEROULER DE TOUT L'ALGORITHME
# VERSION FINALE DOIT SE COMPOSER :
#   - Recupération fichier csv en passant par l'utilisateur
#   - Effectuer controle de coherence sur les donnees
#   - Implementer la liste de texte coordonnees
#   - Boucler dessus pour ajouter chaque élément au bon emplacement



def on_selection():
    if var.get() == "alternance":
        remplir_fichier_excel(nom_dossier_alternant)
        fenetre_initiale.quit()
        fenetre_initiale.destroy()
    else:
       # Créer une fenêtre principale
        fenetre = tk.Tk()
        fenetre.title("Lire un fichier CSV")

        # Créer un bouton pour choisir le fichier CSV
        bouton_choisir_1 = tk.Button(fenetre, text="Choisir les fichiers CSV et PDF", command=choisir_fichier)
        bouton_choisir_1.pack(pady=10)

     # Lancer la boucle principale de l'interface graphique
        fenetre.mainloop()
        fenetre.quit()
        fenetre.destroy()

# Recupération fichier csv en passant par l'utilisateur
if __name__ == "__main__":
    nom_dossier_fiche_liaison, nom_dossier_alternant = creer_dossier()
    # Créer la fenêtre principale
    fenetre_initiale = tk.Tk()
    fenetre_initiale.title("Choix de l'option")

    # Variable pour stocker la sélection
    var = tk.StringVar(value="")
    # Créer les boutons radio pour choisir entre "stage" et "alternance"
    radio_stage = tk.Radiobutton(fenetre_initiale, text="Stage fiche de liaison", variable=var, value="stage")
    radio_alternance = tk.Radiobutton(fenetre_initiale, text="Alternance fichier excel", variable=var, value="alternance")
    
    radio_stage.pack(pady=5)
    radio_alternance.pack(pady=5)

    # Créer un bouton pour valider la sélection
    bouton_valider = tk.Button(fenetre_initiale, text="Valider", command=on_selection)
    bouton_valider.pack(pady=10)
    
    # Lancer la boucle principale de l'interface graphique
    fenetre_initiale.mainloop()
        
        
 

